from __future__ import annotations

from pathlib import Path

from jetpytools import SingleOrArr
from muxtools import Setup, VideoFile
from muxtools import mux as vsmux
from pydantic import BaseModel, ConfigDict
from vodesfunc import adaptive_grain, ntype4
from vsdeband import pfdeband, placebo_deband
from vsdehalo import fine_dehalo
from vsdenoise import (
    MVToolsPreset,
    Prefilter,
    bm3d,
    mc_degrain,
    nl_means,
)
from vsdenoise.blockmatch import BM3D
from vsdenoise.nlm import NLMeans
from vsexprtools import norm_expr
from vsmuxtools import SourceFilter, do_audio, settings_builder_x265, src_file, x265
from vspreview import is_preview
from vsrgtools import bilateral
from vstools import (
    ChromaLocation,
    core,
    DitherType,
    FrameRangeN,
    FrameRangesN,
    Keyframes,
    finalize_clip,
    replace_ranges,
    set_output,
    SPath,
    vs,
)

from monster_common.sources import Source, sources


# <https://github.com/sgt0/encodes/blob/2ea22f/src/sgtfunc/sgtfunc/sgtfunc.py#L12>
def denoise(
    clip: vs.VideoNode,
    block_size: int = 64,
    limit: int | tuple[int | None, int | None] | None = None,
    refine: int = 3,
    sigma: SingleOrArr[float] = 0.7,
    sr: int = 2,
    strength: float = 0.2,
    thSAD: int | tuple[int, int] = 115,  # noqa: N803
    tr: int = 2,
) -> vs.VideoNode:
    """MVTools + BM3D + NLMeans denoise."""

    ref = mc_degrain(  # type: ignore[call-overload]
        clip,
        prefilter=Prefilter.DFTTEST,
        preset=MVToolsPreset.HQ_SAD,
        blksize=block_size,
        thsad=thSAD,
        limit=limit,
        refine=refine,
    )

    denoised_luma = bm3d(
        clip, ref=ref, sigma=sigma, tr=tr, profile=BM3D.Profile.NORMAL, planes=0
    )
    denoised_luma = ChromaLocation.ensure_presence(
        denoised_luma, ChromaLocation.from_video(clip, strict=True)
    )

    return nl_means(
        denoised_luma,
        ref=ref,
        h=strength,
        tr=tr,
        a=sr,
        wmode=NLMeans.WeightMode.BISQUARE_HR,  # wmode=3
        planes=[1, 2],
    )


class FilterchainResults(BaseModel):
    src: vs.VideoNode
    final: vs.VideoNode
    audio_file: src_file

    model_config = ConfigDict(arbitrary_types_allowed=True)


def filterchain(
    *,
    episode: str,
    source: Source,
    no_dehalo: FrameRangeN | FrameRangesN | None = None,
    mini: bool = False,
    dynamic_detail_scenes: FrameRangeN | FrameRangesN | None = None
) -> FilterchainResults:
    cr_file = src_file(
        str(source.cr_path),
        trim=(None, -24),
        preview_sourcefilter=SourceFilter.BESTSOURCE,
    )
    amzn_file = src_file(
        str(source.amzn_path), preview_sourcefilter=SourceFilter.BESTSOURCE
    )

    cr = cr_file.init_cut().std.SetFrameProps(source="CR")
    amzn = amzn_file.init_cut().std.SetFrameProps(source="AMZN")

    assert cr.num_frames == amzn.num_frames

    keyframes = Keyframes.unique(cr, episode)
    src = keyframes.to_clip(cr, scene_idx_prop=True)

    # Denoise
    if not mini:
        denoised = denoise(src, sigma=0.72, strength=0.27, thSAD=117, tr=3)
    else:
        heavy_denoised = denoise(src, sigma=1.07, strength=0.27, thSAD=257, tr=3)
        weak_denoised = denoise(src, sigma=0.57, strength=0.17, thSAD=87, tr=2)
        weak_denoised = core.vszip.LimitFilter(weak_denoised, src, dark_thr=0.25, bright_thr=1.5, elast=3.5)

        assert dynamic_detail_scenes is not None
        denoised = replace_ranges(heavy_denoised, weak_denoised, dynamic_detail_scenes)

    # Dehalo
    dehaloed = fine_dehalo(denoised, blur=1.7, thmi=50, pre_ss=2)
    dehaloed = ChromaLocation.ensure_presence(
        dehaloed, ChromaLocation.from_video(denoised, strict=True)
    )
    bilateref = bilateral(denoised, ref=dehaloed, sigmaR=5 / 255, sigmaS=6)
    dehaloed = norm_expr([denoised, dehaloed, bilateref], "x y z max min")
    if no_dehalo is not None:
        dehaloed = replace_ranges(dehaloed, denoised, no_dehalo)

    # Deband
    if not mini:
        debanded = pfdeband(dehaloed, thr=1.3, debander=placebo_deband)

    # Regrain
    if not mini:
        grained = adaptive_grain(
            debanded,
            strength=[1.92, 0.4],
            size=3.16,
            temporal_average=50,
            seed=274810,
            **ntype4,
        )

        final = finalize_clip(grained)

    if mini:
        final = finalize_clip(dehaloed, dither_type=DitherType.NONE)

    if is_preview():
        set_output(src, "src")
        set_output(denoised, "denoised")
        set_output(dehaloed, "dehaloed")
        set_output(final, "final")

    return FilterchainResults(src=cr, final=final, audio_file=amzn_file)


def mux(
    *,
    episode: str,
    source: Source,
    filterchain_results: FilterchainResults,
) -> Path | str:
    setup = Setup(episode)
    assert setup.work_dir

    # Video
    settings = settings_builder_x265(
        preset="placebo",
        crf=13.5,
        rd=3,
        rect=False,
        ref=5,
        bframes=12,
        qcomp=0.72,
        limit_refs=1,
        merange=57,
        asm="avx512",
        keyint=round(filterchain_results.final.fps) * 10,
        frames=filterchain_results.final.num_frames,
    )
    encoded = Path(setup.work_dir).joinpath("encoded.265").resolve()
    zones: list[tuple[int, int, float]] = []
    if source.op is not None:
        zones.append((source.op[0], source.op[1], 1.2))
    if source.ed is not None:
        zones.append((source.ed[0], source.ed[1], 1.2))
    video = (
        VideoFile(encoded)
        if encoded.exists()
        else x265(
            settings, zones=zones, qp_clip=filterchain_results.src, resumable=False
        ).encode(filterchain_results.final)
    )

    return vsmux(
        video.to_track(
            "WEB encode by sgt",
            "jpn",
            default=True,
            forced=False,
            args=["--deterministic", "274810"],
        ),
        do_audio(filterchain_results.audio_file).to_track(
            "E-AC-3 2.0", "jpn", default=True, forced=False
        ),
    )

def mux_mini(
    episode: str,
    filterchain_results: FilterchainResults,
    target: SPath
):
    pass

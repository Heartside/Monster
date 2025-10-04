from muxtools import (
    Chapters,
    GlobSearch,
    Premux,
    Setup,
    SubFile,
    TmdbConfig,
    mux,
    ASSHeader,
)

epi = int(input("Enter episode number: "))

setup = Setup(
    f"{epi:02d}",
    None,
    out_dir=R"This Monster Wants to Eat Me (2025) - S01 (WEBRip 1080p HEVC E-AC-3) [Dual Audio] [Heartside]",
    mkv_title_naming="",
    out_name=R"[Heartside] This Monster Wants to Eat Me (2025) - S01E$ep$ (WEBRip 1080p HEVC E-AC-3) [$crc32$]",  # CHANGE THIS BEFORE RELEASE!!!!!!!!!!!!!
    clean_work_dirs=True,
    error_on_danger=True,
)

premux = GlobSearch(f"./{setup.episode}/*Monster* - {setup.episode}*premux*.mkv")

subs = (
    SubFile(
        GlobSearch(
            f"./{setup.episode}/Monster - {setup.episode} - *.ass", allow_multiple=True
        )
    )
    .clean_styles()
    .clean_garbage()
    .clean_comments()
    .clean_extradata()
)

op = (
    SubFile("./common/OP/OP.ass")
    .clean_styles()
    .clean_garbage()
    .clean_comments()
    .clean_extradata()
)

ed = (
    SubFile("./common/ED/ED.ass")
    .clean_styles()
    .clean_garbage()
    .clean_comments()
    .clean_extradata()
)

premux = Premux(premux, subtitles=None, keep_attachments=False)

chapters = Chapters.from_sub(subs, timesource=premux.file)

full = subs.merge("./common/OP/OP.ass", sync="Opening", timesource=premux.file) # TODO: FIX THIS
full = full.merge("./common/ED/ED.ass", sync="Ending", timesource=premux.file)

full = full.set_headers(
    (ASSHeader.PlayResX, 1920),
    (ASSHeader.PlayResY, 1080),
    (ASSHeader.LayoutResX, 1920),
    (ASSHeader.LayoutResY, 1080),
    (ASSHeader.YCbCr_Matrix, "TV.709"),
    (ASSHeader.ScaledBorderAndShadow, True),
)


fonts = full.collect_fonts()

mux(
    premux,
    full.to_track("Full Subtitles [Heartside]", "eng", default=True, forced=False),
    *fonts,
    chapters,
    tmdb=TmdbConfig(274810, season=1),
)

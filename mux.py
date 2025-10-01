from muxtools import GlobSearch, Premux, Setup, SubFile, TmdbConfig, mux

ep = int(input("Enter episode number: "))

setup = Setup(
    f"{ep:02d}",
    None,
    out_dir=R"This Monster Wants to Eat Me (2025) - S01 (WEBRip 1080p HEVC AAC) [Dual Audio] [Heartside]",
    mkv_title_naming="",
    out_name=R"[Heartside] This Monster Wants to Eat Me (2025) - S01E$ep$ (WEBRip 1080p HEVC AAC) [$crc32$]",  # CHANGE THIS BEFORE RELEASE!!!!!!!!!!!!!
    clean_work_dirs=True,
    error_on_danger=True,
)

premux = GlobSearch(f"./{setup.episode}/Monster - {setup.episode} - Premux*.mkv")

dialogue = (
    SubFile(f"./{setup.episode}/Monster - {setup.episode} - Dialogue.ass")
    .clean_styles()
    .clean_garbage()
    .clean_comments()
    .clean_extradata()
)

signs = (
    SubFile(f"./{setup.episode}/Monster - {setup.episode} - Signs.ass")
    .clean_styles()
    .clean_garbage()
    .clean_comments()
    .clean_extradata()
)

op = (
    SubFile(f"./common/op/OP.ass")
    .clean_styles()
    .clean_garbage()
    .clean_comments()
    .clean_extradata()
)

ed = (
    SubFile(f"./common/ed/ED.ass")
    .clean_styles()
    .clean_garbage()
    .clean_comments()
    .clean_extradata()
)

# dubtitles= SubFile(f"./{setup.episode}/This Monster Wants to Eat Me - {setup.episode} - Dubtitles.ass").clean_styles().clean_garbage().clean_comments()

fonts = dialogue.collect_fonts(use_system_fonts=False)
signsfonts = signs.collect_fonts(use_system_fonts=False)
opfonts = op.collect_fonts(use_system_fonts=False)

premux = Premux(premux, subtitles=None, keep_attachments=False)

mux(
    premux,
    dialogue.to_track("Full Subtitles [Heartside]", "eng", default=True, forced=False),
    signs.to_track("Signs/Songs [Heartside]", "eng", default=False, forced=True),
    # dubtitles.to_track("Dubtitles (SDH) [Heartside]", "eng", default=False, forced=False),
    *fonts,
    tmdb=TmdbConfig(274810, season=1),
)

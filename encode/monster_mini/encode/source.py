#!/usr/bin/env python3

import os
from pathlib import Path
from vapoursynth import core

source_file = Path(os.environ["SOURCE_FILE"])
if not source_file.exists():
    raise FileNotFoundError("Source file not found.")
source_ffindex_file = Path(os.environ["SOURCE_FFINDEX_FILE"])

src = core.ffms2.Source(source_file, cachefile=source_ffindex_file)

src.set_output()

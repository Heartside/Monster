import os
from vstools import core, SPath


source_file = SPath(os.environ["SOURCE_FILE_CR"])
if not source_file.exists():
    raise FileNotFoundError("Source file not found.")


src = core.bs.VideoSource(source_file)

src = src[:-24]

src.set_output()

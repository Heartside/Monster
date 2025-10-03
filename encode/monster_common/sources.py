from __future__ import annotations

import os
from pathlib import Path, PurePath

from pydantic import BaseModel

raws_directory_raw = os.getenv("RAWS_DIRECTORY")
if raws_directory_raw is None:
    print("RAWS_DIRECTORY environment variable is not set.")
    exit(1)
raws_directory = Path(raws_directory_raw)


class Source(BaseModel):
    cr_path: PurePath | str
    amzn_path: PurePath | str
    op: tuple[int, int] | None = None
    ed: tuple[int, int] | None = None


sources = {
    "01": Source(
        cr_path=raws_directory / "01 (CR).mkv",
        amzn_path=raws_directory / "01 (AMZN).mkv",
        op=(1678, 1678 + 2156 + 2),
        ed=(31649, 31649 + 2156 + 1),
    )
}

from __future__ import annotations


from vspreview import is_preview

from monster_common import filterchain, mux, sources

EPISODE = "01"
source = sources[EPISODE]
NO_DEHALO = [
    source.op,
    source.ed,
    (3948, 4042),  # Episode title.
    (33807, None),  # Preview.
]


filterchain_results = filterchain(episode=EPISODE, source=source, no_dehalo=NO_DEHALO)

if not is_preview():
    mux(episode=EPISODE, source=source, filterchain_results=filterchain_results)

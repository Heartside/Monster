from __future__ import annotations


from argparse import ArgumentParser, BooleanOptionalAction

parser = ArgumentParser()
parser.add_argument("--main", action=BooleanOptionalAction, default=True)
parser.add_argument("--mini", action=BooleanOptionalAction, default=False)
args = parser.parse_args()


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

if args.main:
    filterchain_results = filterchain(episode=EPISODE, source=source, no_dehalo=NO_DEHALO)

    if not is_preview():
        mux(episode=EPISODE, source=source, filterchain_results=filterchain_results)

if args.mini:
    from monster_common import mux_mini
    from monster_mini import finalise_dynamic_detail_scenes, get_dynamic_detail_scenes, get_paths, scene_detection

    scene_detection_temp_dir, dynamic_detail_scenes_json, dynamic_detail_scenes_zones, intermediate = get_paths(EPISODE)

    scene_detection(scene_detection_temp_dir, source.cr_path, dynamic_detail_scenes_json)
    finalise_dynamic_detail_scenes(dynamic_detail_scenes_json, dynamic_detail_scenes_zones, source)
    dynamic_detail_scenes = get_dynamic_detail_scenes(dynamic_detail_scenes_json)

    filterchain_results = filterchain(episode=EPISODE, source=source, no_dehalo=NO_DEHALO, mini=args.mini, dynamic_detail_scenes=dynamic_detail_scenes)

    if not is_preview():
        mux_mini(episode=EPISODE, filterchain_results=filterchain_results, target=intermediate)

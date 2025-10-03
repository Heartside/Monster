import json
from muxtools import Setup
import os
import subprocess
import sys
from vstools import SPath


def get_paths(episode):
    setup = Setup(episode)

    scene_detection_temp_dir = SPath(setup.work_dir) / "mini.scene-detection.tmp"
    dynamic_detail_scenes_json = SPath(setup.work_dir) / "mini-flashback-scenes.json"

    intermediate_dir_raw = os.getenv("INTERMEDIATE_DIRECTORY")
    if intermediate_dir_raw is None:
        raise ValueError("INTERMEDIATE_DIRECTORY environment variable is not set.")
    intermediate_dir = SPath(intermediate_dir_raw)

    dynamic_detail_scenes_zones = intermediate_dir / f"{episode}.zones.txt"
    intermediate = intermediate_dir / f"{episode}.264"

    return scene_detection_temp_dir, dynamic_detail_scenes_json, dynamic_detail_scenes_zones, intermediate


def scene_detection(temp_dir, source, output_json):
    env = dict(os.environ)
    env["SOURCE_FILE_CR"] = str(source)
    command = [
        sys.executable, SPath(__file__).parent / "scripts" / "scene-detection.py",
        "--temp", temp_dir,
        "--resume",
        "--input", source,
        "--scene-detection-input", SPath(__file__).parent / "scripts" / "scene-detection-source.py",
        "--output-scenes", output_json.parent / "THIS_FILE_SHOULD_NOT_BE_GENERATED_KDLUIGSJ",
        "--output-json", output_json,
    ]
    subprocess.run(command, env=env, check=True)

def get_dynamic_detail_scenes(output_json):
    with output_json.open("r") as output_json_f:
        scenes = json.load(output_json_f)

    for i in range(len(scenes)):
        scenes[i] = tuple(scenes[i])

    return scenes

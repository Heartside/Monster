from copy import deepcopy
import json

def finalise_dynamic_detail_scenes(json_file, zones_file, source):
    with json_file.open("r") as json_f:
        scenes = json.load(json_f)

    json_scenes = deepcopy(scenes)
    zones_scenes = deepcopy(scenes)

    def add_to_scenes(scenes, start_frame, end_frame):
        for i, line in enumerate(scenes):
            if line[0] <= start_frame <= line[1] or \
               line[0] <= end_frame <= line[1]:
                line[0] = min(line[0], start_frame)
                line[1] = max(line[1], end_frame)
                break
            elif line[0] > start_frame:
                scenes.insert(i, [start_frame, end_frame])
                break

    if source.op_type == 1:
        add_to_scenes(json_scenes, source.op[0], source.op[0] + 857) # 1678, 2535
        add_to_scenes(json_scenes, source.op[0] + 1055, source.op[0] + 1535) # 2733, 3213
        add_to_scenes(json_scenes, source.op[0] + 1912, source.op[0] + 2042) # 3590, 3720
        add_to_scenes(json_scenes, source.op[0] + 2056, source.op[0] + 2085) # 3734, 3763

        add_to_scenes(zones_scenes, source.op[0] + 1288, source.op[0] + 1371) # 2966, 3049

    if source.ed_type == 1:
        add_to_scenes(json_scenes, source.ed[0], source.ed[1])

    with json_file.open("w") as json_f:
        json.dump(json_scenes, json_f)
    with zones_file.open("w") as zones_f:
        for line in zones_scenes:
            zones_f.write(f"{line[0]} {line[1]} grain\n")

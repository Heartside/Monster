#!/usr/bin/env fish

# $argv[1]: Episode number "01"
function boost
    set episode $argv[1]
    if test -z $episode
        set_color red ; echo "[boost] Episode number not provided." ; set_color normal
        return 126
    end

    set source_file "Intermediate/$episode.mp4"
    if begin test -z $source_file ; or not test -e $source_file ; end
        set_color red ; echo "[boost] Intermediate file not found." ; set_color normal
        return 126
    end
    set source_zones_file "Intermediate/$episode.zones.txt"
    if begin test -z $source_zones_file ; or not test -e $source_zones_file ; end
        set_color red ; echo "[boost] Zones file not found." ; set_color normal
        return 126
    end
    set source_ffindex_file "Temp/$episode.mp4.ffindex"

    set_color -o white ; echo "[boost] Boosting episode $episode..." ; set_color normal

    set temp_dir_boost "Temp/$episode.boost.tmp"
    set scenes_file "Temp/$episode.scenes.json"
    set roi_maps_dir "Temp/$episode.roi-maps"
    LOCAL_SOURCE_FILE=$local_source_file SOURCE_FFINDEX_FILE=$source_ffindex_file python x86-boost.py --temp $temp_dir_boost --resume --input $source_file --input-ffindex $source_ffindex_file --scene-detection-input source.py --encode-input source.py --zones $source_zones_file --output-scenes $scenes_file --output-roi-maps $roi_maps_dir
    or return $status

    if begin test -z $scenes_file ; or not test -e $scenes_file ; end
        set_color red ; echo "[boost] Scenes file not found." ; set_color normal
        return 126
    end

    if begin test -z $roi_maps_dir ; or not test -e $roi_maps_dir ; end
        set_color red ; echo "[boost] ROI map directory not found." ; set_color normal
        return 126
    end
end

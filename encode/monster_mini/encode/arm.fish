#!/usr/bin/env fish

# $argv[1]: Episode number "01"
function boost
    set episode $argv[1]
    if test -z $episode
        set_color red ; echo "[boost] Episode number not provided." ; set_color normal
        return 126
    end

    if begin test -z $local ; or not test -e $local ; end
        set_color red ; echo "[boost] \$local not found." ; set_color normal
        return 126
    end

    set source_file "Intermediate/$episode.mp4"
    if begin test -z $source_file ; or not test -e $source_file ; end
        set_color red ; echo "[boost] Intermediate file not found." ; set_color normal
        return 126
    end
    set source_ffindex_file "Temp/$episode.mp4.ffindex"

    set_color -o white ; echo "[boost] Boosting episode $episode..." ; set_color normal

    set local_source_file "$local/Intermediate/$episode.mp4"
    rsync -u --progress $source_file $local_source_file
    or return $status
    set local_source_ffindex_file "$local/Temp/$episode.mp4.ffindex"

    SOURCE_FILE=$local_source_file SOURCE_FFINDEX_FILE=$source_ffindex_file python arm-boost.py
    or return $status

    set scenes_file "Temp/$episode.scenes.json"
    if begin test -z $scenes_file ; or not test -e $scenes_file ; end
        set_color red ; echo "[boost] Scenes file not found." ; set_color normal
        return 126
    end
    set local_scenes_file "$local/Temp/$episode.scenes.json"
    rsync -u --progress $scenes_file $local_scenes_file
    or return $status

    set roi_maps_dir "Temp/$episode.roi-maps"
    if begin test -z $roi_maps_dir ; or not test -e $roi_maps_dir ; end
        set_color red ; echo "[boost] ROI map directory not found." ; set_color normal
        return 126
    end
    set local_roi_maps_dir "$local/Temp/$episode.roi-maps"
    rsync -u --progress $roi_maps_dir $local_roi_maps_dir
    or return $status
    
    rsync -u --progress $source_ffindex_file $local_source_ffindex_file
    or return $status
end

# $argv[1]: Episode number "01"
function copy_encode
    set episode $argv[1]
    if test -z $episode
        set_color red ; echo "[copy_encode] Episode number not provided." ; set_color normal
        return 126
    end

    if begin test -z $local ; or not test -e $local ; end
        set_color red ; echo "[copy_encode] \$local not found." ; set_color normal
        return 126
    end

    set local_video_file "$local/Video/$episode.mkv"
    if begin test -z $local_video_file ; or not test -e $local_video_file ; end
        set_color red ; echo "[copy_encode] Local video file not found." ; set_color normal
        return 126
    end

    set_color -o white ; echo "[copy_encode] Copying episode $episode..." ; set_color normal

    set video_file "Video/$episode.mkv"
    rsync -u --progress $local_video_file $video_file
    or return $status
end

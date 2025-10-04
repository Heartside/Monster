#!/usr/bin/env fish

# $argv[1]: Episode number "01"
# $argv[2]: Workers "3"
function encode
    set episode $argv[1]
    if test -z $episode
        set_color red ; echo "[encode] Episode number not provided." ; set_color normal
        return 126
    end

    set workers $argv[2]
    if test -z $workers
        set workers 3
    end

    set source_file "Intermediate/$episode.mp4"
    if begin test -z $source_file ; or not test -e $source_file ; end
        set_color red ; echo "[encode] Intermediate file not found." ; set_color normal
        return 126
    end
    set source_ffindex_file "Temp/$episode.mp4.ffindex"

    set scenes_file "Temp/$episode.scenes.json"
    if begin test -z $scenes_file ; or not test -e $scenes_file ; end
        set_color red ; echo "[encode] Scenes file not found." ; set_color normal
        return 126
    end

    set_color -o white ; echo "[encode] Encoding episode $episode..." ; set_color normal

    set video_file "Video/$episode.mkv"
    if test -e $video_file
        set_color -o yellow ; echo "[encode] Target video file already exists. Continuing..." ; set_color normal
    end
    set temp_dir "Temp/$episode.tmp"
    if test -e $temp_dir
        set_color -o yellow ; echo "[encode] Temp dir already exists. Continuing..." ; set_color normal
    end
    SOURCE_FILE=$source_file SOURCE_FFINDEX_FILE=$source_ffindex_file av1an -y --max-tries 5 --temp $temp_dir --resume --keep --verbose --log-level debug -i arm-local-source.py -o $video_file --scenes $scenes_file --chunk-order random --chunk-method ffms2 --workers $workers --encoder svt-av1 --no-defaults --video-params "[1;5m:Hanabana:[0m" --pix-format yuv420p10le --concat mkvmerge
    or return $status

    if not test -e $video_file
        set_color red ; echo "[encode] Encoded video file missing. Exiting..." ; set_color normal
        return 126
    end
end

## Recommended prerequisites

- VapourSynth v72 (older versions are probably fine).
- uv (but pip could work as well).

## Sources

CR WEB-DL should be renamed to `01 (CR).mkv`. AMZN WEB-DL should be renamed to
`01 (AMZN).mkv`. (Replace `01` with the respective episode number.) These should
all exist within the same folder somewhere.

Create a `.env` file within this `encode` directory with the following
content:

```
RAWS_DIRECTORY="/path/to/raws"
```

Replace `/path/to/raws` with the path to the folder containing the video/audio
sources. Note that on Windows, any backslashes must be escaped
(so, `C:\path\to\raws` becomes `"C:\\path\\to\\raws"`).

## Usage

Preview an episode:

```shell
uv run --env-file .env vspreview 01.py
```

Run an encode:

```shell
uv run --env-file .env 01.py
```

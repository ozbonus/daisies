from pathlib import Path
from typing import NamedTuple

from dialog_script import DialogScript
from elevenlabs_client import DialogResponse


class LineTiming(NamedTuple):
    start: int
    end: int


class OutputWriter:
    """
    A class that handles writing JSON scripts and audio files that are
    compatible with Kantan Player apps.
    """

    def __init__(
        self,
        write_dir: Path,
        input_script: DialogScript,
        response: DialogResponse,
    ):
        self.write_dir = write_dir
        self.input_script = input_script
        self.response = response
        self.audio_write_path = write_dir / f"{input_script.stem}.mp3"
        self.script_write_path = write_dir / f"{input_script.stem}.json"

    def _build_output_script(self) -> dict:
        language_code = self.input_script.language_code
        country_code = self.input_script.country_code
        input_lines = self.input_script.lines
        timings = [
            LineTiming(
                # Timing must be in whole milliseconds.
                int(segment.start_time_seconds * 1000),
                int(segment.end_time_seconds * 1000),
            )
            for segment in self.response.segments
        ]
        script = {
            "locale": {
                "languageCode": language_code,
                **({"countryCode": country_code} if country_code else {}),
            },
            "lines": [
                {
                    "startTime": timing.start,
                    "endTime": timing.end,
                    "speaker": line.speaker,
                    "text": line.text,
                }
                for line, timing in zip(input_lines, timings)
            ],
        }
        return script

    def write_output_script(self) -> None:
        pass

    def write_audio(self) -> None:
        pass

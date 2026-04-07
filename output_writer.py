from pathlib import Path

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

    def _build_output_script(self) -> None:
        language_code = self.input_script.language_code
        country_code = self.input_script.country_code
        input_lines = self.input_script.lines
        timings = [
            (segment.start_time_seconds, segment.end_time_seconds)
            for segment in self.response.segments
        ]

    def write_output_script(self) -> None:
        pass

    def write_audio(self) -> None:
        pass

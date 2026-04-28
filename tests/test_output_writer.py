import json
from pathlib import Path

from jsonschema import ValidationError
import mutagen
from mutagen.mp3 import MP3
import pytest
from pytest import FixtureRequest
from mutagen._file import File

from dialog_script import DialogScript
from elevenlabs_client import DialogResponse
from json_schema import OUTPUT
from output_writer import LineTiming, OutputWriter
from tests.helpers import (
    COUNTRY_CODE,
    END_TIME_1,
    END_TIME_2,
    LANGUAGE_CODE,
    OMIT,
    SPEAKER_1,
    SPEAKER_2,
    START_TIME_1,
    START_TIME_2,
    TEXT_1,
    TEXT_2,
    make_output_script,
)


def test_line_timing() -> None:
    timing = LineTiming(0, 100)
    assert timing.start == 0
    assert timing.end == 100


@pytest.mark.parametrize(
    "script_fixture",
    [
        "dialog_script_complete_script",
        "dialog_script_no_country_code",
        "dialog_script_no_first_speaker",
    ],
)
def test_init(
    write_dir: Path,
    script_fixture: str,
    dialog_response: DialogResponse,
    request: FixtureRequest,
) -> None:
    script: DialogScript = request.getfixturevalue(script_fixture)
    writer = OutputWriter(
        write_dir=write_dir, input_script=script, response=dialog_response
    )
    stem = script.stem
    assert writer is not None
    assert writer.audio_write_path == write_dir / f"{stem}.mp3"
    assert writer.script_write_path == write_dir / f"{stem}.json"


@pytest.mark.parametrize(
    "script_fixture",
    [
        "dialog_script_complete_script",
        "dialog_script_no_country_code",
        "dialog_script_no_first_speaker",
    ],
)
def test_build_script(
    write_dir: Path,
    script_fixture: str,
    dialog_response: DialogResponse,
    request: FixtureRequest,
) -> None:
    input_script: DialogScript = request.getfixturevalue(script_fixture)
    segments = dialog_response.segments
    writer = OutputWriter(
        write_dir=write_dir, input_script=input_script, response=dialog_response
    )
    output_script = writer._build_output_script()
    assert output_script["locale"]["languageCode"] == input_script.language_code
    assert output_script["locale"].get("countryCode") == input_script.country_code
    for index, line in enumerate(output_script["lines"]):
        assert line["startTime"] == int(segments[index].start_time_seconds * 1000)
        assert line["endTime"] == int(segments[index].end_time_seconds * 1000)
        assert line.get("speaker") == input_script.lines[index].speaker
        assert line["text"] == input_script.lines[index].text


class TestOutputScriptValidation:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        write_dir: Path,
        dialog_script_complete_script: DialogScript,
        dialog_response: DialogResponse,
    ) -> None:
        self.writer = OutputWriter(
            write_dir=write_dir,
            input_script=dialog_script_complete_script,
            response=dialog_response,
        )

    def test_script_maker_helper(self) -> None:
        script = make_output_script()
        assert script["locale"]["languageCode"] == LANGUAGE_CODE
        assert script["locale"]["countryCode"] == COUNTRY_CODE
        assert script["lines"][0]["startTime"] == START_TIME_1
        assert script["lines"][0]["endTime"] == END_TIME_1
        assert script["lines"][0]["speaker"] == SPEAKER_1
        assert script["lines"][0]["text"] == TEXT_1
        assert script["lines"][1]["startTime"] == START_TIME_2
        assert script["lines"][1]["endTime"] == END_TIME_2
        assert script["lines"][1]["speaker"] == SPEAKER_2
        assert script["lines"][1]["text"] == TEXT_2

    def test_validate_complete_script(self) -> None:
        self.writer._validate_output_script(
            output_script=make_output_script(),
        )

    def test_no_country_code(self) -> None:
        self.writer._validate_output_script(
            output_script=make_output_script(
                country_code=OMIT,
            ),
        )

    def test_missing_one_timing(self) -> None:
        self.writer._validate_output_script(
            output_script=make_output_script(start_time_1=OMIT),
        )

    def test_no_timings(self) -> None:
        self.writer._validate_output_script(
            output_script=make_output_script(
                start_time_1=OMIT,
                start_time_2=OMIT,
                end_time_1=OMIT,
                end_time_2=OMIT,
            ),
        )

    def test_no_language_code(self) -> None:
        with pytest.raises(ValidationError):
            self.writer._validate_output_script(
                output_script=make_output_script(
                    language_code=OMIT,
                ),
            )

    def test_no_lines(self) -> None:
        output_script = make_output_script()
        output_script["lines"] = []
        with pytest.raises(ValidationError):
            self.writer._validate_output_script(
                output_script=output_script,
            )

    def test_no_speakers(self) -> None:
        with pytest.raises(ValidationError):
            self.writer._validate_output_script(
                output_script=make_output_script(
                    speaker_1=OMIT,
                    speaker_2=OMIT,
                ),
            )

    def test_no_text(self) -> None:
        with pytest.raises(ValidationError):
            self.writer._validate_output_script(
                output_script=make_output_script(
                    text_1=OMIT,
                    text_2=OMIT,
                ),
            )


class TestWriteOutputScript:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        write_dir: Path,
        dialog_script_complete_script: DialogScript,
        dialog_response: DialogResponse,
    ) -> None:
        self.writer = OutputWriter(
            write_dir=write_dir,
            input_script=dialog_script_complete_script,
            response=dialog_response,
        )
        self.writer.write_output_script()
        self.script_path = self.writer.script_write_path

    def test_write_file_to_path(self) -> None:
        assert self.script_path.exists()

    def test_file_contents(self) -> None:
        with open(self.script_path, encoding="utf-8") as file:
            data = json.load(file)
        assert data == self.writer.output_script


class TestWriteAudio:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        write_dir: Path,
        dialog_script_complete_script: DialogScript,
        dialog_response: DialogResponse,
    ) -> None:
        self.writer = OutputWriter(
            write_dir=write_dir,
            input_script=dialog_script_complete_script,
            response=dialog_response,
        )
        self.writer.write_audio()
        self.audio_path = self.writer.audio_write_path

    def test_write_file_to_path(self) -> None:
        assert self.audio_path.exists()

    def test_file_validity(self) -> None:
        file = File(self.audio_path)
        assert isinstance(file, MP3)

from pathlib import Path

import pytest
from pytest import FixtureRequest

from dialog_script import DialogScript
from elevenlabs_client import DialogResponse
from output_writer import LineTiming, OutputWriter
from tests.helpers import LANGUAGE_CODE, make_output_script


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

    def test_full_script(self) -> None:
        script = make_output_script()
        self.writer._validate_output_script(script)
        assert script["locale"]["languageCode"] == LANGUAGE_CODE

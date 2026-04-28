from json import JSONDecodeError
from pathlib import Path
from jsonschema import ValidationError
import pytest

from tests.helpers import (
    COUNTRY_CODE,
    LANGUAGE_CODE,
    SPEAKER_1,
    SPEAKER_2,
    TAGGED_TEXT_1,
    TEXT_1,
    TEXT_2,
    VOICE_ID_1,
    VOICE_ID_2,
)
from dialog_script import DialogScript


class TestDialogScriptLoadScript:
    def test_complete_script(
        self,
        sample_script_file: Path,
    ):
        script = DialogScript(sample_script_file)
        assert script is not None
        assert script.path == sample_script_file
        assert script.stem == sample_script_file.stem
        assert script.language_code == LANGUAGE_CODE
        assert script.country_code == COUNTRY_CODE

    def test_no_country_code(self, sample_script_file_no_country_code):
        script = DialogScript(sample_script_file_no_country_code)
        assert script is not None
        assert script.country_code is None

    def test_no_tagged_text(self, sample_script_file_no_tagged_text):
        script = DialogScript(sample_script_file_no_tagged_text)
        assert script is not None

    def test_invalid_json(self, sample_script_file_invalid_json):
        with pytest.raises(JSONDecodeError):
            DialogScript(sample_script_file_invalid_json)

    def test_schema_violation(self, sample_script_schema_violation):
        with pytest.raises(ValidationError):
            DialogScript(sample_script_schema_violation)

    def test_encoding_error(self, sample_script_encoding_error):
        with pytest.raises(UnicodeDecodeError):
            DialogScript(sample_script_encoding_error)


class TestDialogScriptVoicesMethod:
    def test_voices(
        self,
        sample_script_file,
    ):
        script = DialogScript(sample_script_file)
        voices = script.voices
        expected: set[str] = {VOICE_ID_1, VOICE_ID_2}
        assert voices == expected


class TestDialogScriptDialogInputsMethod:
    def test_dialog_inputs(self, sample_script_file, dialog_input_list):
        script = DialogScript(sample_script_file)
        inputs = script.dialog_inputs
        assert inputs == dialog_input_list

    def test_dialog_inputs_no_tagged_text(
        self,
        sample_script_file_no_tagged_text,
        dialog_input_list_no_tagged_text,
    ):
        script = DialogScript(sample_script_file_no_tagged_text)
        inputs = script.dialog_inputs
        assert inputs == dialog_input_list_no_tagged_text


class TestDialogScriptLinesProperty:
    def test_lines(
        self,
        sample_script_file,
    ):
        script = DialogScript(sample_script_file)
        lines = script.lines
        assert len(lines) == 2
        assert lines[0].speaker == SPEAKER_1
        assert lines[0].voice_id == VOICE_ID_1
        assert lines[0].text == TEXT_1
        assert lines[1].speaker == SPEAKER_2
        assert lines[1].voice_id == VOICE_ID_2
        assert lines[1].text == TEXT_2

    def test_lines_no_tagged_text(
        self,
        sample_script_file_no_tagged_text,
    ):
        script = DialogScript(sample_script_file_no_tagged_text)
        lines = script.lines
        assert len(lines) == 2
        assert lines[0].speaker == SPEAKER_1
        assert lines[0].voice_id == VOICE_ID_1
        assert lines[0].text == TEXT_1
        assert lines[1].speaker == SPEAKER_2
        assert lines[1].voice_id == VOICE_ID_2
        assert lines[1].text == TEXT_2

    def test_lines_no_speaker(
        self,
        sample_script_file_no_first_speaker,
    ):
        script = DialogScript(sample_script_file_no_first_speaker)
        lines = script.lines
        assert len(lines) == 2
        assert lines[0].speaker is None
        assert lines[0].voice_id == VOICE_ID_1
        assert lines[0].text == TEXT_1
        assert lines[1].speaker == SPEAKER_2
        assert lines[1].voice_id == VOICE_ID_2
        assert lines[1].text == TEXT_2

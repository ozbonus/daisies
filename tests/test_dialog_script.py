from json import JSONDecodeError
from pathlib import Path
from jsonschema import ValidationError
import pytest

from dialog_script import DialogScript


class TestDialogScriptLoadScript:
    def test_complete_script(
        self,
        sample_script_file: Path,
        script_language_code,
        script_country_code,
    ):
        script = DialogScript(sample_script_file)
        assert script is not None
        assert script.path == sample_script_file
        assert script.stem == sample_script_file.stem
        assert script.language_code == script_language_code
        assert script.country_code == script_country_code

    def test_no_country_code(self, sample_script_file_no_country_code):
        script = DialogScript(sample_script_file_no_country_code)
        assert script is not None
        assert script.country_code is None

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
        script_voice_id_1,
        script_voice_id_2,
    ):
        script = DialogScript(sample_script_file)
        voices = script.voices
        expected: set[str] = {script_voice_id_1, script_voice_id_2}
        assert voices == expected


class TestDialogScriptDialogInputsMethod:
    def test_dialog_inputs(self, sample_script_file, dialog_input_list):
        script = DialogScript(sample_script_file)
        inputs = script.dialog_inputs
        assert inputs == dialog_input_list


class TestDialogScriptLinesProperty:
    def test_lines(
        self,
        sample_script_file,
        script_speaker_1,
        script_voice_id_1,
        script_text_1,
        script_speaker_2,
        script_voice_id_2,
        script_text_2,
    ):
        script = DialogScript(sample_script_file)
        lines = script.lines
        assert len(lines) == 2
        assert lines[0].speaker == script_speaker_1
        assert lines[0].voice_id == script_voice_id_1
        assert lines[0].text == script_text_1
        assert lines[1].speaker == script_speaker_2
        assert lines[1].voice_id == script_voice_id_2
        assert lines[1].text == script_text_2

    def test_lines_no_speaker(
        self,
        sample_script_file_no_first_speaker,
        script_voice_id_1,
        script_text_1,
        script_speaker_2,
        script_voice_id_2,
        script_text_2,
    ):
        script = DialogScript(sample_script_file_no_first_speaker)
        lines = script.lines
        assert len(lines) == 2
        assert lines[0].speaker is None
        assert lines[0].voice_id == script_voice_id_1
        assert lines[0].text == script_text_1
        assert lines[1].speaker == script_speaker_2
        assert lines[1].voice_id == script_voice_id_2
        assert lines[1].text == script_text_2

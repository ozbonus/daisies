from json import JSONDecodeError
from elevenlabs import DialogueInput
from jsonschema import ValidationError
import pytest

from dialog_script import DialogScript


class TestDialogScriptLoadScript:
    def test_complete_script(
        self,
        sample_script_file,
        script_language_code,
        script_country_code,
    ):
        script = DialogScript(sample_script_file)
        assert script is not None
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
        voices = script.voices()
        expected: tuple[str, ...] = (script_voice_id_1, script_voice_id_2)
        assert voices == expected


class TestDialogScriptDialogInputsMethod:
    def test_dialog_inputs(self, sample_script_file, dialog_input_list):
        script = DialogScript(sample_script_file)
        inputs = script.dialog_inputs()
        assert inputs == dialog_input_list

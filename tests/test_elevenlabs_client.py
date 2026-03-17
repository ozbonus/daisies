import pytest
from elevenlabs_client import ElevenLabsClient, DialogResponse
from elevenlabs import DialogueInput, VoiceSegment
from elevenlabs.types import ModelSettingsResponseModel
from errors import (
    Base64DecodeError,
    ElevenLabsClientError,
    VoiceNotAvailableError,
)


class TestElevenLabsClientGetDialogSuccess:
    """
    Test the output of a successful get_dialog request.
    """

    @pytest.fixture(autouse=True)
    def setup(self, mock_elevenlabs_api, dialog_input_list):
        self.client = ElevenLabsClient(mock_elevenlabs_api)
        self.result = self.client.get_dialog(dialog_input_list)
        self.mock = mock_elevenlabs_api

    def test_api_called_with_correct_parameters(
        self,
        script_text_1: str,
        script_text_2: str,
        script_voice_id_1: str,
        script_voice_id_2: str,
    ):
        """Verify the API receives the expected configuration."""
        call_kwargs = (
            self.mock.text_to_dialogue.convert_with_timestamps.call_args.kwargs
        )

        # Verify API endpoint parameters.
        assert call_kwargs["model_id"] == "eleven_v3"
        assert call_kwargs["output_format"] == "mp3_44100_128"
        assert call_kwargs["language_code"] == "en"
        assert call_kwargs["apply_text_normalization"] == "auto"
        assert call_kwargs["pronunciation_dictionary_locators"] == []

        # Verify model settings.
        settings = call_kwargs["settings"]
        assert isinstance(settings, ModelSettingsResponseModel)
        assert settings.stability == 0.5

        # Verify input transformation.
        inputs = call_kwargs["inputs"]
        assert len(inputs) == 2
        assert all(isinstance(i, DialogueInput) for i in inputs)
        assert inputs[0].text == script_text_1
        assert inputs[0].voice_id == script_voice_id_1
        assert inputs[1].text == script_text_2
        assert inputs[1].voice_id == script_voice_id_2

    def test_api_is_called(self):
        """Verify that the API method was called once."""
        self.mock.text_to_dialogue.convert_with_timestamps.assert_called_once()

    def test_return_dialog_response(self):
        """Verify that the response is the correct type."""
        assert isinstance(self.result, DialogResponse)

    def test_audio_data_validity(self):
        """Verify that the audio data is the correct type."""
        assert isinstance(self.result.audio_data, bytes)

    def test_segments_structure(
        self,
        script_voice_id_1: str,
        script_voice_id_2: str,
    ):
        """Verify the structure and contents of the audio segments."""
        segments = self.result.segments

        # Test overall structure of the segments.
        assert isinstance(segments, list)
        assert len(segments) == 2
        assert all(isinstance(i, VoiceSegment) for i in segments)

        # Test the contents of each segment.
        assert self.result.segments[0].voice_id == script_voice_id_1
        assert self.result.segments[0].start_time_seconds == 0.0
        assert self.result.segments[0].end_time_seconds == 1.0
        assert self.result.segments[1].voice_id == script_voice_id_2
        assert self.result.segments[1].start_time_seconds == 1.0
        assert self.result.segments[1].end_time_seconds == 2.0


class TestElevenLabsClientError:
    """Test various scenarios when errors should be raised."""

    def test_raise_elevenlabs_client_error_on_unprocessable_input(
        self,
        sample_script,
        mock_api_unprocessable_entity_error,
    ):
        client = ElevenLabsClient(mock_api_unprocessable_entity_error)
        with pytest.raises(ElevenLabsClientError) as exception_info:
            client.get_dialog(sample_script)
        assert "Error location" in exception_info.value.msg
        assert "Error message" in exception_info.value.msg

    def test_raise_elevenlabs_client_error_on_unhandled_error(
        self,
        sample_script,
        mock_api_unhandled_error,
    ):
        client = ElevenLabsClient(mock_api_unhandled_error)
        with pytest.raises(ElevenLabsClientError) as exception_info:
            client.get_dialog(sample_script)
        assert "Unhandled API client error" in exception_info.value.msg

    def test_raise_base64_decode_error_on_value_error(
        self,
        sample_script,
        mock_elevenlabs_api_bad_audio,
        invalid_base64_audio_string,
    ):
        client = ElevenLabsClient(mock_elevenlabs_api_bad_audio)
        with pytest.raises(Base64DecodeError) as exception_info:
            client.get_dialog(sample_script)
        mock_elevenlabs_api_bad_audio.text_to_dialogue.convert_with_timestamps.assert_called_once()
        assert "Error decoding audio to bytes." in exception_info.value.msg


class TestElevenLabsClientVerifyVoices:
    """
    Tests for the `_verify_voices` method that confirms whether or not the
    user's API key may access all of the voices used in the script.
    """

    def test_voices_available(
        self,
        mock_elevenlabs_api,
        script_voice_id_1: str,
        script_voice_id_2: str,
    ):
        """
        All voices in the script are available to the user's API key. The method
        should not raise and error.
        """
        client = ElevenLabsClient(mock_elevenlabs_api)
        client.verify_voices([script_voice_id_1, script_voice_id_2])
        mock_elevenlabs_api.voices.get_all.assert_called_once()

    def test_voice_not_available(
        self,
        mock_elevenlabs_api,
        script_voice_id_3: str,
    ):
        """
        The script contains one voice that is not available to the user's API.
        Should raise a `VoiceNotAvailableError` and the error message should
        contain the offending voice ID.
        """
        client = ElevenLabsClient(mock_elevenlabs_api)
        with pytest.raises(VoiceNotAvailableError) as exception_info:
            client.verify_voices([script_voice_id_3])
        mock_elevenlabs_api.voices.get_all.assert_called_once()
        assert script_voice_id_3 in exception_info.value.msg

import pytest
from elevenlabs_client import ElevenLabsClient, DialogResponse
from elevenlabs import DialogueInput, VoiceSegment
from elevenlabs.types import ModelSettingsResponseModel
from errors import Base64DecodeError, ElevenLabsClientError, ScriptError


class TestElevenLabsClientMakeInputSequenceSuccess:
    """
    Test the method for generating an input sequence from a script.
    """

    @pytest.fixture(autouse=True)
    def setup(self, mock_elevenlabs_happy, sample_script):
        self.client = ElevenLabsClient(mock_elevenlabs_happy)
        self.result = self.client._make_input_sequence(sample_script)

    def test_is_list(self):
        assert isinstance(self.result, list)

    def test_elements_are_dialog_input(self):
        assert all(isinstance(i, DialogueInput) for i in self.result)

    def test_values(self):
        assert self.result[0].text == "[happily] How are you?"
        assert self.result[0].voice_id == "abc123"
        assert self.result[1].text == "[whispering] Fine, thank you."
        assert self.result[1].voice_id == "def456"


class TestElevenLabsClientMakeInputSequenceErrors:
    """
    Test `_make_input_sequence` with various faulty inputs.
    """

    @pytest.fixture(autouse=True)
    def setup(self, mock_elevenlabs_happy):
        self.client = ElevenLabsClient(mock_elevenlabs_happy)

    @pytest.mark.parametrize(
        "script, expected_key",
        [
            ([{"bad_key": "blah", "voice_id": "blah"}], "text"),  # Bad key.
            ([{"voice_id": "blah"}], "text"),  # Missing key.
            ([{"text": "blah"}], "voice_id"),  # Missing key.
            ([{}], "text"),  # Missing all keys.
        ],
    )
    def test_raise_script_error(self, script, expected_key):
        with pytest.raises(ScriptError) as exception:
            self.client._make_input_sequence(script)
        assert expected_key in str(exception.value.msg)


class TestElevenLabsClientGetDialogSuccess:
    """
    Test the output of a successful get_dialog request.
    """

    @pytest.fixture(autouse=True)
    def setup(self, mock_elevenlabs_happy, sample_script):
        self.client = ElevenLabsClient(mock_elevenlabs_happy)
        self.result = self.client.get_dialog(sample_script)
        self.mock = mock_elevenlabs_happy

    def test_api_called_with_correct_parameters(self):
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
        assert inputs[0].text == "[happily] How are you?"
        assert inputs[0].voice_id == "abc123"
        assert inputs[1].text == "[whispering] Fine, thank you."
        assert inputs[1].voice_id == "def456"

    def test_api_is_called(self):
        """Verify that the API method was called once."""
        self.mock.text_to_dialogue.convert_with_timestamps.assert_called_once()

    def test_return_dialog_response(self):
        """Verify that the response is the correct type."""
        assert isinstance(self.result, DialogResponse)

    def test_audio_data_validity(self):
        """Verify that the audio data is the correct type."""
        assert isinstance(self.result.audio_data, bytes)

    def test_segments_structure(self):
        """Verify the structure and contents of the audio segments."""
        segments = self.result.segments

        # Test overall structure of the segments.
        assert isinstance(segments, list)
        assert len(segments) == 2
        assert all(isinstance(i, VoiceSegment) for i in segments)

        # Test the contents of each segment.
        assert self.result.segments[0].voice_id == "abc123"
        assert self.result.segments[0].start_time_seconds == 0.0
        assert self.result.segments[0].end_time_seconds == 1.0
        assert self.result.segments[1].voice_id == "def456"
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
    ):
        client = ElevenLabsClient(mock_elevenlabs_api_bad_audio)
        with pytest.raises(Base64DecodeError) as exception_info:
            client.get_dialog(sample_script)
        assert "Error decoding audio to bytes." in exception_info.value.msg

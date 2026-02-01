from typing import List
import pytest
from elevenlabs_client import ElevenLabsClient, DialogResponse
from elevenlabs import DialogueInput, UnprocessableEntityError, VoiceSegment
from elevenlabs.types import ModelSettingsResponseModel
from errors import Base64DecodeError, ElevenLabsClientError





class TestElevenLabsClientGetDialogSuccess:
    """
    Test the output of a successful get_dialog request.
    """

    @pytest.fixture(autouse=True)
    def setup(self, mock_elevenlabs_happy, sample_script):
        self.client = ElevenLabsClient(mock_elevenlabs_happy)
        result = self.client.get_dialog(sample_script)
        assert isinstance(result, DialogResponse), (
            f"Expected DialogResponse, got {type(result)}"
        )
        self.result: DialogResponse = result

    def test_method_called(self, mock_elevenlabs_happy):
        mock_elevenlabs_happy.text_to_dialogue.convert_with_timestamps.assert_called_once()

    def test_response_type(self):
        assert isinstance(self.result, DialogResponse), (
            f"Expected DialogResponse, got {type(self.result)}"
        )

    def test_segments_length(self):
        assert len(self.result.segments) == 2

    def test_segments_is_list(self):
        assert isinstance(self.result.segments, List)

    def test_segments_are_voice_segments(self):
        assert all(isinstance(i, VoiceSegment) for i in self.result.segments)

    def test_segments_structure(self):
        assert self.result.segments[0].voice_id == "abc123"
        assert self.result.segments[0].start_time_seconds == 0.0
        assert self.result.segments[0].end_time_seconds == 1.0
        assert self.result.segments[1].voice_id == "def456"
        assert self.result.segments[1].start_time_seconds == 1.0
        assert self.result.segments[1].end_time_seconds == 2.0

    def test_audio_data_exists(self):
        assert len(self.result.audio_data) > 0

    def test_audio_data_is_bytes(self):
        assert isinstance(self.result.audio_data, bytes)


class TestElevenLabsClient:
    """
    Tests for the ElevenLabs client API wrapper.
    """

    def test_get_dialog_success(self, mock_elevenlabs_happy, sample_script):
        """Test successful dialogue generation with valid inputs."""
        client = ElevenLabsClient(mock_elevenlabs_happy)
        result = client.get_dialog(sample_script)

        # Assert the mock was called correctly.
        mock_elevenlabs_happy.text_to_dialogue.convert_with_timestamps.assert_called_once()

        # Assert result type and structure.
        assert isinstance(result, DialogResponse), (
            f"Expected DialogResponse, got {type(result)}"
        )
        assert not isinstance(result, (Base64DecodeError, ElevenLabsClientError))

        # Assert - verify audio data is correctly decoded
        assert isinstance(result.audio_data, bytes)
        assert len(result.audio_data) > 0

        # Assert - verify segments structure
        assert len(result.segments) == 2
        assert result.segments[0].voice_id == "abc123"
        assert result.segments[0].start_time_seconds == 0.0
        assert result.segments[0].end_time_seconds == 1.0
        assert result.segments[1].voice_id == "def456"
        assert result.segments[1].start_time_seconds == 1.0
        assert result.segments[1].end_time_seconds == 2.0

        # Verify call arguments
        call_args = (
            mock_elevenlabs_happy.text_to_dialogue.convert_with_timestamps.call_args
        )
        assert call_args.kwargs["model_id"] == "eleven_v3"
        assert call_args.kwargs["output_format"] == "mp3_44100_128"
        assert call_args.kwargs["language_code"] == "en"
        assert isinstance(call_args.kwargs["settings"], ModelSettingsResponseModel)
        assert call_args.kwargs["settings"].stability == 0.5

        # Verify inputs were correctly transformed
        inputs = call_args.kwargs["inputs"]
        assert len(inputs) == 2
        assert all(isinstance(inp, DialogueInput) for inp in inputs)
        assert inputs[0].text == "[happily] How are you?"
        assert inputs[0].voice_id == "abc123"
        assert inputs[1].text == "[whispering] Fine, thank you."
        assert inputs[1].voice_id == "def456"

    # def test_get_dialog_unprocessable_entity_error_with_detail(
    #     self,
    #     mock_elevenlabs_unprocessable_error_with_detail,
    #     sample_script,
    # ):
    #     """
    #     Test getting a 402 Unprocessable Entity Error.
    #     """

    #     # Setup
    #     client = ElevenLabsClient(
    #         client=mock_elevenlabs_unprocessable_error_with_detail
    #     )
    #     response = client.get_dialog(sample_script)

    #     # Assert the mocked method was called.
    #     mock_elevenlabs_unprocessable_error_with_detail.text_to_dialogue.convert_with_timestamps.assert_called_once()

    #     # Assert result type and structure.
    #     assert isinstance(response, UnprocessableEntityError)

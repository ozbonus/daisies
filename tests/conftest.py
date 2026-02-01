from elevenlabs import (
    AudioWithTimestampsAndVoiceSegmentsResponseModel,
    ElevenLabs,
    UnprocessableEntityError,
    VoiceSegment,
)
import pytest
from unittest.mock import MagicMock, patch
import os


@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict(os.environ, {"API_KEY": "FNORD123"}):
        yield


@pytest.fixture
def sample_script() -> list[dict[str, str]]:
    """A minimal dialog for testing."""
    return [
        {"text": "[happily] How are you?", "voice_id": "abc123"},
        {"text": "[whispering] Fine, thank you.", "voice_id": "def456"},
    ]


@pytest.fixture
def mock_elevenlabs_happy():
    mock = MagicMock(spec=ElevenLabs)

    mock_result = MagicMock(spec=AudioWithTimestampsAndVoiceSegmentsResponseModel)
    mock_result.audio_base_64 = "aGVsbG8egd29ybGQ"
    mock_result.voice_segments = [
        VoiceSegment(
            voice_id="abc123",
            start_time_seconds=0.0,
            end_time_seconds=1.0,
            character_start_index=0,
            character_end_index=1,
            dialogue_input_index=0,
        ),
        VoiceSegment(
            voice_id="def456",
            start_time_seconds=1.0,
            end_time_seconds=2.0,
            character_start_index=0,
            character_end_index=1,
            dialogue_input_index=1,
        ),
    ]

    mock.text_to_dialogue.convert_with_timestamps.return_value = mock_result

    return mock


@pytest.fixture
def mock_elevenlabs_unprocessable_error_with_detail():
    mock = MagicMock(spec=ElevenLabs)
    error = UnprocessableEntityError(body=MagicMock())
    error.body.detail = [
        MagicMock(
            loc="Error location",
            msg="Error message",
        )
    ]
    mock.text_to_dialogue.convert_with_timestamps.side_effect = error
    return mock

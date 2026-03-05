from elevenlabs import (
    AudioWithTimestampsAndVoiceSegmentsResponseModel,
    ElevenLabs,
    GetVoicesResponse,
    UnprocessableEntityError,
    Voice,
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
def script_language_code() -> str:
    return "eo"


@pytest.fixture
def script_country_code() -> str:
    return "AQ"


@pytest.fixture
def script_text_1() -> str:
    return "Blah blah."


@pytest.fixture
def script_text_2() -> str:
    return "Blah blah blah."


@pytest.fixture
def script_voice_id_1() -> str:
    return "abc123"


@pytest.fixture
def script_voice_id_2() -> str:
    return "def456"


@pytest.fixture
def script_voice_id_3() -> str:
    return "ghi789"


@pytest.fixture
def user_voice_1(script_voice_id_1: str) -> Voice:
    return Voice(voice_id=script_voice_id_1)


@pytest.fixture
def user_voice_2(script_voice_id_2: str) -> Voice:
    return Voice(voice_id=script_voice_id_2)


@pytest.fixture
def sample_script(
    script_text_1: str,
    script_text_2: str,
    script_voice_id_1: str,
    script_voice_id_2: str,
) -> dict[str, object]:
    """
    A minimal dialog for testing.
    """
    return {
        "languageCode": script_language_code,
        "countryCode": script_country_code,
        "lines": [
            {"text": script_text_1, "voice_id": script_voice_id_1},
            {"text": script_text_2, "voice_id": script_voice_id_2},
        ],
    }


@pytest.fixture
def sample_script_unavailable_voice(
    script_text_1: str,
    script_text_2: str,
    script_voice_id_2: str,
    script_voice_id_3: str,
) -> dict[str, object]:
    """
    This script contains a reference to a voice that is meant to be unavailable
    to the user account associated with the API key, `script_voice_id_3.
    """
    return {
        "languageCode": script_language_code,
        "countryCode": script_country_code,
        "lines": [
            {"text": script_text_1, "voice_id": script_voice_id_1},
            {"text": script_text_2, "voice_id": script_voice_id_3},
        ],
    }


@pytest.fixture
def invalid_base64_audio_string() -> str:
    """
    This is an invalid base-64 string because exclamation points are not within
    the set of ASCII characters that can be conventionally used to encode
    base-64.
    """
    return "!!!"


@pytest.fixture
def voice_segments(
    script_voice_id_1: str,
    script_voice_id_2: str,
) -> list[VoiceSegment]:
    """
    A mock list of voice segments to mimic a successful response.
    """
    return [
        VoiceSegment(
            voice_id=script_voice_id_1,
            start_time_seconds=0.0,
            end_time_seconds=1.0,
            character_start_index=0,
            character_end_index=1,
            dialogue_input_index=0,
        ),
        VoiceSegment(
            voice_id=script_voice_id_2,
            start_time_seconds=1.0,
            end_time_seconds=2.0,
            character_start_index=0,
            character_end_index=1,
            dialogue_input_index=1,
        ),
    ]


@pytest.fixture
def mock_elevenlabs_happy(
    voice_segments: list[VoiceSegment],
    user_voice_1: Voice,
    user_voice_2: Voice,
):
    """
    Mock a successful ElevenLabs API for happy path events.
    """
    mock = MagicMock(spec=ElevenLabs)

    # Mock a successful result of requesting a dialogue with timestamps.
    mock_get_dialogue_result = MagicMock(
        spec=AudioWithTimestampsAndVoiceSegmentsResponseModel
    )
    mock_get_dialogue_result.audio_base_64 = "aGVsbG8egd29ybGQ"
    mock_get_dialogue_result.voice_segments = voice_segments
    mock.text_to_dialogue.convert_with_timestamps.return_value = (
        mock_get_dialogue_result
    )

    # Mock a successful request for the voices available to the API key.
    mock_verify_voices_result = MagicMock(spec=GetVoicesResponse)
    mock_verify_voices_result.voices = [user_voice_1, user_voice_2]
    mock.voices.get_all.return_value = mock_verify_voices_result

    return mock


@pytest.fixture
def mock_api_unprocessable_entity_error():
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


@pytest.fixture
def mock_api_unhandled_error():
    """
    Unhandled errors should raise an `ElevenLabsClientError` when encountered
    within `ElevenlabsClient`.
    """
    mock = MagicMock(spec=ElevenLabs)
    error = Exception()
    mock.text_to_dialogue.convert_with_timestamps.side_effect = error
    return mock


@pytest.fixture
def mock_elevenlabs_api_bad_audio(
    invalid_base64_audio_string: str,
    voice_segments: list[VoiceSegment],
):
    mock = MagicMock(spec=ElevenLabs)
    mock_result = MagicMock(spec=AudioWithTimestampsAndVoiceSegmentsResponseModel)
    mock_result.audio_base_64 = invalid_base64_audio_string
    mock_result.voice_segments = voice_segments
    mock.text_to_dialogue.convert_with_timestamps.return_value = mock_result
    return mock

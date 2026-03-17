import base64
import binascii
import os
from dataclasses import dataclass

from dotenv import load_dotenv
from elevenlabs import (
    DialogueInput,
    GetVoicesResponse,
    UnprocessableEntityError,
)
from elevenlabs.client import ElevenLabs
from elevenlabs.types import ModelSettingsResponseModel, VoiceSegment
from errors import (
    Base64DecodeError,
    ElevenLabsClientError,
    VoiceNotAvailableError,
)


@dataclass
class DialogResponse:
    """
    A structured response from ElevenLabs' text-to-dialog API.
    """

    audio_data: bytes
    segments: list[VoiceSegment]


class ElevenLabsClient:
    """
    A wrapper for ElevenLabs text-to-dialog API.
    """

    def __init__(self, api: ElevenLabs):
        self.api = api

    def _str_to_bytes(self, data: str) -> bytes:
        return base64.b64decode(data, validate=True)

    def verify_voices(self, voice_ids: list[str]) -> None:
        """
        Verify that the user associated with the API key has access to all of
        the voices used in the script.

        Note that this application is made on a shoe string budget and assumes
        that the user's account is not of a level that can keep a large library
        of voices. As such, the page size, which is set the maximum value of
        100, should be more than large enough to get the full voice library of
        the user.

        Raises:
            VoiceNotAvailableError: One or more unavailable voices are used.
        """

        voices_query: GetVoicesResponse = self.api.voices.get_all()
        user_voices: list[str] = [voice.voice_id for voice in voices_query.voices]
        unavailable_voices = [v for v in voice_ids if v not in user_voices]

        if unavailable_voices:
            raise VoiceNotAvailableError(unavailable_voices)

    def get_dialog(self, inputs: list[DialogueInput]) -> DialogResponse:
        settings = ModelSettingsResponseModel(stability=0.5)

        try:
            result = self.api.text_to_dialogue.convert_with_timestamps(
                model_id="eleven_v3",
                settings=settings,
                output_format="mp3_44100_128",
                language_code="en",
                pronunciation_dictionary_locators=[],
                apply_text_normalization="auto",
                inputs=inputs,
            )
        except UnprocessableEntityError as error:
            if hasattr(error.body, "detail") and error.body.detail:
                error_message = error.body.detail[0].msg
                error_location = error.body.detail[0].loc
                msg = f"API error at {error_location}: {error_message}"
                raise ElevenLabsClientError(msg=msg)
            else:
                raise ElevenLabsClientError(msg="Unspecified API client error")
        except Exception:
            raise ElevenLabsClientError(msg="Unhandled API client error")

        try:
            audio_data = self._str_to_bytes(result.audio_base_64)
        except binascii.Error:
            raise Base64DecodeError()

        return DialogResponse(
            audio_data=audio_data,
            segments=result.voice_segments,
        )


load_dotenv()
api = ElevenLabs(
    base_url="https://api.elevenlabs.io",
    api_key=os.getenv("API_KEY"),
)
eleven_labs_client = ElevenLabsClient(api=api)

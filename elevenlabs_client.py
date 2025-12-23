import base64
import os
from dataclasses import dataclass
from typing import Dict, List

from dotenv import load_dotenv
from elevenlabs import DialogueInput
from elevenlabs.client import ElevenLabs
from elevenlabs.types import ModelSettingsResponseModel, VoiceSegment


@dataclass
class DialogResponse:
    """
    A structured response from ElevenLabs' text-to-dialog API.
    """

    audio_data: bytes
    segments: List[VoiceSegment]


class ElevenLabsClient:
    """
    A wrapper for ElevenLabs text-to-dialog API.
    """

    def __init__(self):
        load_dotenv()
        self.client = ElevenLabs(
            base_url="https://api.elevenlabs.io",
            api_key=os.getenv("API_KEY"),
        )

    @staticmethod
    def str_to_bytes(data: str) -> bytes:
        return base64.b64decode(data)

    def get_dialog(self, dialog: List[Dict[str, str]]) -> DialogResponse:
        dialog_input_sequence = [
            DialogueInput(text=line["text"], voice_id=line["voice_id"])
            for line in dialog
        ]

        settings = ModelSettingsResponseModel(
            stability=0.5,
        )

        result = self.client.text_to_dialogue.convert_with_timestamps(
            model_id="eleven_v3",
            settings=settings,
            output_format="mp3_44100_128",
            language_code="en",
            pronunciation_dictionary_locators=[],
            apply_text_normalization="auto",
            inputs=dialog_input_sequence,
        )

        audio_data = ElevenLabsClient.str_to_bytes(result.audio_base_64)

        return DialogResponse(
            audio_data=audio_data,
            segments=result.voice_segments,
        )

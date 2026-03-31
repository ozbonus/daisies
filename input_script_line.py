from dataclasses import dataclass


@dataclass
class InputScriptLine:
    speaker: str | None
    voice_id: str
    text: str
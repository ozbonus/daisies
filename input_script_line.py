from dataclasses import dataclass


@dataclass
class InputScriptLine:
    speaker: str | None
    voiceId: str
    text: str
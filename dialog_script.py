import json
from pathlib import Path
from elevenlabs import DialogueInput
from jsonschema import validate
from input_script_line import InputScriptLine
from json_schema import INPUT


class DialogScript:
    def __init__(self, file: Path):
        """
        Load and validate a JSON-formatted dialog script.

        Raises:
            JSONDecodeError: The file is not valid JSON.
            UnicodeDecodeError: Data is not encoded using UTF-8, UTF-16, UTF-32.
            ValidationError: The JSON doesn't follow the defined schema.
        """
        self.file = file
        with open(file) as f:
            self.data = json.load(f)
        validate(self.data, schema=INPUT)
        self.language_code = self.data["locale"]["languageCode"]
        self.country_code = self.data["locale"].get("countryCode")

    @property
    def path(self) -> Path:
        return self.file

    @property
    def stem(self) -> str:
        """
        The stem of the file path of the input script.
        """
        return self.file.stem

    @property
    def voices(self) -> set[str]:
        return {line["voiceId"] for line in self.data["lines"]}

    @property
    def dialog_inputs(self) -> list[DialogueInput]:
        return [
            DialogueInput(text=line["text"], voice_id=line["voiceId"])
            for line in self.data["lines"]
        ]

    @property
    def lines(self) -> list[InputScriptLine]:
        return [
            InputScriptLine(
                speaker=line.get("speaker"),
                voice_id=line["voiceId"],
                text=line["text"],
            )
            for line in self.data["lines"]
        ]

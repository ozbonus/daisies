class AudioDecodeError(Exception):
    def __init__(self):
        self.msg = "Error decoding audio."
        super().__init__(self.msg)


class ElevenLabsClientError(Exception):
    def __init__(self, msg: str):
        self.msg = msg
        super().__init__(msg)


class ScriptError(ValueError):
    def __init__(self, msg: str):
        self.msg = f"Script Error: {msg}"
        super().__init__(msg)


class ScriptKeyError(ValueError):
    def __init__(self, key: str):
        self.msg = f"The scripts is missing the key: {key}"


class VoiceNotAvailableError(ValueError):
    """
    Raised when the script contains voice IDs that are not available to the user
    account associated with the current API key.
    """

    def __init__(self, voice_ids: list[str]):
        self.voice_ids = voice_ids
        ids = ", ".join(voice_ids)
        self.msg = (
            "The following voice IDs are used in the script "
            "but are not available to the current API key: "
            f"{ids}"
        )
        super().__init__(self.msg)

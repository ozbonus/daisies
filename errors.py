class Base64DecodeError(ValueError):
    def __init__(self):
        self.msg = "Error decoding audio to bytes."


class ElevenLabsClientError(Exception):
    def __init__(self, msg: str):
        self.msg = msg
        super().__init__(msg)

INPUT = {
    "type": "object",
    "properties": {
        "locale": {
            "type": "object",
            "properties": {
                "languageCode": {"type": "string"},
                "countryCode": {"type": "string"},
            },
            "required": ["languageCode"],
            "additionalProperties": False,
        },
        "lines": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "speaker": {"type": "string"},
                    "voiceId": {"type": "string"},
                },
                "required": ["text", "speaker", "voiceId"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["locale", "lines"],
    "additionalProperties": False,
}

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

OUTPUT = {
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
                    "startTime": {"type": "integer"},
                    "endTime": {"type": "integer"},
                    "speaker": {"type": ["string", "null"]},
                    "text": {"type": "string"},
                },
                "required": ["speaker", "text"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["locale", "lines"],
    "additionalProperties": False,
}

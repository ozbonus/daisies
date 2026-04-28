# Sentinel used to omit a key-value pair from a dict during unit tests.
import base64


OMIT = object()

LANGUAGE_CODE = "eo"
COUNTRY_CODE = "AQ"
START_TIME_1 = 0
START_TIME_2 = 1000
END_TIME_1 = 1000
END_TIME_2 = 2000
TEXT_1 = "Blah blah."
TEXT_2 = "Blah blah blah."
TAGGED_TEXT_1 = "[happily] Blah blah."
TAGGED_TEXT_2 = "[mildly vexed] Blah blah blah."
SPEAKER_1 = "Gandalf"
SPEAKER_2 = "Bilbo"
VOICE_ID_1 = "abc123"
VOICE_ID_2 = "def456"
VOICE_ID_3 = "ghi789"

mp3_bytes = base64.b64decode(
    "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU2LjM2LjEwMAAAAAAAAAAAAAAA//OEAAAAAAAAAAAAAAAAAAAAAAAASW5mbwAAAA8AAAAEAAABIADAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDV1dXV1dXV1dXV1dXV1dXV1dXV1dXV1dXV6urq6urq6urq6urq6urq6urq6urq6urq6v////////////////////////////////8AAAAATGF2YzU2LjQxAAAAAAAAAAAAAAAAJAAAAAAAAAAAASDs90hvAAAAAAAAAAAAAAAAAAAA//MUZAAAAAGkAAAAAAAAA0gAAAAATEFN//MUZAMAAAGkAAAAAAAAA0gAAAAARTMu//MUZAYAAAGkAAAAAAAAA0gAAAAAOTku//MUZAkAAAGkAAAAAAAAA0gAAAAANVVV"
)


def make_output_script(
    *,
    language_code: str | object = LANGUAGE_CODE,
    country_code: str | object = COUNTRY_CODE,
    start_time_1: int | object = START_TIME_1,
    start_time_2: int | object = START_TIME_2,
    end_time_1: int | object = END_TIME_1,
    end_time_2: int | object = END_TIME_2,
    speaker_1: str | object = SPEAKER_1,
    speaker_2: str | object = SPEAKER_2,
    text_1: str | object = TEXT_1,
    text_2: str | object = TEXT_2,
) -> dict:
    def _strip(d: dict) -> dict:
        return {k: v for k, v in d.items() if v is not OMIT}

    return {
        "locale": _strip(
            {
                "languageCode": language_code,
                "countryCode": country_code,
            }
        ),
        "lines": [
            _strip(
                {
                    "startTime": start_time_1,
                    "endTime": end_time_1,
                    "speaker": speaker_1,
                    "text": text_1,
                }
            ),
            _strip(
                {
                    "startTime": start_time_2,
                    "endTime": end_time_2,
                    "speaker": speaker_2,
                    "text": text_2,
                }
            ),
        ],
    }

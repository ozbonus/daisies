from tests.helpers import SPEAKER_1, TEXT_1, VOICE_ID_1
from input_script_line import InputScriptLine


def test_all_properties():
    line = InputScriptLine(
        speaker=SPEAKER_1,
        voice_id=VOICE_ID_1,
        text=TEXT_1,
    )
    assert line.speaker == SPEAKER_1
    assert line.voice_id == VOICE_ID_1
    assert line.text == TEXT_1


def test_null_speaker():
    line = InputScriptLine(
        # Mimic an expression used by the DialogScript.lines property.
        speaker={}.get("speaker"),
        voice_id=VOICE_ID_1,
        text=TEXT_1,
    )
    assert line.speaker is None
    assert line.voice_id == VOICE_ID_1
    assert line.text == TEXT_1

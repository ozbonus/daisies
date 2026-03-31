from input_script_line import InputScriptLine


def test_all_properties(
    script_speaker_1: str,
    script_voice_id_1: str,
    script_text_1: str,
):
    line = InputScriptLine(
        speaker=script_speaker_1,
        voice_id=script_voice_id_1,
        text=script_text_1,
    )
    assert line.speaker == script_speaker_1
    assert line.voice_id == script_voice_id_1
    assert line.text == script_text_1


def test_null_speaker(
    script_voice_id_1: str,
    script_text_1: str,
):
    line = InputScriptLine(
        # Mimic an expression used by the DialogScript.lines property.
        speaker={}.get("speaker"),
        voice_id=script_voice_id_1,
        text=script_text_1,
    )
    assert line.speaker is None
    assert line.voice_id == script_voice_id_1
    assert line.text == script_text_1

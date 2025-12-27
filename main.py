from pathlib import Path
from elevenlabs_client import eleven_labs_client, DialogResponse



def write_audio(
    dialog_response: DialogResponse,
    output_filename: str = "output.mp3",
) -> Path:
    output_path = Path(__file__).parent / output_filename
    output_path.write_bytes(dialog_response.audio_data)
    return output_path


def write_segments():
    pass


def main():
    inputs = [
        {
            "text": "[meows] I am a cat.",
            "voice_id": "BIvP0GN1cAtSRTxNHnWS",
        },
        {
            "text": "[high pitched] Tweet tweet! I am a bird.",
            "voice_id": "kmSVBPu7loj4ayNinwWM",
        },
    ]

    response = eleven_labs_client.get_dialog(inputs)
    if response is DialogResponse:
        write_audio(response)


if __name__ == "__main__":
    main()

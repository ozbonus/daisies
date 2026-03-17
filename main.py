import os
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
from elevenlabs_client import ElevenLabsClient


def write_audio():
    pass


def write_segments():
    pass


def main():
    load_dotenv()
    api = ElevenLabs(
        base_url="https://api.elevenlabs.io",
        api_key=os.getenv("API_KEY"),
    )
    client = ElevenLabsClient(api=api)


if __name__ == "__main__":
    main()

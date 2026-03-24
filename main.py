from dataclasses import dataclass
import os
import argparse
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs import ElevenLabs
from dialog_script import DialogScript
from elevenlabs_client import ElevenLabsClient


def parse_args() -> list[Path]:
    parser = argparse.ArgumentParser(
        prog="daisies",
        description="A utility for generating audio and timestamps from text dialog scripts.",
        epilog="Examples:\n  daisies ./scripts\n  daisies ./scripts/dialog.json",
    )

    parser.add_argument(
        "input", type=Path, help="A JSON script or directory that contains JSON scripts"
    )

    args = parser.parse_args()
    path: Path = args.input

    if not path.exists():
        parser.error(f"Not found: {path}")

    if path.is_file():
        if path.suffix.lower() != ".json":
            parser.error(f"Expected JSON file, but got: {path}")
        return [path]
    elif path.is_dir():
        scripts = list({*path.glob("*.json"), *path.glob("*.JSON")})
        if not scripts:
            parser.error(f"No JSON files found in directory: {path}")
        return scripts
    else:
        parser.error(f"Input must be a file or directory, not: {path}")


def write_audio():
    pass


def write_segments():
    pass


def main():
    scripts = parse_args()
    load_dotenv()
    api = ElevenLabs(
        base_url="https://api.elevenlabs.io",
        api_key=os.getenv("API_KEY"),
    )
    
    for path in scripts:
        script = DialogScript(path)
        client = ElevenLabsClient(api=api)
        output = client.get_dialog(
            inputs=script.dialog_inputs()
        )

    


if __name__ == "__main__":
    main()

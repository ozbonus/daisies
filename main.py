import os
import argparse
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs import ElevenLabs
from dialog_script import DialogScript
from elevenlabs_client import ElevenLabsClient


def parse_args() -> tuple[list[Path], bool, Path]:
    parser = argparse.ArgumentParser(
        prog="daisies",
        description="A utility for generating audio and timestamps from text dialog scripts.",
        epilog="Examples:\n  daisies ./scripts\n  daisies ./scripts/dialog.json",
    )

    parser.add_argument(
        "input",
        type=Path,
        help="a JSON script or directory that contains JSON scripts",
    )

    parser.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        help="overwrite existing files",
    )

    args = parser.parse_args()
    path: Path = args.input
    overwrite: bool = args.overwrite

    if not path.exists():
        parser.error(f"Not found: {path}")

    if path.is_file():
        if path.suffix.lower() != ".json":
            parser.error(f"Expected JSON file, but got: {path}")
        write_dir = path.parent / "output"
        scripts = [path]
    elif path.is_dir():
        scripts = list({*path.glob("*.json"), *path.glob("*.JSON")})
        if not scripts:
            parser.error(f"No JSON files found in directory: {path}")
        write_dir = path / "output"
    else:
        parser.error(f"Input must be a file or directory, not: {path}")

    if not os.access(write_dir.parent, os.W_OK):
        parser.error(f"No write permission in directory: {write_dir.parent}")

    return scripts, overwrite, write_dir


def decide_files_to_write(
    inputs: list[Path],
    overwrite: bool,
    write_dir: Path,
) -> list[Path]:
    if overwrite or not write_dir.exists():
        return inputs
    existing_stems = {file.stem for file in write_dir.iterdir()}
    return [path for path in inputs if path.stem not in existing_stems]


def write_audio():
    pass


def write_segments():
    pass


def main():
    inputs, overwrite, write_dir = parse_args()
    load_dotenv()
    api = ElevenLabs(
        base_url="https://api.elevenlabs.io",
        api_key=os.getenv("API_KEY"),
    )

    client = ElevenLabsClient(api)
    scripts = decide_files_to_write(
        inputs=inputs,
        overwrite=overwrite,
        write_dir=write_dir,
    )
    dialog_scripts = [DialogScript(path) for path in scripts]
    client.verify_voices(
        list(
            {voice for script in dialog_scripts for voice in script.voices},
        )
    )

    for script in dialog_scripts:
        output = client.get_dialog(inputs=script.dialog_inputs)
        print(output.segments)


if __name__ == "__main__":
    main()

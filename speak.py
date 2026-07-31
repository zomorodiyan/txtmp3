#!/usr/bin/env python3
"""CLI for Google Cloud Text-to-Speech: give it text, get an MP3."""

from __future__ import annotations

import argparse
import os
import sys

from google.cloud import texttospeech


def _read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_text(args: argparse.Namespace) -> tuple[str, str | None]:
    """Return (text, source_path). source_path is set when the text came
    from a file, so the caller can derive a matching default output name."""
    if args.file:
        return _read_file(args.file), args.file
    if len(args.text) == 1 and os.path.isfile(args.text[0]):
        return _read_file(args.text[0]), args.text[0]
    if args.text:
        return " ".join(args.text), None
    if not sys.stdin.isatty():
        return sys.stdin.read(), None
    print("Enter text to speak. Press Ctrl+Z then Enter when done:")
    return sys.stdin.read(), None


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert text to speech using Google Cloud TTS.")
    parser.add_argument(
        "text",
        nargs="*",
        help="Text to speak, or a path to a text file. If omitted, reads from --file, stdin, or a prompt.",
    )
    parser.add_argument(
        "-o", "--output", help="Output MP3 file path (default: same name as the input file, otherwise output.mp3)"
    )
    parser.add_argument("-f", "--file", help="Read text from a file instead of the command line")
    parser.add_argument("--voice", default="en-US-Standard-D", help="Google TTS voice name (default: en-US-Standard-D)")
    parser.add_argument("--language", default=None, help="Language code, e.g. en-US (default: derived from --voice)")
    parser.add_argument("--rate", type=float, default=1.0, help="Speaking rate, 0.25-4.0 (default: 1.0)")
    parser.add_argument("--pitch", type=float, default=0.0, help="Pitch, -20.0 to 20.0 semitones (default: 0.0)")
    parser.add_argument("--creds", help="Path to service account JSON key (overrides GOOGLE_APPLICATION_CREDENTIALS)")
    parser.add_argument("--play", action="store_true", help="Play the audio after saving")
    args = parser.parse_args()

    if args.creds:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = args.creds

    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        sys.exit(
            "No credentials found. Set the GOOGLE_APPLICATION_CREDENTIALS environment "
            "variable to your service account JSON key path, or pass --creds <path>."
        )

    text, source_path = get_text(args)
    text = text.strip()
    if not text:
        sys.exit("No text provided.")

    output = args.output or (os.path.splitext(source_path)[0] + ".mp3" if source_path else "output.mp3")

    language_code = args.language or "-".join(args.voice.split("-")[:2])

    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code=language_code, name=args.voice)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=args.rate,
        pitch=args.pitch,
    )

    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    with open(output, "wb") as f:
        f.write(response.audio_content)

    print(f"Saved: {output}")

    if args.play:
        os.startfile(output)


if __name__ == "__main__":
    main()

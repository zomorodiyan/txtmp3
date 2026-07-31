#!/usr/bin/env python3
"""CLI for Google Cloud Text-to-Speech: give it text, get an MP3."""

import argparse
import os
import sys

from google.cloud import texttospeech


def get_text(args: argparse.Namespace) -> str:
    if args.text:
        return " ".join(args.text)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return f.read()
    if not sys.stdin.isatty():
        return sys.stdin.read()
    print("Enter text to speak. Press Ctrl+Z then Enter when done:")
    return sys.stdin.read()


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert text to speech using Google Cloud TTS.")
    parser.add_argument("text", nargs="*", help="Text to speak. If omitted, reads from --file, stdin, or a prompt.")
    parser.add_argument("-o", "--output", default="output.mp3", help="Output MP3 file path (default: output.mp3)")
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

    text = get_text(args).strip()
    if not text:
        sys.exit("No text provided.")

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

    with open(args.output, "wb") as f:
        f.write(response.audio_content)

    print(f"Saved: {args.output}")

    if args.play:
        os.startfile(args.output)


if __name__ == "__main__":
    main()

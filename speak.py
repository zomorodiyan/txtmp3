#!/usr/bin/env python3
"""CLI for Google Cloud Text-to-Speech: give it text, get an MP3."""

from __future__ import annotations

import argparse
import os
import re
import sys

from google.cloud import texttospeech

# Google Cloud TTS's synchronous API hard-limits input to 5,000 UTF-8 bytes
# per request. Chunk a bit under that so boundary edge cases never trip it.
MAX_CHUNK_BYTES = 4800

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def _read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _split_long_segment(segment: str, max_bytes: int) -> list[str]:
    """Hard-split a segment with no sentence breaks (e.g. one huge run-on
    sentence) on whitespace, as a last resort."""
    pieces = []
    current = ""
    for word in segment.split(" "):
        candidate = f"{current} {word}".strip() if current else word
        if len(candidate.encode("utf-8")) <= max_bytes:
            current = candidate
            continue
        if current:
            pieces.append(current)
            current = ""
        if len(word.encode("utf-8")) <= max_bytes:
            current = word
            continue
        # A single "word" is itself too large (e.g. no spaces at all) - cut by raw bytes.
        encoded = word.encode("utf-8")
        for i in range(0, len(encoded), max_bytes):
            pieces.append(encoded[i : i + max_bytes].decode("utf-8", errors="ignore"))
    if current:
        pieces.append(current)
    return pieces


def split_into_chunks(text: str, max_bytes: int = MAX_CHUNK_BYTES) -> list[str]:
    """Split text into pieces that each fit within max_bytes of UTF-8, preferring
    paragraph and sentence boundaries over mid-word cuts, and packing multiple
    sentences per chunk to keep the number of API calls (and audio seams) low."""
    if len(text.encode("utf-8")) <= max_bytes:
        return [text]

    segments = []
    for paragraph in re.split(r"\n\s*\n", text):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        if len(paragraph.encode("utf-8")) <= max_bytes:
            segments.append(paragraph)
            continue
        for sentence in _SENTENCE_SPLIT_RE.split(paragraph):
            sentence = sentence.strip()
            if not sentence:
                continue
            if len(sentence.encode("utf-8")) <= max_bytes:
                segments.append(sentence)
            else:
                segments.extend(_split_long_segment(sentence, max_bytes))

    chunks = []
    current = ""
    for segment in segments:
        candidate = f"{current} {segment}".strip() if current else segment
        if len(candidate.encode("utf-8")) <= max_bytes:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = segment
    if current:
        chunks.append(current)
    return chunks


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
    voice = texttospeech.VoiceSelectionParams(language_code=language_code, name=args.voice)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=args.rate,
        pitch=args.pitch,
    )

    chunks = split_into_chunks(text)

    audio_parts = []
    for i, chunk in enumerate(chunks, start=1):
        if len(chunks) > 1:
            print(f"Synthesizing chunk {i}/{len(chunks)}...")
        synthesis_input = texttospeech.SynthesisInput(text=chunk)
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        audio_parts.append(response.audio_content)

    with open(output, "wb") as f:
        for part in audio_parts:
            f.write(part)

    print(f"Saved: {output}")

    if args.play:
        os.startfile(output)


if __name__ == "__main__":
    main()

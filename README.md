# mp3

Turn a text file into speech with one command:

```
mp3 notes.txt
```

That's it — it creates `notes.mp3` in the same folder, using Google
Cloud Text-to-Speech. Long text is split into chunks automatically
(Google's API caps each request at 5,000 bytes) and stitched back
into one MP3.

Try it on a bundled sample: `mp3 samples/octopus-intelligence.txt`

## Setup

1. [Create a Google Cloud project](https://console.cloud.google.com/projectcreate) (needs [billing enabled](https://console.cloud.google.com/billing))
2. [Enable the Text-to-Speech API](https://console.cloud.google.com/apis/library/texttospeech.googleapis.com) for it
3. [Create a service account](https://console.cloud.google.com/iam-admin/serviceaccounts) → **Keys** → **Add key** → **JSON**, and download it
4. Install:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -e .
   ```
5. Point at your key:
   ```
   set GOOGLE_APPLICATION_CREDENTIALS=path\to\key.json
   ```
   (or pass `--creds path\to\key.json` on each run instead)

## Options

```
mp3 "Hello, world!"                  # speak literal text instead of a file
echo "Hello, world!" | mp3           # read text from stdin
mp3 notes.txt -o greeting.mp3        # choose the output path
mp3 notes.txt --play                 # play the audio after saving
mp3 notes.txt --creds key.json       # use a specific credentials file
```

| Flag             | Description                                                        |
| ---------------- | -------------------------------------------------------------------|
| `text`            | Text to speak, or a path to a text file (omit to read from `--file`, stdin, or a prompt) |
| `-o, --output`     | Output MP3 file path (default: same name as the input file, otherwise `output.mp3`) |
| `-f, --file`       | Read text from a file instead of the command line                  |
| `--voice`          | Google TTS voice name (default: `en-US-Standard-D`)                |
| `--language`       | Language code, e.g. `en-US` (default: derived from `--voice`)       |
| `--rate`           | Speaking rate, `0.25`–`4.0` (default: `1.0`)                        |
| `--pitch`          | Pitch, `-20.0` to `20.0` semitones (default: `0.0`)                 |
| `--creds`          | Path to a service account JSON key (overrides the env variable)     |
| `--play`           | Play the audio after saving                                         |

See the [Google Cloud TTS voice list](https://cloud.google.com/text-to-speech/docs/voices)
for available `--voice` names and languages.

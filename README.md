# mp3

Turn a text file into speech with one command:

```
mp3 notes.txt
```

That's it — it creates `notes.mp3` in the same folder, using Google
Cloud Text-to-Speech.

## Setup

1. Create and activate a virtual environment:

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install the tool into it:

   ```
   pip install -e .
   ```

3. Get a Google Cloud service account key (IAM & Admin > Service
   Accounts > Keys) for a project with the Text-to-Speech API enabled,
   and point the tool at it:

   ```
   set GOOGLE_APPLICATION_CREDENTIALS=path\to\your-key.json
   ```

   (or pass `--creds path\to\your-key.json` on each run instead).

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

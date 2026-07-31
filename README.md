# mp3

A command-line tool that converts text to speech using Google Cloud
Text-to-Speech and saves the result as an MP3 file.

## Requirements

- Python 3.8+
- A Google Cloud project with the Text-to-Speech API enabled
- A service account JSON key with access to that API

## Setup

1. Create and activate a virtual environment:

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Get a service account key from Google Cloud (IAM & Admin > Service
   Accounts > Keys), and point the app at it either by setting an
   environment variable:

   ```
   set GOOGLE_APPLICATION_CREDENTIALS=path\to\your-key.json
   ```

   or by passing `--creds` on each run (see below).

## Usage

Speak text given directly on the command line:

```
python speak.py "Hello, world!"
```

Read text from a file:

```
python speak.py -f input.txt
```

Read text from stdin:

```
echo "Hello, world!" | python speak.py
```

By default the audio is saved to `output.mp3`. Use `-o` to change that:

```
python speak.py "Hello, world!" -o greeting.mp3
```

Play the audio immediately after saving:

```
python speak.py "Hello, world!" --play
```

Use a specific credentials file for a single run instead of the
environment variable:

```
python speak.py "Hello, world!" --creds path\to\your-key.json
```

### Options

| Flag             | Description                                                        |
| ---------------- | -------------------------------------------------------------------|
| `text`            | Text to speak (omit to read from `--file`, stdin, or a prompt)     |
| `-o, --output`     | Output MP3 file path (default: `output.mp3`)                       |
| `-f, --file`       | Read text from a file instead of the command line                  |
| `--voice`          | Google TTS voice name (default: `en-US-Standard-D`)                |
| `--language`       | Language code, e.g. `en-US` (default: derived from `--voice`)       |
| `--rate`           | Speaking rate, `0.25`–`4.0` (default: `1.0`)                        |
| `--pitch`          | Pitch, `-20.0` to `20.0` semitones (default: `0.0`)                 |
| `--creds`          | Path to a service account JSON key (overrides the env variable)     |
| `--play`           | Play the audio after saving                                         |

See the [Google Cloud TTS voice list](https://cloud.google.com/text-to-speech/docs/voices)
for available `--voice` names and languages.

# mp3

Turn a text file into speech with one command:

```
mp3 notes.txt
```

That's it — it creates `notes.mp3` in the same folder, using Google
Cloud Text-to-Speech. Everything else below is optional extras.

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

   This makes the `mp3` command available anywhere the environment is
   activated.

3. Get a Google Cloud service account key (IAM & Admin > Service
   Accounts > Keys) for a project with the Text-to-Speech API enabled,
   and point the tool at it:

   ```
   set GOOGLE_APPLICATION_CREDENTIALS=path\to\your-key.json
   ```

   (or pass `--creds path\to\your-key.json` on each run instead).

Now, whenever this environment is activated:

```
mp3 notes.txt
```

## Bonus features

Speak text given directly on the command line instead of a file:

```
mp3 "Hello, world!"
```

Read text from stdin:

```
echo "Hello, world!" | mp3
```

Choose a different output path (default: same name as the input file,
or `output.mp3` for direct/stdin text):

```
mp3 notes.txt -o greeting.mp3
```

Play the audio immediately after saving:

```
mp3 notes.txt --play
```

Use a specific credentials file for a single run instead of the
environment variable:

```
mp3 notes.txt --creds path\to\your-key.json
```

### Options

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

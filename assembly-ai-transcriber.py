# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)

import assemblyai as aai
import json

aai.settings.api_key = ""

transcriber = aai.Transcriber()

audio_url = "Weaviate-Podcast-110.mp3"

config = aai.TranscriptionConfig(speaker_labels=True)

transcript = transcriber.transcribe(audio_url, config)

print(transcript.text)

transcriptions = []
for utterance in transcript.utterances:
    print(f"\033[92mSpeaker {utterance.speaker}:\033[0m")
    print(f"{utterance.text}")
    transcriptions.append({
        "speaker": f"Speaker {utterance.speaker}",
        "content": utterance.text
    })

with open("transcription.json", "w") as f:
    json.dump(transcriptions, f, indent=4)
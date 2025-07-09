import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(audio_path: str) -> str:
    """
    Uses OpenAI Whisper transcription via new SDK.
    """
    try:
        print(f"[🔁] Uploading {audio_path} to OpenAI Whisper...")

        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        transcript_text = transcript.text

        # Save transcript
        filename = os.path.basename(audio_path).replace(".mp3", ".txt")
        transcript_path = os.path.join("static/transcripts", filename)

        os.makedirs("static/transcripts", exist_ok=True)
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript_text)

        print(f"[✅] Transcription saved at: {transcript_path}")
        return transcript_text

    except Exception as e:
        print(f"[❌] Error in OpenAI Whisper transcription: {e}")
        return ""

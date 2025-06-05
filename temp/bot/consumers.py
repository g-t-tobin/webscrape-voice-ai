from channels.generic.websocket import AsyncWebsocketConsumer
import tempfile
import subprocess
import whisper
import json

# Load Whisper model once globally
model = whisper.load_model("base")

class VoiceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            try:
                # Save received audio blob to a temporary raw file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as raw_file:
                    raw_file.write(bytes_data)
                    raw_file.flush()

                    # Prepare another temp file for the converted version
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as converted_file:
                        # Use ffmpeg to convert to 16kHz mono WAV (Whisper requirement)
                        command = [
                            "ffmpeg",
                            "-y",
                            "-i", raw_file.name,
                            "-ar", "16000",
                            "-ac", "1",
                            converted_file.name
                        ]
                        result = subprocess.run(
                            command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )

                        if result.returncode != 0:
                            # Log and send error back to client
                            await self.send(text_data=json.dumps({
                                "transcript": "Error: FFmpeg conversion failed",
                                "details": result.stderr.decode()
                            }))
                            return

                        # Transcribe the clean audio with Whisper
                        result = model.transcribe(converted_file.name)
                        await self.send(text_data=json.dumps({
                            "transcript": result["text"]
                        }))

            except Exception as e:
                await self.send(text_data=json.dumps({
                    "transcript": "Error processing audio",
                    "details": str(e)
                }))



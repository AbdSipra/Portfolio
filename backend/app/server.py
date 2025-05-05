import grpc
from concurrent import futures
import time
import numpy as np
import soundfile as sf
import tempfile
import os
import re
import nltk

from backend.protos import audio_pb2, audio_pb2_grpc
from backend.model.tts_model import Story2AudioModel

from nltk.tokenize import sent_tokenize

nltk.download('punkt')  # Download punkt if not already present

MAX_LENGTH = 1000  # Max allowed story length

class StoryAudioService(audio_pb2_grpc.StoryAudioServiceServicer):
    def __init__(self):
        self.tts_model = Story2AudioModel()

    def GenerateAudio(self, request, context):
        story_text = request.story_text.strip()

        # 🔎 Validate input
        if not story_text:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Input text cannot be empty or whitespace.")
        if len(story_text) > MAX_LENGTH:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, f"Input text exceeds max length of {MAX_LENGTH} characters.")
        if not re.search(r'[a-zA-Z0-9]', story_text):
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Input must contain valid letters or numbers, not only special characters.")

        try:
            sentences = sent_tokenize(story_text)

            full_audio = []
            sample_rate = None

            for sentence in sentences:
                if not sentence.strip():
                    continue

                print(f"🎤 Generating audio for: {sentence}")
                audio_np, sr = self.tts_model.generate_audio_from_text(sentence)

                if sample_rate is None:
                    sample_rate = sr

                full_audio.append(audio_np)

            if not full_audio:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, "No valid sentences found in the input.")

            combined_audio = np.concatenate(full_audio)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                tmpfile_name = tmpfile.name

            sf.write(tmpfile_name, combined_audio, sample_rate, format='WAV', subtype='PCM_16')

            with open(tmpfile_name, "rb") as f:
                audio_data = f.read()

            try:
                os.remove(tmpfile_name)
            except PermissionError:
                print(f"⚠ Warning: Could not delete {tmpfile_name}.")

            return audio_pb2.AudioResponse(audio_data=audio_data)

        except Exception as e:
            print("❌ Error occurred:", e)
            context.abort(grpc.StatusCode.INTERNAL, f"Failed to generate audio: {str(e)}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    audio_pb2_grpc.add_StoryAudioServiceServicer_to_server(StoryAudioService(), server)
    server.add_insecure_port("[::]:50051")
    print("🚀 Backend server running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

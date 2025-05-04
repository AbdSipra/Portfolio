import grpc
from concurrent import futures
import time
import numpy as np
import soundfile as sf
import tempfile
import os
import nltk

from backend.protos import audio_pb2, audio_pb2_grpc
from backend.model.tts_model import Story2AudioModel

from nltk.tokenize import sent_tokenize

# Make sure nltk punkt is available
nltk.data.path.append("/home/saad-khan/nltk_data")

class StoryAudioService(audio_pb2_grpc.StoryAudioServiceServicer):
    def __init__(self):
        self.tts_model = Story2AudioModel()

    def GenerateAudio(self, request, context):
        story_text = request.story_text
        sentences = sent_tokenize(story_text)

        full_audio = []
        sample_rate = None

        for sentence in sentences:
            # Skip empty sentences
            if not sentence.strip():
                continue

            print(f"🎤 Generating audio for: {sentence}")
            audio_np, sr = self.tts_model.generate_audio_from_text(sentence)

            if sample_rate is None:
                sample_rate = sr

            full_audio.append(audio_np)

        combined_audio = np.concatenate(full_audio)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            sf.write(tmpfile.name, combined_audio, sample_rate, format='WAV', subtype='PCM_16')
            with open(tmpfile.name, "rb") as f:
                audio_data = f.read()
            os.remove(tmpfile.name)

        return audio_pb2.AudioResponse(audio_data=audio_data)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    audio_pb2_grpc.add_StoryAudioServiceServicer_to_server(StoryAudioService(), server)
    server.add_insecure_port("[::]:50051")
    print("🚀 Backend server running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

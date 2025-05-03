import sys
import os
import grpc
from concurrent import futures
import io
import soundfile as sf

# Add backend path so we can import model and protos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from protos import audio_pb2, audio_pb2_grpc
from model.tts_model import Story2AudioModel

class StoryAudioService(audio_pb2_grpc.StoryAudioServiceServicer):
    def __init__(self):
        # Load the ParlerTTS model
        self.model = Story2AudioModel()

    def GenerateAudio(self, request, context):
        story_text = request.story_text
        print(f"[gRPC] Received story: {story_text}")

        # Generate audio numpy array and sample rate
        audio_np, sample_rate = self.model.generate_audio_from_text(story_text)

        # Convert numpy array to WAV bytes using PCM_16 (browser compatible)
        buffer = io.BytesIO()
        sf.write(buffer, audio_np, sample_rate, format='WAV', subtype='PCM_16')
        audio_bytes = buffer.getvalue()

        return audio_pb2.AudioResponse(audio_data=audio_bytes)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    audio_pb2_grpc.add_StoryAudioServiceServicer_to_server(StoryAudioService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("✅ ParlerTTS gRPC Server running on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

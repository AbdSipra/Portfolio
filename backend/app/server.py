import sys
import os
import grpc
import io
from concurrent import futures

# Add backend path so we can import model and protos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from protos import audio_pb2, audio_pb2_grpc
from model.tts_model import Story2AudioModel
import soundfile as sf

class StoryAudioService(audio_pb2_grpc.StoryAudioServiceServicer):
    def __init__(self):
        self.model = Story2AudioModel()

    def GenerateAudio(self, request, context):
        story_text = request.story_text
        print(f"[gRPC] Received story: {story_text}")

        # Generate audio numpy array and sample rate
        audio_np, sample_rate = self.model.generate_audio_from_text(story_text)

        # Write numpy array to WAV format in memory
        buffer = io.BytesIO()
        sf.write(buffer, audio_np, sample_rate, format='WAV', subtype='PCM_16')
        audio_bytes = buffer.getvalue()

        return audio_pb2.AudioResponse(audio_data=audio_bytes)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    audio_pb2_grpc.add_StoryAudioServiceServicer_to_server(StoryAudioService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("✅ gRPC Server running on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

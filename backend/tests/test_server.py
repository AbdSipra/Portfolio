#checking if the gRPC server is running 

import grpc
import sys
import os

# Allow imports from sibling 'protos' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from protos import audio_pb2
from protos import audio_pb2_grpc

def test_generate_audio():
    # Connect to the gRPC server
    channel = grpc.insecure_channel('localhost:50051')

    # Create a stub (client) to use the service
    stub = audio_pb2_grpc.StoryAudioServiceStub(channel)

    # Create a request message
    request = audio_pb2.AudioRequest(story_text="Ansari likes the smell of... ;)")

    # Call the GenerateAudio method
    response = stub.GenerateAudio(request)

    # Check that we got a response
    assert response.audio_data is not None, "Response audio is None!"
    assert len(response.audio_data) > 0, "Response audio is empty!"

    print("✅ Test passed: Received audio data from server.")

if __name__ == "__main__":
    test_generate_audio()



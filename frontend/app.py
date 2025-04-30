import gradio as gr
import grpc
import sys
import os

# Add backend path to import protos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from protos import audio_pb2, audio_pb2_grpc

# Setup gRPC client
channel = grpc.insecure_channel("localhost:50051")
stub = audio_pb2_grpc.StoryAudioServiceStub(channel)

def generate_audio_gradio(story_text):
    if not story_text.strip():
        return None  # No empty requests

    try:
        # Create a request message
        request = audio_pb2.AudioRequest(story_text=story_text)

        # Send request and get response
        response = stub.GenerateAudio(request)

        # Save audio bytes to a temporary file
        output_path = "frontend_output.wav"
        with open(output_path, "wb") as f:
            f.write(response.audio_data)

        return output_path  # Gradio will play this file
    except Exception as e:
        print(f"Error: {e}")
        return None

# Build Gradio Interface
iface = gr.Interface(
    fn=generate_audio_gradio,
    inputs=gr.Textbox(lines=8, placeholder="Enter your story here...", label="Story Text"),
    outputs=gr.Audio(type="numpy", label="Generated Audio"),
    title="Story2Audio Generator",
    description="Paste a story below and generate lifelike audio using Bark TTS via gRPC backend.",
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)

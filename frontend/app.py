import gradio as gr
import grpc
import sys
import os
import io
import soundfile as sf
import numpy as np
import tempfile
import threading
import time

# Add backend path to import protos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from protos import audio_pb2, audio_pb2_grpc

# Setup gRPC client
channel = grpc.insecure_channel("localhost:50051")
stub = audio_pb2_grpc.StoryAudioServiceStub(channel)

# Function to delete file after some time
def delete_file_later(filepath, delay=30):
    def delete():
        time.sleep(delay)
        try:
            os.remove(filepath)
            print(f"✅ Deleted temporary file: {filepath}")
        except Exception as e:
            print(f"⚠️ Error deleting file {filepath}: {e}")
    threading.Thread(target=delete, daemon=True).start()

def generate_audio_gradio(story_text):
    if not story_text.strip():
        return None  # No empty requests

    try:
        # Create a request message
        request = audio_pb2.AudioRequest(story_text=story_text)

        # Send request and get response
        response = stub.GenerateAudio(request)

        # Read the audio bytes into numpy
        buffer = io.BytesIO(response.audio_data)
        audio_np, sr = sf.read(buffer, dtype="float32")

        # Normalize/Clamp audio to be safe for PCM16
        audio_np = np.clip(audio_np, -1.0, 1.0)

        # Save to temporary file (IMPORTANT: Save as PCM_16 with WAV format)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            sf.write(tmpfile.name, audio_np, sr, format='WAV', subtype='PCM_16')
            filepath = tmpfile.name

        # Schedule file for deletion
        delete_file_later(filepath)

        # Return path to Gradio
        return filepath

    except Exception as e:
        print(f"Error: {e}")
        return None


# Build Gradio Interface
iface = gr.Interface(
    fn=generate_audio_gradio,
    inputs=gr.Textbox(lines=8, placeholder="Enter your story here...", label="Story Text"),
    outputs=gr.Audio(type="filepath", label="Generated Audio"),
    title="Story2Audio Generator",
    description="Paste a story below and generate lifelike audio using XTTS v2 via gRPC backend.",
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)

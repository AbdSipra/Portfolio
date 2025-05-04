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

# Add backend path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from protos import audio_pb2, audio_pb2_grpc

channel = grpc.insecure_channel("localhost:50051")
stub = audio_pb2_grpc.StoryAudioServiceStub(channel)

def delete_file_later(filepath, delay=30):
    def delete():
        time.sleep(delay)
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Error deleting file: {e}")
    threading.Thread(target=delete, daemon=True).start()

def generate_audio_gradio(story_text):
    if not story_text.strip():
        return None

    try:
        request = audio_pb2.AudioRequest(story_text=story_text)
        response = stub.GenerateAudio(request)

        buffer = io.BytesIO(response.audio_data)
        audio_np, sr = sf.read(buffer, dtype="float32")
        audio_np = np.clip(audio_np, -1.0, 1.0)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            sf.write(tmpfile.name, audio_np, sr, format='WAV', subtype='PCM_16')
            filepath = tmpfile.name

        delete_file_later(filepath)
        return filepath

    except Exception as e:
        print(f"Error: {e}")
        return None

iface = gr.Interface(
    fn=generate_audio_gradio,
    inputs=gr.Textbox(lines=8, placeholder="Enter your story here...", label="Story Text"),
    outputs=gr.Audio(type="filepath", label="Generated Audio"),
    title="Story2Audio Generator",
    description="Paste a story below and generate lifelike audio using narration style + XTTS2",
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)

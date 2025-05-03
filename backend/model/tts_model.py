import os
import numpy as np
import soundfile as sf
import tempfile
from TTS.api import TTS

class Story2AudioModel:
    def __init__(self):
        print("Loading Jenny TTS model...")
        self.tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=True, gpu=False)

        # Jenny is a single speaker model, so no speaker wav or speaker id is required
        print("✅ Jenny model loaded successfully.")

    def generate_audio_from_text(self, text):
        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            output_path = tmpfile.name

        # Generate and save audio
        self.tts.tts_to_file(
            text=text,
            file_path=output_path
        )

        # Read audio as numpy array
        audio_np, sr = sf.read(output_path, dtype="float32")

        # Delete the temporary file after reading
        os.remove(output_path)

        return audio_np, sr

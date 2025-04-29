#This file will load Bark TTS model and handle audio generation

import torch
import numpy as np
import os
from bark import generate_audio, preload_models
#this comment tells that the code pushed was done while in LRC with saad and ansari

# === PATCH for Bark Compatibility with PyTorch 2.1+ ===
import torch.serialization

# Allow numpy scalar global safely
if hasattr(torch.serialization, "add_safe_globals"):
    torch.serialization.add_safe_globals([np.core.multiarray.scalar])

# Patch torch.load to force weights_only=False
_original_torch_load = torch.load
def patched_torch_load(*args, **kwargs):
    if "weights_only" not in kwargs:
        kwargs["weights_only"] = False
    return _original_torch_load(*args, **kwargs)
torch.load = patched_torch_load
# =======================================================


class Story2AudioModel:
    def __init__(self):
        # Preload Bark models (loads into memory once)
        print("Loading Bark models...please wait.")
        preload_models()
        print("Bark models loaded successfully.")

    def generate_audio_from_text(self, text, output_path="output.wav"):
        print(f"Generating audio for text: {text}")
        
        # Generate audio from text
        audio_array = generate_audio(text, history_prompt="v2/en_speaker_6")

        
        # Save audio to file
        from scipy.io.wavfile import write as write_wav
        sample_rate = 24_000  # Bark uses 24 kHz
        write_wav(output_path, sample_rate, audio_array)
        
        print(f"Audio saved to {output_path}")
        return output_path

if __name__ == "__main__":
    print()
    model = Story2AudioModel()
    model.generate_audio_from_text("Once upon a time, there was a brave knight who saved the world!")

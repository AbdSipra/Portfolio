# backend/model/bark_model.py

import torch
import numpy as np
import io
import soundfile as sf
from bark import generate_audio, preload_models

# === PATCH for Bark Compatibility with PyTorch 2.1+ ===
import torch.serialization
if hasattr(torch.serialization, "add_safe_globals"):
    torch.serialization.add_safe_globals([np.core.multiarray.scalar])

_original_torch_load = torch.load
def patched_torch_load(*args, **kwargs):
    if "weights_only" not in kwargs:
        kwargs["weights_only"] = False
    return _original_torch_load(*args, **kwargs)
torch.load = patched_torch_load
# =======================================================

class Story2AudioModel:
    def __init__(self):
        print("Loading Bark models...please wait.")
        preload_models()
        print("Bark models loaded successfully.")

    def generate_audio_from_text(self, text: str, speaker: str = "v2/en_speaker_6") -> bytes:
        print(f"Generating audio for text: {text}")
        print(f"Using speaker: {speaker}")

        # Generate Bark audio as NumPy array
        audio_array = generate_audio(text, history_prompt=speaker)

        # Convert to WAV bytes in memory
        buffer = io.BytesIO()
        sf.write(buffer, audio_array, samplerate=24000, format='WAV')
        audio_bytes = buffer.getvalue()

        return audio_bytes

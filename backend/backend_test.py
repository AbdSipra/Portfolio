import os
import nltk
from nltk.tokenize import sent_tokenize
from backend.model.tts_model import Story2AudioModel
from backend.model.llm_model import LLMNarrator
import numpy as np
import soundfile as sf
import tempfile

# Ensure nltk punkt is available
nltk.data.path.append("/home/saad-khan/nltk_data")

# Example story
story = """
At the bottom, she found a door carved with strange symbols.
It was unlike anything she had ever seen before.
Cautiously, she pushed it open and stepped into the unknown.
"""

print("✅ Story loaded. Splitting into sentences...")
sentences = sent_tokenize(story)
print(sentences)

tts_model = Story2AudioModel()
llm = LLMNarrator()

full_audio = []
sample_rate = None

for sentence in sentences:
    description = llm.generate_narration_instruction(sentence)
    print(f"🎨 Narration Style: {description}")

    audio_np, sr = tts_model.generate_audio_from_text(sentence)

    if sample_rate is None:
        sample_rate = sr

    full_audio.append(audio_np)

combined_audio = np.concatenate(full_audio)

output_file = "test_output.wav"
sf.write(output_file, combined_audio, sample_rate, format='WAV', subtype='PCM_16')
print(f"✅ Saved generated audio to {output_file}")

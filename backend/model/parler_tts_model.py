import os
import numpy as np
import soundfile as sf
import torch
import tempfile
from transformers import AutoTokenizer
from parler_tts import ParlerTTSForConditionalGeneration
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

class Story2AudioModel:
    def __init__(self):
        print("Loading ParlerTTS Jenny model...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = ParlerTTSForConditionalGeneration.from_pretrained(
            "parler-tts/parler-tts-mini-jenny-30H"
        ).to(self.device)

        self.tokenizer = AutoTokenizer.from_pretrained(
            "parler-tts/parler-tts-mini-jenny-30H"
        )

        self.sampling_rate = self.model.config.sampling_rate
        print("✅ ParlerTTS model loaded.")

    def generate_audio_from_text(self, text, description="Read in an excited manner , emphasizing the pauses"):

        # Break text into sentences
        sentences = sent_tokenize(text)

        audio_segments = []

        for sentence in sentences:
            print(f"🔊 Generating audio for sentence: {sentence}")

            input_ids = self.tokenizer(description, return_tensors="pt").input_ids.to(self.device)
            prompt_input_ids = self.tokenizer(sentence, return_tensors="pt").input_ids.to(self.device)

            generation = self.model.generate(
                input_ids=input_ids,
                prompt_input_ids=prompt_input_ids,
                max_new_tokens=4000  # allows more output
            )

            audio_arr = generation.cpu().numpy().squeeze()
            audio_segments.append(audio_arr)

        # Concatenate all audio segments
        final_audio = np.concatenate(audio_segments)

        # Save to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            sf.write(tmpfile.name, final_audio, self.sampling_rate, subtype='PCM_16')
            filepath = tmpfile.name

        # Load audio back as numpy
        audio_np, sr = sf.read(filepath, dtype="float32")

        # Delete temp file after loading
        os.remove(filepath)

        return audio_np, sr

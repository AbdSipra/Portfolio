import os
import numpy as np
import soundfile as sf
import torch
import tempfile
from transformers import AutoTokenizer
from parler_tts import ParlerTTSForConditionalGeneration
import re

def simple_sentence_tokenize(text):
    return re.split(r'(?<=[.!?]) +', text)

class Story2AudioModel:
    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Story2AudioModel, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return  # Already initialized, skip

        print("🔄 Loading ParlerTTS Jenny model...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = ParlerTTSForConditionalGeneration.from_pretrained(
            "parler-tts/parler-tts-mini-jenny-30H"
        ).to(self.device)

        self.tokenizer = AutoTokenizer.from_pretrained(
            "parler-tts/parler-tts-mini-jenny-30H"
        )

        self.sampling_rate = self.model.config.sampling_rate
        print("✅ ParlerTTS model loaded.")
        self._initialized = True

    def generate_audio_from_text(self, text, description="Read in an excited manner , emphasizing the pauses"):
        if not text or not text.strip():
            raise ValueError("Text for audio generation is empty.")

        sentences = simple_sentence_tokenize(text)
        audio_segments = []

        for sentence in sentences:
            if not sentence.strip():
                continue

            print(f"🔊 Generating audio for sentence: {sentence}")

            input_ids = self.tokenizer(description, return_tensors="pt").input_ids.to(self.device)
            prompt_input_ids = self.tokenizer(sentence, return_tensors="pt").input_ids.to(self.device)

            generation = self.model.generate(
                input_ids=input_ids,
                prompt_input_ids=prompt_input_ids,
                max_new_tokens=4000
            )

            audio_arr = generation.cpu().numpy().squeeze()
            audio_segments.append(audio_arr)

        if not audio_segments:
            raise ValueError("No valid audio segments generated.")

        final_audio = np.concatenate(audio_segments)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            sf.write(tmpfile.name, final_audio, self.sampling_rate, subtype='PCM_16')
            filepath = tmpfile.name

        audio_np, sr = sf.read(filepath, dtype="float32")
        os.remove(filepath)

        return audio_np, sr

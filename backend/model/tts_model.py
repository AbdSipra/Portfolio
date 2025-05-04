import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import numpy as np

class Story2AudioModel:
    def __init__(self):
        print("Loading Parler Jenny model...")
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model = ParlerTTSForConditionalGeneration.from_pretrained("parler-tts/parler-tts-mini-jenny-30H").to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler-tts-mini-jenny-30H")
        print("✅ Parler Jenny model loaded.")

        # Use a fixed style description (can be improved later)
        self.default_style = "Speaks at an average pace with clear and animated tone."

    def generate_audio_from_text(self, prompt_text):
        # Prepare style and prompt
        input_ids = self.tokenizer(self.default_style, return_tensors="pt").input_ids.to(self.device)
        prompt_input_ids = self.tokenizer(prompt_text, return_tensors="pt").input_ids.to(self.device)

        # Generate audio
        generation = self.model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)

        # Convert to numpy
        audio_np = generation.cpu().numpy().squeeze()

        return audio_np, self.model.config.sampling_rate

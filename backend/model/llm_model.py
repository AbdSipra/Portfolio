from transformers import AutoTokenizer, AutoModelForCausalLM

class LLMNarrator:
    def __init__(self):
        print("Loading Phi-3 Mini for narration style...")
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-3-mini-4k-instruct")
        self.model = AutoModelForCausalLM.from_pretrained(
            "microsoft/phi-3-mini-4k-instruct",
            torch_dtype="auto"
        )
        print("✅ Phi-3 Mini loaded.")

    def generate_narration_instruction(self, sentences_list):
        context = " ".join(sentences_list)

        prompt = f"Based on the following passage, describe the narrator's voice style in short (example: calm, animated, fast paced): '{context}'"

        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=30)

        description = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        return description

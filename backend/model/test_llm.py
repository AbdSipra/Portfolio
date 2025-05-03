from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-3-mini-4k-instruct")
model = AutoModelForCausalLM.from_pretrained("microsoft/phi-3-mini-4k-instruct", device_map="auto")

prompt = "Describe how a narrator should read this sentence: 'Sarah walked into the room and whispered hello.'"
inputs = tokenizer(prompt, return_tensors="pt")

outputs = model.generate(**inputs, max_new_tokens=50)
description = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(description)

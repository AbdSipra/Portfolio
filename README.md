# story2audio
**Story2Audio Microservice Documentation**

---
<img src='C:\Users\abdul\story2audio\story2audio\architecture.png'>
**Table of Contents**

1. Overview
2. System Architecture
3. Setup Instructions
4. Usage Guidelines
5. API Specification
6. Test Cases
7. Performance Evaluation
8. Model Sources
9. Limitations
10. Contributors

---

# 1. Overview

**Story2Audio** is a gRPC-based microservice that converts user-provided text into audio narration using the ParlerTTS Jenny text-to-speech model. It supports concurrent requests, includes validation for edge cases, and has been tested using Postman and a Gradio frontend.

---

# 2. System Architecture

**Architecture Diagram:**

![Architecture Diagram](A_flowchart-style_digital_2D_diagram_illustrates_t.png)

* **Client Layer**: Postman gRPC client or minimal frontend (Gradio/Streamlit).
* **Server Layer**: gRPC server with StoryAudioService (handles requests, validation, and concurrency).
* **Model Layer**: ParlerTTS Jenny model used for speech synthesis.

---

# 3. Setup Instructions

## Environment Setup

```bash
git clone <repository-link>
cd story2audio
```

### Optional: Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

### Install required libraries

```bash
pip install -r requirements.txt
```

### NLTK Data (only first time)

```bash
python -m nltk.downloader punkt
```

### Run the Server

```bash
python backend/app/server.py
```

The server will start at `localhost:50051`.

---

# 4. Usage Guidelines

## Using Postman (Recommended for Testing)

1. Open Postman.
2. Import the provided gRPC collection: `story2audio gRPC test`.
3. Select any test case (e.g., TC1 - short sentence).
4. Click **Invoke** to receive the audio response.

## Using Gradio or Streamlit (Optional Frontend)

```bash
python frontend/app.py
```

The UI will allow text input and playback of generated audio.

---

# 5. API Specification

## gRPC Method: GenerateAudio

| Parameter   | Type   | Description                |
| ----------- | ------ | -------------------------- |
| story\_text | string | Text to convert into audio |

### Returns

* `audio_data`: bytes (WAV format)

### Validation Checks

* Empty or whitespace-only text is rejected.
* Excessively long text is rejected.
* Special characters (%, \$, #, ^) are blocked.

### Status Codes

* 0 OK: Success
* 3 INVALID\_ARGUMENT: Invalid input

---

# 6. Test Cases

| Test Case | Description                  | Expected Outcome                      |
| --------- | ---------------------------- | ------------------------------------- |
| TC1       | Simple sentence              | Audio response                        |
| TC2       | Short text                   | Audio response                        |
| TC3       | Long paragraph               | Audio response                        |
| TC4       | Concurrency test             | Audio responses, concurrency verified |
| unnamed   | Additional concurrency tests | Audio responses, concurrency verified |

All test cases passed successfully during testing.

---

# 7. Performance Evaluation

## Concurrency Test Results (5 concurrent requests)

| Request Number | Response Time (seconds) |
| -------------- | ----------------------- |
| 1              | 54.18                   |
| 2              | 47.05                   |
| 3              | 49.76                   |
| 4              | 52.82                   |

## Performance Graph

A graph was generated to visualize response time vs number of concurrent requests using comparison\_graph.py.

---

# 8. Model Sources

| Component | Source                                                                                                                                                 |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| TTS Model | Parler-TTS Mini Jenny 30H ([https://huggingface.co/parler-tts/parler-tts-mini-jenny-30H](https://huggingface.co/parler-tts/parler-tts-mini-jenny-30H)) |
| Tokenizer | Hugging Face AutoTokenizer                                                                                                                             |

---

# 9. Limitations

* Response time increases with long inputs and high concurrency.
* Input text is limited to reasonable length for performance reasons.
* Currently supports English text only.
* Audio is returned as raw bytes and must be saved or played back by the client.
* Due to lack of GPU, the model runs on CPU, which significantly increases processing time. Additionally, we are unable to load any smaller models like Phi due to hardware constraints.

---

# 10. Contributors

**Abdullah, Saad, Ansari** 

---

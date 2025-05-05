FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend ./backend
COPY requirements.txt .

# Install PyTorch CPU version
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install project requirements
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader punkt

# Add /app to PYTHONPATH so backend module works
ENV PYTHONPATH=/app

EXPOSE 50051

CMD ["python", "backend/app/server.py"]

# Use PyTorch base image with CUDA (for GPU support)
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc git cmake && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# add api.py
COPY api.py .

# copy the model/tokenizer
COPY ./Mistral-7B-Instruct-v0.3 /app/Mistral-7B-Instruct-v0.3

# Expose API port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

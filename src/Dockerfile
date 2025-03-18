FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

WORKDIR /app

# Install system dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y gcc git cmake && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy backend
COPY ./backend/api.py /app/api.py
COPY ./backend/Mistral-7B-Instruct-v0.3 /app/Mistral-7B-Instruct-v0.3

# copy frontend
COPY ./frontend/components /app/components
COPY ./frontend/pages /app/pages
COPY ./frontend/Chat.py /app/Chat.py

# add run.sh
COPY ./run.sh /app/run.sh
RUN chmod +x /app/run.sh

# Expose API and Streamlit ports
EXPOSE 8000 8501

CMD ["/app/run.sh"]
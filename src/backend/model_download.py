from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    local_dir="./Mistral-7B-Instruct-v0.3",  # Path to save the model
    local_dir_use_symlinks=False  # Ensures compatibility in Docker
)

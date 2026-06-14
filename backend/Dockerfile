# Backend container for FastAPI, CPU-only PyTorch, and YOLO inference.
FROM python:3.12-slim

# Setup user for Hugging Face Spaces
RUN useradd -m -u 1000 user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* && \
    chown -R user:user $HOME/app

COPY --chown=user requirements.txt .
USER user

RUN python -m pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu && \
    grep -vE '^(torch|torchvision)$' requirements.txt > requirements-docker.txt && \
    pip install --no-cache-dir -r requirements-docker.txt

COPY --chown=user . $HOME/app

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]

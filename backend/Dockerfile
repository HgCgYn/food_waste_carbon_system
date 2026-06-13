# Backend container for FastAPI, CPU-only PyTorch, and YOLO inference.
FROM python:3.12-slim

WORKDIR /app

ARG YOLO_MODEL_URL=https://github.com/joaopferreira19/Food-Waste-Detection-using-YOLOv11/releases/download/0.3.0/yolov11-x-weights-v6.pt
ARG YOLO_MODEL_SHA256=bb4beadb985b85b8768dcda52ca85d1ea1dbb533afcbf9f46bd1f014651c1ca7

COPY backend/requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu && \
    grep -vE '^(torch|torchvision)$' requirements.txt > requirements-docker.txt && \
    pip install --no-cache-dir -r requirements-docker.txt

COPY backend/ .
COPY database/init.sql /app/sql/init.sql

RUN mkdir -p server/yolo/weights && \
    curl --fail --location --retry 5 --retry-all-errors --continue-at - \
      --output server/yolo/weights/yolov11-x-weights-v6.pt \
      "${YOLO_MODEL_URL}" && \
    echo "${YOLO_MODEL_SHA256}  server/yolo/weights/yolov11-x-weights-v6.pt" | sha256sum --check -

EXPOSE 10000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000}"]

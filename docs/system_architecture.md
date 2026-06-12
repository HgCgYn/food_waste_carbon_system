<!-- Brief architecture note for the food waste carbon estimation system. -->

# System Architecture

## Overview

This system implements an **Edge-Cloud Collaborative** architecture for food waste carbon estimation.

- **Edge Inference (YOLO)**: YOLOv11 runs locally inside Docker to detect food items with high confidence. Low-confidence objects (below `VLM_CONFIDENCE_THRESHOLD = 0.70`) are flagged for cloud review.
- **Cloud VLM (optional)**: Cropped images of all low-confidence objects in a single request are **batched into one API call** and sent to Google Gemini or OpenAI GPT-4o for secondary visual confirmation. The VLM returns results as a structured JSON array, which conserves Free Tier RPM quotas. Each object is then either corrected with a new label, or marked as non-food/ignored if unrecognized.

## Services

`frontend` is a React + Vite client responsible for image upload, total waste weight input, model selection (`yolo` / `yolo_gemini` / `yolo_gpt`), and result presentation including the VLM correction column (⚡).

`backend` is a FastAPI service that:
1. Receives the image and runs YOLOv11 segmentation.
2. Optionally calls `VLMService` (`vlm_service.py`) to correct low-confidence detections.
3. Estimates each food item's weight from object area and `density_factor`.
4. Calculates carbon emissions from `carbon_factor`.
5. Stores the analysis result into PostgreSQL.

`database` contains the PostgreSQL bootstrap SQL for the system tables and starter food factor data.

`docker-compose.yml` orchestrates `frontend`, `backend`, `postgres`, and optional `pgadmin`.

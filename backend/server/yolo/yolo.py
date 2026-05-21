"""YOLO wrapper that loads weights from the new backend/server/yolo layout."""

from pathlib import Path

import torch
from ultralytics import YOLO


class YOLOModel:
    def __init__(self):
        self.model = self.load_model()

    def load_model(self):
        try:
            print("Loading YOLO model...")
            weights_path = Path(__file__).resolve().parent / "weights" / "yolov11-x-weights-v6.pt"
            model = YOLO(str(weights_path))
            print("Model loaded!")
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            return None

    def predict(self, frame):
        try:
            if self.model is None:
                raise RuntimeError("YOLO model is not available")
            print("Predicting...")
            with torch.no_grad():
                results = self.model(frame)
            detected_objects = []
            for result in results:
                if result.masks is None:
                    continue
                for i, (mask, box) in enumerate(zip(result.masks.data, result.boxes)):
                    area = mask.sum().item()
                    detected_objects.append(
                        {
                            "label": box.cls.item(),
                            "label_name": result.names[box.cls.item()],
                            "confidence": box.conf.item(),
                            "box": box.xyxy.tolist(),
                            "area": area,
                        }
                    )

            print("Success!")
            return detected_objects, results
        except Exception as e:
            print(f"Error predicting: {e}")
            return None, None

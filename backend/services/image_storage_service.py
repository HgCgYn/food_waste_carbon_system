"""Image storage helper for persisting uploads and YOLO output images."""

from datetime import datetime
from io import BytesIO
from pathlib import Path

from PIL import Image


class ImageStorageService:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parents[1] / "storage"
        self.upload_dir = self.base_dir / "uploads"
        self.result_dir = self.base_dir / "results"
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.result_dir.mkdir(parents=True, exist_ok=True)

    def save_upload(self, original_filename: str, content: bytes) -> str:
        suffix = Path(original_filename).suffix or ".jpg"
        path = self.upload_dir / f"{self._timestamp()}_{Path(original_filename).stem}{suffix}"
        path.write_bytes(content)
        return str(path)

    def result_image_from_detection(self, result, include_boxes: bool) -> Image.Image:
        plotted = result.plot(boxes=include_boxes, labels=True, color_mode="class")
        return Image.fromarray(plotted)

    def save_pil_image(self, prefix: str, image: Image.Image) -> str:
        path = self.result_dir / f"{self._timestamp()}_{prefix}.jpg"
        image.save(path, format="JPEG")
        return str(path)

    def pil_to_bytes(self, image: Image.Image) -> bytes:
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        return buffer.getvalue()

    def _timestamp(self) -> str:
        return datetime.utcnow().strftime("%Y%m%d%H%M%S%f")

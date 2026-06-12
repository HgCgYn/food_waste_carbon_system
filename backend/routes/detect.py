"""Detection API that runs YOLO, estimates weights, calculates carbon, and stores results."""

import base64
import io
import logging
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from PIL import Image
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import AnalysisItem, AnalysisRecord
from services.carbon_calculator import estimate_items_and_total
from services.food_factor_service import FoodFactorLookupService
from services.image_storage_service import ImageStorageService
from services.vlm_service import UNKNOWN_LABEL, VLMService
from server.yolo.yolo import YOLOModel

logger = logging.getLogger(__name__)

router = APIRouter()
yolo_model = YOLOModel()
image_storage_service = ImageStorageService()

# NOTE: YOLO 信心度低於此門檻的物件才會觸發 VLM 二次確認
VLM_CONFIDENCE_THRESHOLD = 0.50

GARBAGE_CLASSES = {35.0}
IGNORE_CLASSES = {58.0, 31.0, 42.0, 70.0, 83.0, 25.0, 27.0, 22.0, 11.0, 8.0}
PLATE_CLASS = 58.0


@router.post("/detect")
async def detect_objects(
    file: UploadFile = File(...),
    total_weight_g: float = Form(...),
    model: str = Form(default="yolo"),
    user_id: Optional[int] = Form(default=None),
    db: Session = Depends(get_db),
):
    if total_weight_g <= 0:
        raise HTTPException(status_code=400, detail="total_weight_g must be greater than 0")

    image_bytes = await file.read()
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid image upload") from exc

    detected_objects, results = yolo_model.predict(image)
    if results is None:
        raise HTTPException(status_code=500, detail="Error in object detection")

    output_image = image_storage_service.result_image_from_detection(results[0], include_boxes=True)
    clustering_image = image_storage_service.result_image_from_detection(results[0], include_boxes=False)

    plate_area = 0.0
    garbage_area = 0.0
    food_area = 0.0

    for obj in detected_objects:
        label = float(obj["label"])
        if label == PLATE_CLASS:
            plate_area += obj["area"]
        if label in GARBAGE_CLASSES:
            garbage_area += obj["area"]
        if label not in GARBAGE_CLASSES and label not in IGNORE_CLASSES:
            food_area += obj["area"]

    if plate_area == 0:
        raise HTTPException(status_code=400, detail="No plate detected in the image")

    # ── VLM 二次確認（僅在 YOLO + Gemini / YOLO + GPT 模式下執行）──────────
    if model in ("yolo_gemini", "yolo_gpt"):
        try:
            vlm = VLMService(model=model)
            for obj in detected_objects:
                label = float(obj["label"])
                # NOTE: 只有食物物件且信心度低於門檻才送 VLM 確認
                if (
                    label not in GARBAGE_CLASSES
                    and label not in IGNORE_CLASSES
                    and obj["confidence"] < VLM_CONFIDENCE_THRESHOLD
                ):
                    box_coords = obj["box"][0]  # xyxy 格式
                    x1, y1, x2, y2 = (
                        int(box_coords[0]),
                        int(box_coords[1]),
                        int(box_coords[2]),
                        int(box_coords[3]),
                    )
                    cropped = image.crop((x1, y1, x2, y2))
                    
                    original_label_name = obj["label_name"]
                    corrected_label = vlm.confirm_low_confidence_item(
                        cropped_image=cropped,
                        yolo_label=original_label_name,
                    )
                    
                    if corrected_label == UNKNOWN_LABEL:
                        # NOTE: VLM 認定非食物 → 標記此物件為略過
                        obj["vlm_ignored"] = True
                    else:
                        # NOTE: 儲存原始 YOLO 標籤，供前端顯示「vegetables → chicken」的更正明細
                        obj["original_yolo_label"] = original_label_name
                        obj["label_name"] = corrected_label
                        obj["vlm_corrected"] = True
                        
                    logger.info(
                        "VLM correction: %s (conf=%.2f) → %s",
                        original_label_name,
                        obj["confidence"],
                        corrected_label,
                    )
        except EnvironmentError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    waste_percentage = 0.0
    if plate_area > garbage_area:
        waste_percentage = (food_area / (plate_area - garbage_area)) * 100
    waste_percentage = min(max(waste_percentage, 0.0), 100.0)

    # 過濾掉被 VLM 判定為非食物的物件
    valid_objects = [obj for obj in detected_objects if not obj.get("vlm_ignored", False)]

    factor_service = FoodFactorLookupService(db)
    enriched_items, total_carbon_emission_kg = estimate_items_and_total(
        detected_objects=valid_objects,
        total_weight_g=total_weight_g,
        factor_resolver=factor_service.resolve_factor,
        ignored_labels=GARBAGE_CLASSES | IGNORE_CLASSES,
    )

    original_path = image_storage_service.save_upload(file.filename or "upload.jpg", image_bytes)
    detect_path = image_storage_service.save_pil_image("detected", output_image)
    cluster_path = image_storage_service.save_pil_image("clustered", clustering_image)

    record = AnalysisRecord(
        user_id=user_id,
        image_path=original_path,
        total_weight_g=total_weight_g,
        total_carbon_emission_kg=total_carbon_emission_kg,
        waste_percentage=waste_percentage,
        model_used=model,
    )
    db.add(record)
    db.flush()

    for item in enriched_items:
        db.add(
            AnalysisItem(
                record_id=record.record_id,
                yolo_label=item["yolo_label"],
                food_name_zh=item["food_name_zh"],
                confidence=item["confidence"],
                area=item["area"],
                density_factor=item["density_factor"],
                estimated_weight_g=item["estimated_weight_g"],
                carbon_factor=item["carbon_factor"],
                carbon_emission_kg=item["carbon_emission_kg"],
            )
        )

    db.commit()
    db.refresh(record)

    matched_item_count = sum(1 for item in enriched_items if item["has_carbon_data"])
    unmatched_item_count = len(enriched_items) - matched_item_count

    return {
        "record_id": record.record_id,
        "objects": enriched_items,
        "image_base64": pil_to_base64(output_image),
        "clustering_image_base64": pil_to_base64(clustering_image),
        "waste_percentage": waste_percentage,
        "food_area": food_area,
        "garbage_area": garbage_area,
        "plate_area": plate_area,
        "total_weight_g": total_weight_g,
        "total_carbon_emission_kg": total_carbon_emission_kg,
        "matched_item_count": matched_item_count,
        "unmatched_item_count": unmatched_item_count,
        "image_paths": {
            "original": original_path,
            "detected": detect_path,
            "clustered": cluster_path,
        },
    }


def pil_to_base64(image: Image.Image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

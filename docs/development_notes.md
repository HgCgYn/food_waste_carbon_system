<!-- Brief development notes for local and containerized workflows. -->

# Development Notes

## YOLO 模型載入

The original `restapi/server/yolo/yolo.py` and `weights/yolov11-x-weights-v6.pt` were copied into the new backend layout so the original repo is not modified destructively during the refactor.

The backend loads YOLO weights by resolving the path from `backend/server/yolo/yolo.py`, which avoids path breakage after the directory rename.

YOLO is configured with `conf=0.10` to maximise recall (High Recall Edge). Low-confidence objects are not discarded; instead they are passed to the cloud VLM for secondary confirmation.

## VLM 整合

`backend/services/vlm_service.py` handles all VLM API calls. It supports two backends:

- **Google Gemini** (`yolo_gemini` mode): requires `GEMINI_API_KEY` in `.env`. Uses `gemini-2.5-flash`.
- **OpenAI GPT-4o** (`yolo_gpt` mode): requires `OPENAI_API_KEY` in `.env`. Uses `gpt-4o` with `detail=low`.

The confidence threshold that triggers VLM review is `VLM_CONFIDENCE_THRESHOLD = 0.70` in `backend/routes/detect.py`. Adjust this value to trade off API cost versus correction coverage.

All low-confidence objects in a single request are batched into **one API call** (`confirm_low_confidence_items_batch`). Both Gemini and GPT-4o return results as a JSON array, which conserves the Free Tier RPM (Requests Per Minute) quota significantly.

## 碳排資料

`food_carbon_factors` includes starter seed data only. Update the table to match your trained YOLO label names for accurate carbon estimation.

`foodcarbondata.csv` is the normalized union of `foodcarbon.csv` and `food-product.csv`. It keeps only the fields needed for carbon calculation and standardizes the carbon unit to `kgCO2e/kg_product`.

The backend currently resolves factors by string labels, so `foodcarbondata.csv` uses English `food_name_en` plus a normalized `lookup_key` instead of French product names.

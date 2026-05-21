<!-- Brief development notes for local and containerized workflows. -->

# Development Notes

The original `restapi/server/yolo/yolo.py` and `weights/yolov11-x-weights-v6.pt` were copied into the new backend layout so the original repo is not modified destructively during the refactor.

The backend loads YOLO weights by resolving the path from `backend/server/yolo/yolo.py`, which avoids path breakage after the directory rename.

`food_carbon_factors` includes starter seed data only. Update the table to match your trained YOLO label names for accurate carbon estimation.

`foodcarbondata.csv` is the normalized union of `foodcarbon.csv` and `food-product.csv`. It keeps only the fields needed for carbon calculation and standardizes the carbon unit to `kgCO2e/kg_product`.

The backend currently resolves factors by string labels, so `foodcarbondata.csv` uses English `food_name_en` plus a normalized `lookup_key` instead of French product names.

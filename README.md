<!-- Project overview, data flow, and startup guide for the food waste carbon system. -->

# food-waste-carbon-system

`food-waste-carbon-system` 是一個廚餘碳排放估算系統。它結合 React 前端、FastAPI 後端、YOLOv11 segmentation 與 PostgreSQL，讓使用者可以上傳餐盤廚餘圖片，輸入整盤重量，並取得每項食物的推估重量與碳排放量。

## 系統目標

- 使用 YOLOv11 segmentation 辨識餐盤中的食物廚餘
- 根據物件面積與 `density_factor` 推估各食物重量
- 根據 `carbon_factor` 計算各項食物碳排放量
- 儲存分析紀錄到 PostgreSQL
- 在 React 前端顯示辨識結果、重量與總碳排

## 專案結構

```text
food-waste-carbon-system/
├── frontend/                   # React + Vite 前端
├── backend/                    # FastAPI + YOLOv11 + SQLAlchemy 後端
├── database/                   # PostgreSQL 初始化 SQL
├── docs/                       # 系統設計與開發說明
├── docker-compose.yml          # 服務編排
├── .env                        # 環境變數
├── .gitignore                  # Git 忽略規則
└── README.md                   # 專案說明
```

## 系統流程

```text
使用者
↓
React 上傳圖片 + total_weight_g
↓
FastAPI /detect
↓
PIL 讀取圖片
↓
YOLOv11 segmentation
↓
取得 detected_objects
    ├── label_name
    ├── confidence
    ├── mask area
    └── box
↓
過濾非食物類別
↓
查詢 food_carbon_factors
↓
area × density_factor
↓
分配總重量
↓
estimated_weight_g / 1000 × carbon_factor
↓
加總 total_carbon_emission_kg
↓
回傳 JSON
↓
React 顯示結果
```

## 偵測與碳排計算邏輯

`backend/routes/detect.py` 會接收圖片與 `total_weight_g`，再呼叫 `backend/server/yolo/yolo.py` 執行 YOLOv11 segmentation。

YOLO 回傳的每個物件至少包含：

- `label_name`
- `confidence`
- `area`
- `box`

後端會先過濾垃圾類別、餐盤與忽略類別，再針對可食物件查詢 `food_carbon_factors`。每個物件會依據 `area × density_factor` 計算相對權重比例，最後把 `total_weight_g` 分配到各個食物項目，得到 `estimated_weight_g`。

碳排計算公式如下：

```text
carbon_emission_kg = estimated_weight_g / 1000 × carbon_factor
```

所有項目的 `carbon_emission_kg` 加總後，得到 `total_carbon_emission_kg`。

## API

### `POST /api/detect`

使用 `multipart/form-data` 傳送：

- `file`: 圖片檔案
- `total_weight_g`: 整盤廚餘重量
- `user_id`: 選填

主要回傳欄位：

- `objects`
- `image_base64`
- `clustering_image_base64`
- `waste_percentage`
- `food_area`
- `garbage_area`
- `plate_area`
- `total_weight_g`
- `total_carbon_emission_kg`
- `matched_item_count`
- `unmatched_item_count`

每個 `object` 目前還會包含：

- `label_name`
- `estimated_weight_g`
- `carbon_factor`
- `carbon_emission_kg`
- `has_carbon_data`
- `factor_source`

如果 `has_carbon_data = false`，代表該食物有被辨識到，但目前沒有對應碳排資料，因此不會被計入 `total_carbon_emission_kg`。

### 其他 API

- `GET /` 健康檢查
- `GET /api/users` 查詢使用者
- `POST /api/users` 建立使用者
- `GET /api/records` 查詢分析紀錄
- `GET /api/records/{record_id}` 查詢單筆分析紀錄

## 資料表

系統使用以下資料表：

- `users`
- `food_carbon_factors`
- `analysis_records`
- `analysis_items`

`food_carbon_factors` 用來提供：

- `yolo_label`
- `food_name_zh`
- `category`
- `carbon_factor`
- `density_factor`
- `source`

## 啟動方式

第一次啟動，或你有修改 `database/init.sql` 想重新匯入資料庫 seed 時，請在專案根目錄執行：

```bash
docker compose down -v
docker compose up --build -d
```

一般重啟服務：

```bash
docker compose down
docker compose up --build -d
```

只重建後端：

```bash
docker compose up --build -d backend
```

啟動後可使用：

- React 前端：`http://localhost:5173`
- FastAPI Swagger 文件：`http://localhost:8000/docs`

如果你要啟用 pgAdmin：

```bash
docker compose --profile tools up -d pgadmin
```

pgAdmin 預設位置：

- `http://localhost:5050`

## 開發備註

- YOLO 權重檔位於 `backend/server/yolo/weights/yolov11-x-weights-v6.pt`
- YOLO 載入邏輯位於 `backend/server/yolo/yolo.py`
- 碳排計算邏輯位於 `backend/services/carbon_calculator.py`
- 因子查詢邏輯位於 `backend/services/food_factor_service.py`
- PostgreSQL 初始化檔位於 `database/init.sql`

## 重新建置提醒

調整 Docker、依賴、資料庫初始化或後端模型後，請重新執行：

```bash
docker compose down
docker compose up --build -d
```

如果變更的是 `database/init.sql`，請改用：

```bash
docker compose down -v
docker compose up --build -d
```

"""Database bootstrap that creates tables from SQLAlchemy models on app startup."""

import logging

from database.db import Base, SessionLocal, engine
from database import models  # noqa: F401

logger = logging.getLogger(__name__)

# NOTE: Carbon factors (kg CO2e per kg food) sourced from FAO & IPCC AR5 estimates.
# Density factors are used to convert pixel area ratios to weight estimates.
SEED_FOOD_FACTORS = [
    {"yolo_label": "rice",              "food_name_zh": "白飯",     "category": "grain",      "carbon_factor": 2.7,   "density_factor": 0.9},
    {"yolo_label": "cabidela rice",     "food_name_zh": "雞肉飯",   "category": "grain",      "carbon_factor": 2.7,   "density_factor": 0.9},
    {"yolo_label": "bread",             "food_name_zh": "麵包",     "category": "grain",      "carbon_factor": 0.98,  "density_factor": 0.4},
    {"yolo_label": "toasted bread",     "food_name_zh": "吐司",     "category": "grain",      "carbon_factor": 0.98,  "density_factor": 0.4},
    {"yolo_label": "pasta",             "food_name_zh": "義大利麵", "category": "grain",      "carbon_factor": 1.0,   "density_factor": 0.7},
    {"yolo_label": "spaghetti",         "food_name_zh": "義大利麵", "category": "grain",      "carbon_factor": 1.0,   "density_factor": 0.7},
    {"yolo_label": "lasagna",           "food_name_zh": "千層麵",   "category": "grain",      "carbon_factor": 2.2,   "density_factor": 0.8},
    {"yolo_label": "chips",             "food_name_zh": "薯片",     "category": "grain",      "carbon_factor": 2.5,   "density_factor": 0.3},
    {"yolo_label": "french fries",      "food_name_zh": "薯條",     "category": "vegetable",  "carbon_factor": 0.69,  "density_factor": 0.5},
    {"yolo_label": "baked potatoes",    "food_name_zh": "烤馬鈴薯", "category": "vegetable",  "carbon_factor": 0.69,  "density_factor": 0.8},
    {"yolo_label": "mashed potatoes",   "food_name_zh": "馬鈴薯泥", "category": "vegetable",  "carbon_factor": 0.69,  "density_factor": 0.9},
    {"yolo_label": "lettuce",           "food_name_zh": "生菜",     "category": "vegetable",  "carbon_factor": 0.36,  "density_factor": 0.2},
    {"yolo_label": "tomato",            "food_name_zh": "番茄",     "category": "vegetable",  "carbon_factor": 1.06,  "density_factor": 0.6},
    {"yolo_label": "vegetables",        "food_name_zh": "蔬菜",     "category": "vegetable",  "carbon_factor": 0.5,   "density_factor": 0.4},
    {"yolo_label": "brocolis",          "food_name_zh": "花椰菜",   "category": "vegetable",  "carbon_factor": 0.4,   "density_factor": 0.3},
    {"yolo_label": "cabbage",           "food_name_zh": "高麗菜",   "category": "vegetable",  "carbon_factor": 0.4,   "density_factor": 0.4},
    {"yolo_label": "carrot",            "food_name_zh": "紅蘿蔔",   "category": "vegetable",  "carbon_factor": 0.42,  "density_factor": 0.7},
    {"yolo_label": "cucumber",          "food_name_zh": "小黃瓜",   "category": "vegetable",  "carbon_factor": 0.5,   "density_factor": 0.55},
    {"yolo_label": "onion",             "food_name_zh": "洋蔥",     "category": "vegetable",  "carbon_factor": 0.38,  "density_factor": 0.6},
    {"yolo_label": "mushrooms",         "food_name_zh": "蘑菇",     "category": "vegetable",  "carbon_factor": 1.05,  "density_factor": 0.35},
    {"yolo_label": "olives",            "food_name_zh": "橄欖",     "category": "vegetable",  "carbon_factor": 1.5,   "density_factor": 0.7},
    {"yolo_label": "asparagus",         "food_name_zh": "蘆筍",     "category": "vegetable",  "carbon_factor": 0.4,   "density_factor": 0.3},
    {"yolo_label": "greens",            "food_name_zh": "青菜",     "category": "vegetable",  "carbon_factor": 0.4,   "density_factor": 0.3},
    {"yolo_label": "beans",             "food_name_zh": "豆子",     "category": "vegetable",  "carbon_factor": 0.9,   "density_factor": 0.7},
    {"yolo_label": "black bean",        "food_name_zh": "黑豆",     "category": "vegetable",  "carbon_factor": 0.9,   "density_factor": 0.75},
    {"yolo_label": "chicken",           "food_name_zh": "雞肉",     "category": "poultry",    "carbon_factor": 5.7,   "density_factor": 1.0},
    {"yolo_label": "chicken steak",     "food_name_zh": "雞排",     "category": "poultry",    "carbon_factor": 5.7,   "density_factor": 1.0},
    {"yolo_label": "turkey steak",      "food_name_zh": "火雞排",   "category": "poultry",    "carbon_factor": 5.0,   "density_factor": 1.0},
    {"yolo_label": "pork",              "food_name_zh": "豬肉",     "category": "meat",       "carbon_factor": 7.6,   "density_factor": 1.0},
    {"yolo_label": "pork belly",        "food_name_zh": "五花肉",   "category": "meat",       "carbon_factor": 7.6,   "density_factor": 1.05},
    {"yolo_label": "pork loin",         "food_name_zh": "豬里肌",   "category": "meat",       "carbon_factor": 7.6,   "density_factor": 1.0},
    {"yolo_label": "pork intestines",   "food_name_zh": "豬大腸",   "category": "meat",       "carbon_factor": 7.6,   "density_factor": 1.0},
    {"yolo_label": "steak",             "food_name_zh": "牛排",     "category": "meat",       "carbon_factor": 27.0,  "density_factor": 1.05},
    {"yolo_label": "grilled steak",     "food_name_zh": "烤牛排",   "category": "meat",       "carbon_factor": 27.0,  "density_factor": 1.05},
    {"yolo_label": "grilled chop",      "food_name_zh": "烤豬排",   "category": "meat",       "carbon_factor": 7.6,   "density_factor": 1.0},
    {"yolo_label": "minced meat",       "food_name_zh": "絞肉",     "category": "meat",       "carbon_factor": 10.0,  "density_factor": 1.05},
    {"yolo_label": "meatballs",         "food_name_zh": "肉丸",     "category": "meat",       "carbon_factor": 8.0,   "density_factor": 1.0},
    {"yolo_label": "cutlet",            "food_name_zh": "肉排",     "category": "meat",       "carbon_factor": 8.0,   "density_factor": 1.0},
    {"yolo_label": "stewed veal",       "food_name_zh": "燉小牛肉", "category": "meat",       "carbon_factor": 20.0,  "density_factor": 1.0},
    {"yolo_label": "steaks with mushrooms", "food_name_zh": "牛排佐蘑菇", "category": "meat", "carbon_factor": 25.0,  "density_factor": 1.0},
    {"yolo_label": "bacon",             "food_name_zh": "培根",     "category": "meat",       "carbon_factor": 7.6,   "density_factor": 0.8},
    {"yolo_label": "ham",               "food_name_zh": "火腿",     "category": "meat",       "carbon_factor": 7.6,   "density_factor": 0.9},
    {"yolo_label": "chorizo",           "food_name_zh": "西班牙香腸", "category": "meat",     "carbon_factor": 7.6,   "density_factor": 0.9},
    {"yolo_label": "breaded",           "food_name_zh": "炸肉排",   "category": "meat",       "carbon_factor": 8.0,   "density_factor": 1.0},
    {"yolo_label": "fish",              "food_name_zh": "魚",       "category": "seafood",    "carbon_factor": 3.5,   "density_factor": 0.9},
    {"yolo_label": "fish hake",         "food_name_zh": "鱈魚",     "category": "seafood",    "carbon_factor": 3.5,   "density_factor": 0.9},
    {"yolo_label": "fried cod",         "food_name_zh": "炸鱈魚",   "category": "seafood",    "carbon_factor": 3.5,   "density_factor": 0.95},
    {"yolo_label": "salmon",            "food_name_zh": "鮭魚",     "category": "seafood",    "carbon_factor": 4.5,   "density_factor": 0.95},
    {"yolo_label": "tuna",              "food_name_zh": "鮪魚",     "category": "seafood",    "carbon_factor": 4.0,   "density_factor": 0.9},
    {"yolo_label": "tuna with mushrooms", "food_name_zh": "鮪魚佐蘑菇", "category": "seafood","carbon_factor": 4.0,   "density_factor": 0.85},
    {"yolo_label": "tuna with pasta",   "food_name_zh": "鮪魚義大利麵", "category": "seafood", "carbon_factor": 3.0,  "density_factor": 0.85},
    {"yolo_label": "mussel",            "food_name_zh": "淡菜",     "category": "seafood",    "carbon_factor": 2.0,   "density_factor": 0.8},
    {"yolo_label": "boiled egg",        "food_name_zh": "水煮蛋",   "category": "egg",        "carbon_factor": 4.8,   "density_factor": 1.0},
    {"yolo_label": "fried egg",         "food_name_zh": "煎蛋",     "category": "egg",        "carbon_factor": 4.8,   "density_factor": 1.0},
    {"yolo_label": "omelet",            "food_name_zh": "歐姆蛋",   "category": "egg",        "carbon_factor": 4.8,   "density_factor": 0.9},
    {"yolo_label": "scrambled eggs",    "food_name_zh": "炒蛋",     "category": "egg",        "carbon_factor": 4.8,   "density_factor": 0.85},
    {"yolo_label": "scrambled eggs with bacon", "food_name_zh": "培根炒蛋", "category": "egg","carbon_factor": 6.0,   "density_factor": 0.9},
    {"yolo_label": "cheese",            "food_name_zh": "起司",     "category": "dairy",      "carbon_factor": 13.5,  "density_factor": 0.9},
    {"yolo_label": "soup",              "food_name_zh": "湯",       "category": "other",      "carbon_factor": 1.0,   "density_factor": 1.0},
    {"yolo_label": "pizza",             "food_name_zh": "披薩",     "category": "other",      "carbon_factor": 4.5,   "density_factor": 0.6},
    {"yolo_label": "cake",              "food_name_zh": "蛋糕",     "category": "other",      "carbon_factor": 3.0,   "density_factor": 0.5},
    {"yolo_label": "cereals",           "food_name_zh": "麥片",     "category": "grain",      "carbon_factor": 1.2,   "density_factor": 0.35},
    {"yolo_label": "gelatin",           "food_name_zh": "果凍",     "category": "other",      "carbon_factor": 0.8,   "density_factor": 1.0},
    {"yolo_label": "apple",             "food_name_zh": "蘋果",     "category": "fruit",      "carbon_factor": 0.43,  "density_factor": 0.75},
    {"yolo_label": "banana",            "food_name_zh": "香蕉",     "category": "fruit",      "carbon_factor": 0.86,  "density_factor": 0.6},
    {"yolo_label": "strawberry",        "food_name_zh": "草莓",     "category": "fruit",      "carbon_factor": 0.63,  "density_factor": 0.6},
    {"yolo_label": "grape",             "food_name_zh": "葡萄",     "category": "fruit",      "carbon_factor": 0.9,   "density_factor": 0.7},
    {"yolo_label": "blueberries",       "food_name_zh": "藍莓",     "category": "fruit",      "carbon_factor": 0.9,   "density_factor": 0.5},
    {"yolo_label": "melon",             "food_name_zh": "哈密瓜",   "category": "fruit",      "carbon_factor": 0.5,   "density_factor": 0.6},
    {"yolo_label": "watermelon",        "food_name_zh": "西瓜",     "category": "fruit",      "carbon_factor": 0.3,   "density_factor": 0.55},
    {"yolo_label": "pineapple",         "food_name_zh": "鳳梨",     "category": "fruit",      "carbon_factor": 0.6,   "density_factor": 0.65},
    {"yolo_label": "lime",              "food_name_zh": "萊姆",     "category": "fruit",      "carbon_factor": 0.6,   "density_factor": 0.65},
    {"yolo_label": "coffee",            "food_name_zh": "咖啡",     "category": "beverage",   "carbon_factor": 10.0,  "density_factor": 1.0},
]


def _seed_food_factors(db) -> None:
    """Insert default food carbon factors if the table is empty."""
    existing_count = db.query(models.FoodCarbonFactor).count()
    if existing_count > 0:
        logger.info("Food factors already seeded (%d rows), skipping.", existing_count)
        return

    for row in SEED_FOOD_FACTORS:
        db.add(models.FoodCarbonFactor(
            yolo_label=row["yolo_label"],
            food_name_zh=row["food_name_zh"],
            category=row["category"],
            carbon_factor=row["carbon_factor"],
            density_factor=row["density_factor"],
            source="FAO/IPCC AR5 default estimates",
        ))
    db.commit()
    logger.info("Seeded %d food carbon factor rows.", len(SEED_FOOD_FACTORS))


def init_database() -> None:
    """Create all tables and seed initial data."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        _seed_food_factors(db)
    finally:
        db.close()


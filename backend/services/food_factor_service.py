"""Food factor lookup service that maps YOLO outputs to DB carbon and density factors."""

from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models import FoodCarbonFactor


class FoodFactorLookupService:
    def __init__(self, db: Session):
        self.db = db

    def resolve_factor(self, detected_object):
        label_name = str(detected_object.get("label_name", "")).strip().lower()
        candidates = [candidate for candidate in [label_name] if candidate]

        label_value = detected_object.get("label", 0)
        if isinstance(label_value, float) and label_value.is_integer():
            candidates.append(str(int(label_value)))
        else:
            candidates.append(str(label_value).strip().lower())

        factor = (
            self.db.query(FoodCarbonFactor)
            .filter(func.lower(FoodCarbonFactor.yolo_label).in_(candidates))
            .order_by(FoodCarbonFactor.food_id.asc())
            .first()
        )

        if factor:
            return {
                "food_name_zh": factor.food_name_zh,
                "category": factor.category,
                "carbon_factor": self._to_float(factor.carbon_factor),
                "density_factor": self._to_float(factor.density_factor, default=1.0),
                "has_carbon_data": True,
                "source": factor.source,
            }

        return {
            "food_name_zh": detected_object.get("label_name", "unknown"),
            "category": "unmapped",
            "carbon_factor": 0.0,
            "density_factor": 1.0,
            "has_carbon_data": False,
            "source": None,
        }

    @staticmethod
    def _to_float(value, default=0.0) -> float:
        if value is None:
            return default
        if isinstance(value, Decimal):
            return float(value)
        return float(value)

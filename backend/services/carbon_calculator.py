"""Carbon calculator that turns YOLO areas plus food factors into weights and emissions."""

from typing import Callable


def estimate_items_and_total(detected_objects, total_weight_g, factor_resolver: Callable, ignored_labels):
    food_items = []
    weighted_area_sum = 0.0

    for obj in detected_objects:
        label = float(obj["label"])
        if label in ignored_labels:
            continue

        factor = factor_resolver(obj)
        density_factor = factor["density_factor"]
        weighted_area = max(obj["area"], 0.0) * max(density_factor, 0.0)
        weighted_area_sum += weighted_area
        food_items.append(
            {
                "yolo_label": str(obj["label_name"]),
                "label": obj["label"],
                "label_name": obj["label_name"],
                "food_name_zh": factor["food_name_zh"],
                "category": factor["category"],
                "confidence": obj["confidence"],
                "box": obj["box"],
                "area": obj["area"],
                "density_factor": density_factor,
                "carbon_factor": factor["carbon_factor"],
                "has_carbon_data": factor["has_carbon_data"],
                "factor_source": factor["source"],
                "weighted_area": weighted_area,
            }
        )

    total_carbon_emission_kg = 0.0
    if weighted_area_sum <= 0:
        weighted_area_sum = sum(item["area"] for item in food_items) or 1.0
        for item in food_items:
            item["weighted_area"] = item["area"]

    for item in food_items:
        estimated_weight_g = total_weight_g * (item["weighted_area"] / weighted_area_sum)
        carbon_emission_kg = 0.0
        if item["has_carbon_data"]:
            carbon_emission_kg = (estimated_weight_g / 1000.0) * item["carbon_factor"]
        item["estimated_weight_g"] = round(estimated_weight_g, 2)
        item["carbon_emission_kg"] = round(carbon_emission_kg, 6)
        total_carbon_emission_kg += carbon_emission_kg
        item.pop("weighted_area", None)

    return food_items, round(total_carbon_emission_kg, 6)

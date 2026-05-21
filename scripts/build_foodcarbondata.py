"""Build a normalized carbon-factor dataset from foodcarbon.csv and food-product.csv."""

from __future__ import annotations

import csv
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FOODCARBON_PATH = ROOT / "foodcarbon.csv"
FOOD_PRODUCT_PATH = ROOT / "food-product.csv"
OUTPUT_PATH = ROOT / "foodcarbondata.csv"


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    normalized = normalized.lower().strip()
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized)
    return normalized.strip("_")


def build_food_product_rows():
    rows = []
    with FOOD_PRODUCT_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            food_name_en = row["Entity"].strip()
            rows.append(
                {
                    "source_dataset": "food-product",
                    "source_id": slugify(f"{food_name_en}_{row['Year'].strip()}"),
                    "lookup_key": slugify(food_name_en),
                    "food_name_en": food_name_en,
                    "food_name_zh": "",
                    "food_name_fr": "",
                    "carbon_factor_kgco2e_per_kg": f"{float(row['Greenhouse gas emissions per kilogram']):.6f}",
                    "carbon_unit": "kgCO2e/kg_product",
                    "source_year": row["Year"].strip(),
                    "source_name_raw": food_name_en,
                }
            )
    return rows


def build_foodcarbon_rows():
    rows = []
    with FOODCARBON_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            food_name_fr = row["Nom du Produit en Français"].strip()
            food_name_en = row["LCI Name"].strip() or food_name_fr
            rows.append(
                {
                    "source_dataset": "foodcarbon",
                    "source_id": row["Code AGB"].strip(),
                    "lookup_key": slugify(food_name_en),
                    "food_name_en": food_name_en,
                    "food_name_zh": "",
                    "food_name_fr": food_name_fr,
                    "carbon_factor_kgco2e_per_kg": f"{float(row['Changement climatique']):.6f}",
                    "carbon_unit": "kgCO2e/kg_product",
                    "source_year": "",
                    "source_name_raw": food_name_fr,
                }
            )
    return rows


def main():
    rows = build_food_product_rows() + build_foodcarbon_rows()
    rows.sort(key=lambda item: (item["lookup_key"], item["source_dataset"], item["source_id"]))

    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "source_dataset",
                "source_id",
                "lookup_key",
                "food_name_en",
                "food_name_zh",
                "food_name_fr",
                "carbon_factor_kgco2e_per_kg",
                "carbon_unit",
                "source_year",
                "source_name_raw",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

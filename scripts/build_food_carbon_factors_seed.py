"""Build a carbon-factor seed from detectable YOLO labels and curated foodcarbon mappings."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DETECTABLE_LABELS_PATH = ROOT / "database" / "detectable_food_labels.csv"
FOODCARBONDATA_PATH = ROOT / "foodcarbondata.csv"
SEED_OUTPUT_PATH = ROOT / "database" / "food_carbon_factors_seed.csv"
UNMATCHED_OUTPUT_PATH = ROOT / "database" / "unmatched_labels.csv"


ALIAS_MAP = {
    "apple": ("apples", "fruit", "Mapped to the general Apples commodity from food-product."),
    "asparagus": ("asparagus_green_raw", "vegetable", "Mapped to a raw asparagus entry."),
    "bacon": ("bacon_back", "meat", "Mapped to the closest direct bacon entry."),
    "baked potatoes": ("potato_roasted_baked", "starch", "Mapped to roasted/baked potato."),
    "banana": ("bananas", "fruit", "Mapped to the general Bananas commodity from food-product."),
    "beans": ("broad_bean_cooked", "vegetable", "Mapped to broad bean, cooked."),
    "black bean": ("broad_bean_cooked", "vegetable", "Mapped to broad bean, cooked, as the chosen bean proxy."),
    "blueberries": ("blueberry_raw", "fruit", "Mapped to raw blueberry."),
    "boiled egg": ("egg_hard_boiled", "egg", "Mapped to hard-boiled egg."),
    "bread": ("bread_french_bread_baguette", "starch", "Mapped to plain baguette bread."),
    "breaded": ("chicken_nugget_breaded_croquette", "meat", "Mapped to breaded chicken nugget as the chosen breaded-item proxy."),
    "brocolis": ("broccoli_raw", "vegetable", "Mapped by spelling normalization from brocolis to broccoli."),
    "cabbage": ("green_cabbage_raw", "vegetable", "Mapped to raw green cabbage."),
    "cabidela rice": ("rice", "starch", "Mapped to generic rice."),
    "cake": ("brownie_chocolate_cake", "dessert", "Mapped to brownie chocolate cake as the chosen cake proxy."),
    "carrot": ("carrot_raw", "vegetable", "Mapped to raw carrot."),
    "cereals": ("breakfast_cereals_corn_flakes_plain_fortified_with_vitamins_and_chemical_elements", "starch", "Mapped to plain corn-flakes breakfast cereals."),
    "cheese": ("cheese", "dairy", "Exact commodity match from food-product."),
    "chicken": ("chicken_breast_without_skin_raw", "meat", "Mapped to raw chicken breast without skin."),
    "chicken steak": ("chicken_breast_without_skin_raw", "meat", "Mapped to the closest chicken cut entry."),
    "chips": ("french_fries_or_chips_frozen_deep_fried", "starch", "Mapped to deep-fried French fries/chips."),
    "chorizo": ("salami_pure_pork", "meat", "Mapped to pure pork salami as the chosen chorizo proxy."),
    "coffee": ("coffee", "beverage", "Exact commodity match from food-product."),
    "cucumber": ("cucumber_pulp_and_peel_raw", "vegetable", "Mapped to raw cucumber with peel."),
    "cutlet": ("lamb_cutlet_grilled", "meat", "Mapped to grilled lamb cutlet."),
    "fish": ("fish_farmed", "seafood", "Mapped to the generic Fish (farmed) commodity from food-product."),
    "fish hake": ("european_hake_raw", "seafood", "Mapped to raw European hake."),
    "french fries": ("french_fries_or_chips_frozen_deep_fried", "starch", "Mapped to deep-fried French fries."),
    "fried cod": ("cod_raw", "seafood", "Mapped to cod as the closest direct species entry."),
    "fried egg": ("egg_fried_without_added_fat", "egg", "Mapped to fried egg without added fat."),
    "gelatin": ("gelatine_dried", "dessert", "Mapped by spelling normalization from gelatin to gelatine."),
    "grape": ("grape_raw", "fruit", "Mapped to raw grape."),
    "greens": ("green_cabbage_raw", "vegetable", "Mapped to raw green cabbage as the chosen greens proxy."),
    "grilled chop": ("pork_chop_grilled", "meat", "Mapped to grilled pork chop."),
    "grilled steak": ("beef_rump_steak_grilled", "meat", "Mapped to grilled beef rump steak."),
    "ham": ("cooked_ham_choice", "meat", "Mapped to cooked ham, choice."),
    "lasagna": ("lasagna_or_cannelloni_with_meat_bolognese_sauce", "prepared_meal", "Mapped to meat lasagna / cannelloni with bolognese sauce."),
    "lettuce": ("lettuce_raw", "vegetable", "Mapped to raw lettuce."),
    "lime": ("lime_pulp_raw", "fruit", "Mapped to raw lime pulp."),
    "mashed potatoes": ("mashed_potatoes_w_fresh_tome_cheese", "starch", "Mapped to mashed potatoes with fresh tome cheese."),
    "meatballs": ("beef_meat_balls_cooked", "meat", "Mapped to cooked beef meat balls."),
    "melon": ("melon_cantaloupe_ex_cavaillon_or_charentais_melon_pulp_raw", "fruit", "Mapped to raw cantaloupe melon pulp."),
    "minced meat": ("poultry_minced_meat", "meat", "Mapped to poultry minced meat."),
    "mussel": ("mediterranean_mussel_raw", "seafood", "Mapped to raw Mediterranean mussel."),
    "omelet": ("omelette_with_cheese", "egg", "Mapped to omelette with cheese."),
    "onion": ("onion_raw", "vegetable", "Mapped to raw onion."),
    "pasta": ("dried_pasta_raw", "starch", "Mapped to generic dried pasta."),
    "pineapple": ("pineapple_pulp_raw", "fruit", "Mapped to raw pineapple pulp."),
    "pizza": ("pizza_cheese_and_tomato_or_margherita_pizza", "prepared_meal", "Mapped to cheese and tomato / Margherita pizza."),
    "pork": ("cooked_pork_shoulder_choice", "meat", "Mapped to cooked pork shoulder, choice."),
    "pork belly": ("pork_belly_raw", "meat", "Mapped to raw pork belly."),
    "pork loin": ("pork_loin_raw", "meat", "Mapped to raw pork loin."),
    "rice": ("rice", "starch", "Exact commodity match from food-product."),
    "salmon": ("salmon_raw_farmed", "seafood", "Mapped to raw farmed salmon."),
    "scrambled eggs": ("egg_scrambled_with_added_fat", "egg", "Mapped to scrambled egg with added fat."),
    "scrambled eggs with bacon": ("egg_scrambled_with_added_fat", "egg", "Mapped to scrambled egg with added fat as the chosen proxy for scrambled eggs with bacon."),
    "soup": ("soup_chicken_and_vegetables_prepacked_to_be_reheated", "prepared_meal", "Mapped to prepacked chicken and vegetables soup."),
    "spaghetti": ("bolognese_style_pasta_spaghetti_tagliatelle", "prepared_meal", "Mapped to bolognese-style pasta (spaghetti/tagliatelle)."),
    "steak": ("beef_flank_steak_grilled_pan_fried", "meat", "Mapped to grilled/pan-fried beef flank steak."),
    "steaks with mushrooms": ("beef_flank_steak_grilled_pan_fried", "meat", "Mapped to grilled/pan-fried beef flank steak as the chosen base for steaks with mushrooms."),
    "stewed veal": ("veal_escalope_cooked", "meat", "Mapped to cooked veal escalope."),
    "strawberry": ("strawberry_raw", "fruit", "Mapped to raw strawberry."),
    "toasted bread": ("toasted_bread_home_made", "starch", "Mapped to home-made toasted bread."),
    "tomato": ("tomato_raw", "vegetable", "Mapped to raw tomato."),
    "tuna": ("skipjack_tuna_raw", "seafood", "Mapped to raw skipjack tuna."),
    "turkey steak": ("turkey_escalope_raw", "meat", "Mapped to raw turkey escalope."),
    "vegetables": ("diced_mixed_vegetables_canned_drained", "vegetable", "Mapped to diced mixed vegetables, canned, drained."),
    "watermelon": ("watermelon_pulp_raw", "fruit", "Mapped to raw watermelon pulp."),
}

SKIP_LABELS = {
    "mushrooms",
    "olives",
    "pork intestines",
    "tuna with mushrooms",
    "tuna with pasta",
}


def load_foodcarbon_lookup():
    with FOODCARBONDATA_PATH.open("r", encoding="utf-8", newline="") as handle:
        return {row["lookup_key"]: row for row in csv.DictReader(handle)}


def load_detectable_labels():
    with DETECTABLE_LABELS_PATH.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_outputs():
    carbon_lookup = load_foodcarbon_lookup()
    labels = load_detectable_labels()
    matched_rows = []
    unmatched_rows = []

    for label in labels:
        label_name = label["label_name"]
        alias = ALIAS_MAP.get(label_name)

        if alias is None:
            reason = "Skipped by manual decision." if label_name in SKIP_LABELS else "No conservative one-to-one mapping was defined for this YOLO label."
            unmatched_rows.append(
                {
                    "label_id": label["label_id"],
                    "label_name": label_name,
                    "reason": reason,
                }
            )
            continue

        lookup_key, category, match_note = alias
        carbon_row = carbon_lookup.get(lookup_key)
        if carbon_row is None:
            unmatched_rows.append(
                {
                    "label_id": label["label_id"],
                    "label_name": label_name,
                    "reason": f"Mapped lookup_key '{lookup_key}' was not found in foodcarbondata.csv.",
                }
            )
            continue

        matched_rows.append(
            {
                "label_id": label["label_id"],
                "yolo_label": label_name,
                "food_name_en": carbon_row["food_name_en"],
                "food_name_zh": carbon_row["food_name_en"],
                "category": category,
                "carbon_factor": carbon_row["carbon_factor_kgco2e_per_kg"],
                "density_factor": "1.0",
                "source": f"{carbon_row['source_dataset']}:{carbon_row['source_id']}",
                "matched_lookup_key": carbon_row["lookup_key"],
                "carbon_unit": carbon_row["carbon_unit"],
                "match_note": match_note,
            }
        )

    return matched_rows, unmatched_rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    matched_rows, unmatched_rows = build_outputs()
    write_csv(
        SEED_OUTPUT_PATH,
        [
            "label_id",
            "yolo_label",
            "food_name_en",
            "food_name_zh",
            "category",
            "carbon_factor",
            "density_factor",
            "source",
            "matched_lookup_key",
            "carbon_unit",
            "match_note",
        ],
        matched_rows,
    )
    write_csv(
        UNMATCHED_OUTPUT_PATH,
        ["label_id", "label_name", "reason"],
        unmatched_rows,
    )
    print(f"Wrote {len(matched_rows)} matched rows to {SEED_OUTPUT_PATH}")
    print(f"Wrote {len(unmatched_rows)} unmatched rows to {UNMATCHED_OUTPUT_PATH}")


if __name__ == "__main__":
    main()

import pandas as pd
from statsmodels.stats.contingency_tables import mcnemar
from scipy.stats import chi2_contingency
import numpy as np

EASTERN_IMAGES = [
    'noodles_clam_hard_028.jpeg', 'chayote_leaves_carrot_easy_017.jpeg',
    'bibimbap_veggies_hard_022.jpeg', 'pepper_dried_tofu_easy_010.jpeg',
    'fried_noodles_beef_hard_024.jpeg', 'green_pepper_meat_easy_021.jpeg',
    'seafood_steamed_egg_hard_003.jpeg', 'green_pepper_onion_meat_easy_020.jpeg',
    'leek_dried_tofu_easy_016.jpeg', 'tteokbokki_beef_hard_023.jpeg',
    'century_egg_tofu_hard_009.jpeg', 'carrot_scrambled_egg_easy_005.png',
    'dumplings_easy_025.jpeg', 'mapo_tofu_easy_006.jpeg',
    'rice_noodles_mushroom_hard_030.jpeg', 'grilled_mackerel_easy_011.jpeg'
]

WESTERN_IMAGES = [
    'sausage_salad_hard_018.jpeg', 'potato_salad_leftover_easy_001.webp',
    'steak_bread_egg_easy_026.jpeg', 'avocado_toast_easy_013.jpeg',
    'asparagus_meat_tomato_easy_019.jpeg', 'veggie_fruit_salad_hard_015.jpeg',
    'steak_zucchini_mushroom_easy_027.jpeg', 'sandwich_hard_012.jpeg',
    'potato_broccoli_easy_008.jpeg', 'waffle_cookie_easy_029.jpeg',
    'pasta_sardine_hard_014.jpeg', 'miso_pasta_hard_007.jpeg',
    'shrimp_asparagus_easy_004.jpeg', 'chicken_breast_easy_002.jpeg'
]

def get_culture(filename):
    if filename in EASTERN_IMAGES: return 'Eastern'
    elif filename in WESTERN_IMAGES: return 'Western'
    return 'Unknown'

def main():
    df_gpt = pd.read_csv('experiments/results_yolo_gpt.csv', encoding='utf-8')
    df_gemini = pd.read_csv('experiments/results_yolo_gemini.csv', encoding='utf-8')
    
    yolo_corr = df_gpt['yolo_label_correct'].astype(int).values
    gpt_corr = df_gpt['vlm_label_correct'].astype(int).values
    gemini_corr = df_gemini['vlm_label_correct'].astype(int).values

    print("1. McNemar's Test: YOLO vs GPT-4o")
    # Table: 
    #                GPT Correct  |  GPT Incorrect
    # YOLO Correct        A       |        B
    # YOLO Incorrect      C       |        D
    a = sum((yolo_corr == 1) & (gpt_corr == 1))
    b = sum((yolo_corr == 1) & (gpt_corr == 0))
    c = sum((yolo_corr == 0) & (gpt_corr == 1))
    d = sum((yolo_corr == 0) & (gpt_corr == 0))
    table_gpt = [[a, b], [c, d]]
    res_gpt = mcnemar(table_gpt, exact=False, correction=True)
    print(f"Table: {table_gpt}, p-value = {res_gpt.pvalue:.4f}")

    print("\n2. McNemar's Test: YOLO vs Gemini 2.5")
    a2 = sum((yolo_corr == 1) & (gemini_corr == 1))
    b2 = sum((yolo_corr == 1) & (gemini_corr == 0))
    c2 = sum((yolo_corr == 0) & (gemini_corr == 1))
    d2 = sum((yolo_corr == 0) & (gemini_corr == 0))
    table_gemini = [[a2, b2], [c2, d2]]
    res_gemini = mcnemar(table_gemini, exact=False, correction=True)
    print(f"Table: {table_gemini}, p-value = {res_gemini.pvalue:.4f}")

    print("\n3. Chi-Square Test: Culture vs GPT-4o Accuracy")
    df_gpt['culture'] = df_gpt['image_filename'].apply(get_culture)
    east_corr = df_gpt[(df_gpt['culture'] == 'Eastern') & (df_gpt['vlm_label_correct'] == 1)].shape[0]
    east_incorr = df_gpt[(df_gpt['culture'] == 'Eastern') & (df_gpt['vlm_label_correct'] == 0)].shape[0]
    west_corr = df_gpt[(df_gpt['culture'] == 'Western') & (df_gpt['vlm_label_correct'] == 1)].shape[0]
    west_incorr = df_gpt[(df_gpt['culture'] == 'Western') & (df_gpt['vlm_label_correct'] == 0)].shape[0]
    
    obs = np.array([[east_corr, east_incorr], [west_corr, west_incorr]])
    chi2, p, dof, ex = chi2_contingency(obs)
    print(f"Table (Correct/Incorrect for East/West): \n{obs}")
    print(f"Chi2 = {chi2:.4f}, p-value = {p:.4f}")

if __name__ == "__main__":
    main()

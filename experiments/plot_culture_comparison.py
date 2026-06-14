import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 定義東西方飲食分類
EASTERN_IMAGES = [
    'noodles_clam_hard_028.jpeg',
    'chayote_leaves_carrot_easy_017.jpeg',
    'bibimbap_veggies_hard_022.jpeg',
    'pepper_dried_tofu_easy_010.jpeg',
    'fried_noodles_beef_hard_024.jpeg',
    'green_pepper_meat_easy_021.jpeg',
    'seafood_steamed_egg_hard_003.jpeg',
    'green_pepper_onion_meat_easy_020.jpeg',
    'leek_dried_tofu_easy_016.jpeg',
    'tteokbokki_beef_hard_023.jpeg',
    'century_egg_tofu_hard_009.jpeg',
    'carrot_scrambled_egg_easy_005.png',
    'dumplings_easy_025.jpeg',
    'mapo_tofu_easy_006.jpeg',
    'rice_noodles_mushroom_hard_030.jpeg',
    'grilled_mackerel_easy_011.jpeg'
]

WESTERN_IMAGES = [
    'sausage_salad_hard_018.jpeg',
    'potato_salad_leftover_easy_001.webp',
    'steak_bread_egg_easy_026.jpeg',
    'avocado_toast_easy_013.jpeg',
    'asparagus_meat_tomato_easy_019.jpeg',
    'veggie_fruit_salad_hard_015.jpeg',
    'steak_zucchini_mushroom_easy_027.jpeg',
    'sandwich_hard_012.jpeg',
    'potato_broccoli_easy_008.jpeg',
    'waffle_cookie_easy_029.jpeg',
    'pasta_sardine_hard_014.jpeg',
    'miso_pasta_hard_007.jpeg',
    'shrimp_asparagus_easy_004.jpeg',
    'chicken_breast_easy_002.jpeg'
]

def get_culture(filename):
    if filename in EASTERN_IMAGES:
        return 'Eastern (亞洲/中式)'
    elif filename in WESTERN_IMAGES:
        return 'Western (西式)'
    return 'Unknown'

def main():
    # 讀取 GPT 和 Gemini 的結果
    df_gpt = pd.read_csv('experiments/results_yolo_gpt.csv', encoding='utf-8')
    df_gpt['culture'] = df_gpt['image_filename'].apply(get_culture)
    
    df_gemini = pd.read_csv('experiments/results_yolo_gemini.csv', encoding='utf-8')
    df_gemini['culture'] = df_gemini['image_filename'].apply(get_culture)
    
    # 計算 YOLO 和 VLM 在不同文化的準確率
    results = []
    for culture in ['Eastern (亞洲/中式)', 'Western (西式)']:
        sub_gpt = df_gpt[df_gpt['culture'] == culture]
        sub_gemini = df_gemini[df_gemini['culture'] == culture]
        total = len(sub_gpt)
        if total == 0:
            continue
            
        yolo_correct = sub_gpt['yolo_label_correct'].astype(int).sum()
        gpt_correct = sub_gpt['vlm_label_correct'].astype(int).sum()
        gemini_correct = sub_gemini['vlm_label_correct'].astype(int).sum()
        
        yolo_acc = (yolo_correct / total) * 100
        gemini_acc = (gemini_correct / total) * 100
        gpt_acc = (gpt_correct / total) * 100
        
        results.append({'Culture': culture, 'Model': 'YOLO Only', 'Accuracy': yolo_acc})
        results.append({'Culture': culture, 'Model': 'YOLO + Gemini', 'Accuracy': gemini_acc})
        results.append({'Culture': culture, 'Model': 'YOLO + GPT-4o', 'Accuracy': gpt_acc})
        
        print(f"[{culture}] Total items: {total}")
        print(f"  - YOLO Acc: {yolo_acc:.1f}%")
        print(f"  - Gemini Acc: {gemini_acc:.1f}%")
        print(f"  - GPT-4o Acc: {gpt_acc:.1f}%")
        
    df_results = pd.DataFrame(results)

    # 建立分組長條圖
    plt.figure(figsize=(11, 6))
    
    ax = sns.barplot(x='Culture', y='Accuracy', hue='Model', data=df_results, palette=["#3498db", "#f1c40f", "#2ecc71"])

    plt.title("Accuracy Comparison: Eastern vs. Western Food", fontsize=16, pad=20, fontweight='bold')
    plt.ylabel("Accuracy (%)", fontsize=14)
    plt.xlabel("Cuisine Type", fontsize=14)
    plt.ylim(0, 100)
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 標示數值
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.1f}%", 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 10), 
                    textcoords='offset points',
                    fontsize=12, fontweight='bold')

    plt.legend(title='Model', fontsize=12, title_fontsize=12)

    # 儲存圖表
    out_path = Path("experiments/culture_comparison_chart.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    print(f"Chart saved to {out_path}")

if __name__ == "__main__":
    main()

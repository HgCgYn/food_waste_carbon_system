import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

def main():
    # 最終準確率數據
    models = ['YOLO Only', 'YOLO + Gemini 2.5 Flash', 'YOLO + GPT-4o']
    accuracies = [26.5, 42.2, 44.1]

    # 建立長條圖
    plt.figure(figsize=(9, 6))
    
    # 這裡刻意不用 seaborn 的預設 theme，避免中文字型被洗掉
    sns.barplot(x=models, y=accuracies, hue=models, palette=["#3498db", "#f1c40f", "#2ecc71"], legend=False)

    plt.title("Object-level Label Accuracy (102 objects / 30 images)", fontsize=16, pad=20, fontweight='bold')
    plt.ylabel("Accuracy (%)", fontsize=14)
    plt.xlabel("Model Configuration", fontsize=14)
    plt.ylim(0, 100)
    
    # 加上隔線
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 在柱狀圖上方標示數值
    ax = plt.gca()
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.1f}%", 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 10), 
                    textcoords='offset points',
                    fontsize=12, fontweight='bold')

    # 儲存圖表
    out_path = Path("experiments/accuracy_chart.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    print(f"Chart saved to {out_path}")

if __name__ == "__main__":
    main()

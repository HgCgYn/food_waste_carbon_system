import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import os

def draw_yolo_box(ax, x, y, w, h, label, conf, color='#3498db'):
    bbox = patches.Rectangle((x, y), w, h, linewidth=3, edgecolor=color, facecolor='none')
    ax.add_patch(bbox)
    
    text_str = f"{label} {conf:.2f}"
    text_w = len(text_str) * 12
    text_h = 24
    
    label_bg = patches.Rectangle((x, y - text_h), text_w, text_h, linewidth=1, edgecolor=color, facecolor=color)
    ax.add_patch(label_bg)
    ax.text(x + 5, y - text_h/2, text_str, va='center', ha='left', fontsize=12, color='white', fontweight='bold', fontfamily='sans-serif')

def create_real_pipeline_diagram():
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False

    fig, axes = plt.subplots(1, 4, figsize=(24, 6))
    fig.patch.set_facecolor('#ffffff')
    
    titles = [
        "1. 餐盤影像輸入\n(Edge Device)", 
        "2. YOLO 初判 (低信心)\nConfidence < 0.7", 
        "3. VLM 視覺糾錯\n(Red Box Prompting)", 
        "4. 最終辨識結果與比對\n(Label Evaluation)"
    ]
    
    img_path = 'experiments/test_images/century_egg_tofu_hard_009.jpeg'
    img = Image.open(img_path)
    img_w, img_h = img.size
    
    for i, ax in enumerate(axes):
        ax.set_title(titles[i], fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        
        if i < 3:
            ax.imshow(img)
            
            if i == 0:
                pass
                
            elif i == 1:
                # YOLO misidentifies Century Egg as Meat/Pork
                box_x, box_y, box_w, box_h = img_w*0.3, img_h*0.3, img_w*0.5, img_h*0.5
                draw_yolo_box(ax, box_x, box_y, box_w, box_h, 'pork', 0.41, color='#e67e22')
                
            elif i == 2:
                # VLM Red Box
                box_x, box_y, box_w, box_h = img_w*0.3, img_h*0.3, img_w*0.5, img_h*0.5
                bbox = patches.Rectangle((box_x, box_y), box_w, box_h, linewidth=6, edgecolor='#e74c3c', facecolor='none')
                ax.add_patch(bbox)
                
                # CoT Text overlay
                cot_text = "Prompt: 這是什麼食物？\nCoT: 黑色的部分具有果凍狀光澤，\n且與豆腐搭配，應為皮蛋豆腐...\nResult: century egg, tofu"
                ax.text(img_w/2, box_y - 80, cot_text, ha='center', fontsize=12, color='black', bbox=dict(facecolor='#f1c40f', alpha=0.9, boxstyle='round,pad=0.5'))
                
        else: # Stage 4: Evaluation
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            receipt = patches.Rectangle((1, 1), 8, 8, linewidth=2, edgecolor='#bdc3c7', facecolor='#f8f9fa')
            ax.add_patch(receipt)
            
            lines = [
                ("--- 辨識結果比對 ---", 8, 'bold', '#2c3e50'),
                ("【Ground Truth】", 6.5, 'bold', '#7f8c8d'),
                ("1. 皮蛋 (Century Egg)", 5.8, 'normal', '#2c3e50'),
                ("2. 豆腐 (Tofu)", 5.2, 'normal', '#2c3e50'),
                ("【YOLO 預測】", 4.0, 'bold', '#7f8c8d'),
                ("1. 豬肉 (Pork) [FAIL]", 3.3, 'normal', '#e74c3c'),
                ("【VLM 糾錯後輸出】", 2.1, 'bold', '#7f8c8d'),
                ("1. 皮蛋、豆腐 [SUCCESS]", 1.4, 'bold', '#27ae60')
            ]
            for text, y, weight, color in lines:
                ax.text(5, y, text, ha='center', fontsize=14, fontweight=weight, color=color)

    for i in range(3):
        fig.add_artist(patches.ConnectionPatch(
            xyA=(1.05, 0.5), xyB=(-0.05, 0.5), coordsA=axes[i].transAxes, coordsB=axes[i+1].transAxes,
            arrowstyle="->", color="#95a5a6", linewidth=4, mutation_scale=30
        ))
        
    plt.tight_layout()
    plt.savefig('experiments/pipeline_demo_real.png', dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    create_real_pipeline_diagram()

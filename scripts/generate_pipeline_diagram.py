import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
import os

def create_pipeline_diagram():
    # Use a basic font
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False

    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    fig.patch.set_facecolor('#f8f9fa')
    
    titles = [
        "1. 餐盤影像輸入\n(Edge Device)", 
        "2. YOLO 初判 (低信心)\nConfidence < 0.7", 
        "3. VLM 視覺糾錯\n(Red Box Prompting)", 
        "4. 碳排與罰款結算\n(Cloud Database)"
    ]
    
    for i, ax in enumerate(axes):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        ax.set_title(titles[i], fontsize=14, fontweight='bold', pad=15)
        
        # Draw a mock plate
        if i < 3:
            plate = patches.Circle((5, 5), 4, edgecolor='#bdc3c7', facecolor='#ffffff', linewidth=3)
            ax.add_patch(plate)
            
            # Draw mock food items
            food1 = patches.Ellipse((4, 6), 3, 2, angle=30, edgecolor='none', facecolor='#e74c3c', alpha=0.8) # Meat
            food2 = patches.Ellipse((6, 4), 2.5, 2.5, edgecolor='none', facecolor='#2ecc71', alpha=0.8) # Veggie
            ax.add_patch(food1)
            ax.add_patch(food2)
            
            if i == 0:
                ax.text(5, 1, "Raw Image Capture", ha='center', fontsize=12, color='#7f8c8d')
                
            elif i == 1:
                # YOLO Bounding Box
                bbox = patches.Rectangle((2.5, 4.5), 3, 3, linewidth=2, edgecolor='#3498db', facecolor='none', linestyle='--')
                ax.add_patch(bbox)
                ax.text(4, 7.8, "tomato? (Conf: 0.42)", ha='center', fontsize=10, color='#3498db', bbox=dict(facecolor='white', alpha=0.7))
                ax.text(5, 1, "Edge AI Processing", ha='center', fontsize=12, color='#7f8c8d')
                
            elif i == 2:
                # VLM Red Box
                bbox = patches.Rectangle((2.5, 4.5), 3, 3, linewidth=4, edgecolor='#e74c3c', facecolor='none')
                ax.add_patch(bbox)
                
                # CoT Text
                cot_text = "Prompt: 這是什麼？\nCoT: 紋理似牛肉片...\nResult: Beef"
                ax.text(5, 8.5, cot_text, ha='center', fontsize=10, color='#2c3e50', bbox=dict(facecolor='#f1c40f', alpha=0.8, boxstyle='round,pad=0.5'))
                ax.text(5, 1, "Cloud VLM API", ha='center', fontsize=12, color='#7f8c8d')
                
        else: # Stage 4: Receipt
            receipt = patches.Rectangle((2, 1), 6, 8, linewidth=2, edgecolor='#bdc3c7', facecolor='#ffffff')
            ax.add_patch(receipt)
            
            lines = [
                ("--- 剩食碳排結算 ---", 8),
                ("項目: 牛肉 (Beef)", 6.5),
                ("重量: 120g", 5.5),
                ("碳排: 3,240 gCO2e", 4.5),
                ("-------------------", 3.5),
                ("環境罰金: $32 NTD", 2.5)
            ]
            for text, y in lines:
                weight = 'bold' if '罰金' in text else 'normal'
                color = '#e74c3c' if '罰金' in text else '#2c3e50'
                ax.text(5, y, text, ha='center', fontsize=12, fontweight=weight, color=color)

    # Draw arrows between axes
    for i in range(3):
        fig.add_artist(patches.ConnectionPatch(
            xyA=(10, 5), xyB=(0, 5), coordsA=axes[i].transData, coordsB=axes[i+1].transData,
            arrowstyle="->", color="#95a5a6", linewidth=3, mutation_scale=20
        ))
        
    plt.tight_layout()
    plt.savefig('experiments/pipeline_demo.png', dpi=300, bbox_inches='tight')
    print("Pipeline diagram saved to experiments/pipeline_demo.png")

if __name__ == "__main__":
    create_pipeline_diagram()

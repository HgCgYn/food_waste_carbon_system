import matplotlib.pyplot as plt
from PIL import Image
import os

def create_dataset_examples():
    # Use a basic font
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.patch.set_facecolor('#ffffff')
    
    examples = [
        {
            'img': 'experiments/test_images/dumplings_easy_025.jpeg',
            'title': '【東方 / 簡單場景】\n(Eastern / Easy)',
            'gt': 'Ground Truth: 水餃 (Dumplings)',
            'desc': '單一且完整的食物外觀，未受遮擋'
        },
        {
            'img': 'experiments/test_images/avocado_toast_easy_013.jpeg',
            'title': '【西方 / 簡單場景】\n(Western / Easy)',
            'gt': 'Ground Truth: 酪梨 (Avocado), 吐司 (Toast)',
            'desc': '特徵明顯的西式輕食，光線良好'
        },
        {
            'img': 'experiments/test_images/century_egg_tofu_hard_009.jpeg',
            'title': '【東方 / 困難場景】\n(Eastern / Hard)',
            'gt': 'Ground Truth: 皮蛋 (Century Egg), 豆腐 (Tofu)',
            'desc': '外觀深色難辨識，且與豆腐互相堆疊干擾'
        },
        {
            'img': 'experiments/test_images/pasta_sardine_hard_014.jpeg',
            'title': '【西方 / 困難場景】\n(Western / Hard)',
            'gt': 'Ground Truth: 義大利麵 (Pasta), 沙丁魚 (Sardine)',
            'desc': '沙丁魚與麵條、醬汁嚴重混雜，殘渣破碎'
        }
    ]
    
    axes = axes.flatten()
    for i, ax in enumerate(axes):
        ex = examples[i]
        try:
            img = Image.open(ex['img'])
            ax.imshow(img)
        except Exception as e:
            # Fallback if image is missing
            ax.text(0.5, 0.5, 'Image not found', ha='center', va='center', transform=ax.transAxes)
            
        ax.set_title(ex['title'], fontsize=18, fontweight='bold', pad=15)
        ax.axis('off')
        
        # Add labels below the image
        # To do this cleanly, we can add a text box inside the image at the bottom
        img_w, img_h = img.size
        # Background rect for text
        box_h = img_h * 0.15
        import matplotlib.patches as patches
        rect = patches.Rectangle((0, img_h - box_h), img_w, box_h, linewidth=0, edgecolor='none', facecolor='black', alpha=0.7)
        ax.add_patch(rect)
        
        ax.text(img_w*0.02, img_h - box_h*0.65, ex['gt'], fontsize=16, color='#2ecc71', fontweight='bold', ha='left')
        ax.text(img_w*0.02, img_h - box_h*0.25, ex['desc'], fontsize=14, color='white', ha='left')

    plt.tight_layout()
    plt.savefig('experiments/dataset_examples.png', dpi=300, bbox_inches='tight')
    print("Dataset examples saved to experiments/dataset_examples.png")

if __name__ == "__main__":
    create_dataset_examples()

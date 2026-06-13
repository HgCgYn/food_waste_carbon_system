import csv

with open('experiments/results_yolo_gpt.csv', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        if row['vlm_triggered'] == '1' and row['vlm_label_correct'] == '0':
            print(f"{row['image_filename']:<35} | GT={row['ground_truth_label']:<8} | YOLO={row['yolo_label']:<15} | VLM={row['vlm_label']}")

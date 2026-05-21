<!-- YOLOv11 label inventory and the coarse food-category mapping used for carbon estimation. -->

# YOLO Label Mapping

這個 YOLOv11 權重目前共有 `85` 個 labels。

## 非食物類別

- `board`
- `bowl`
- `coffee cup`
- `cup`
- `fork`
- `garbage`
- `knife`
- `plate`
- `soupbowl`
- `spoon`
- `water`
- `water cup`

## 可直接映射到碳排彙總類別

### `rice`

- `cabidela rice`
- `rice`

### `vegetable`

- `asparagus`
- `baked potatoes`
- `beans`
- `black bean`
- `brocolis`
- `cabbage`
- `carrot`
- `cucumber`
- `french fries`
- `greens`
- `lettuce`
- `mashed potatoes`
- `mushrooms`
- `olives`
- `onion`
- `tomato`
- `vegetables`

### `chicken`

- `chicken`
- `chicken steak`
- `turkey steak`

### `fish`

- `fish`
- `fish hake`
- `fried cod`
- `mussel`
- `salmon`
- `tuna`
- `tuna with mushrooms`
- `tuna with pasta`

### `egg`

- `boiled egg`
- `fried egg`
- `omelet`
- `scrambled eggs`
- `scrambled eggs with bacon`

## 食物但目前不納入這五個彙總類別

- `apple`
- `bacon`
- `banana`
- `blueberries`
- `bread`
- `breaded`
- `cake`
- `cereals`
- `cheese`
- `chips`
- `chorizo`
- `coffee`
- `cutlet`
- `gelatin`
- `grape`
- `grilled chop`
- `grilled steak`
- `ham`
- `lasagna`
- `lime`
- `meatballs`
- `melon`
- `minced meat`
- `pasta`
- `pineapple`
- `pizza`
- `pork`
- `pork belly`
- `pork intestines`
- `pork loin`
- `soup`
- `spaghetti`
- `steak`
- `steaks with mushrooms`
- `stewed veal`
- `strawberry`
- `toasted bread`
- `watermelon`

## 建議

如果你現在只想先把碳排系統做穩，`food_carbon_factors` 應該只先保留這五個彙總類別：

- `rice`
- `vegetable`
- `chicken`
- `fish`
- `egg`

然後把 YOLO 輸出的細 label 先映射到這五類，再做重量分配與碳排計算。

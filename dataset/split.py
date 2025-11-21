import json
import random

INPUT_FILE = "dataset/paired_codes.json"   
TRAIN_OUT = "train.json"
VAL_OUT = "val.json"
VAL_RATIO = 0.10  

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)


random.shuffle(data)


split_idx = int(len(data) * (1 - VAL_RATIO))

train_data = data[:split_idx]
val_data = data[split_idx:]

with open(TRAIN_OUT, "w", encoding="utf-8") as f:
    json.dump(train_data, f, indent=2)

with open(VAL_OUT, "w", encoding="utf-8") as f:
    json.dump(val_data, f, indent=2)

print(f"Total: {len(data)}")
print(f"Train: {len(train_data)}")
print(f"Val: {len(val_data)}")
print("Done!")

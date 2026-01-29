from medicine_extractor import process_prescription

image_path = "images/sample1.png"
result = process_prescription(image_path)

import json

with open("output/result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4)

print("✅ Output saved to output.json")


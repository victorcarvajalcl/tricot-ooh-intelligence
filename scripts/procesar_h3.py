import json
import h3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

with open(os.path.join(DATA_DIR, "soportes.json")) as f:
    soportes = json.load(f)

for s in soportes:
    s["h3"] = h3.latlng_to_cell(s["lat"], s["lng"], 8)

with open(os.path.join(DATA_DIR, "soportes_h3.json"), "w") as f:
    json.dump(soportes, f, indent=2)

print("✅ soportes_h3.json generado")
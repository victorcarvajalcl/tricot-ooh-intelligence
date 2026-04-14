import json
import h3
from collections import Counter

def build_geojson(counter):
    features = []

    for h, count in counter.items():
        boundary = h3.cell_to_boundary(h)

        coords = [[lng, lat] for lat, lng in boundary]
        coords.append(coords[0])

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [coords]
            },
            "properties": {
                "h3": h,
                "soportes": count
            }
        })

    return {
        "type": "FeatureCollection",
        "features": features
    }

# LOAD
with open("data/soportes_h3.json") as f:
    data = json.load(f)

# CONTAR
h3_count = Counter(p["h3"] for p in data if "h3" in p)
h6_count = Counter(p["h6"] for p in data if "h6" in p)
h8_count = Counter(p["h8"] for p in data if "h8" in p)

# SAVE
with open("data/h3.geojson", "w") as f:
    json.dump(build_geojson(h3_count), f)

with open("data/h6.geojson", "w") as f:
    json.dump(build_geojson(h6_count), f)

with open("data/h8.geojson", "w") as f:
    json.dump(build_geojson(h8_count), f)

print("✅ HEX con inteligencia generados")
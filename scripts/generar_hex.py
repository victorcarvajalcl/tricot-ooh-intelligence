import json
import h3
import os
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

with open(os.path.join(DATA_DIR, "soportes_h3.json")) as f:
    soportes = json.load(f)

conteo_h6 = defaultdict(int)
conteo_h8 = defaultdict(int)

for s in soportes:
    h = s["h3"]
    conteo_h6[h3.cell_to_parent(h, 6)] += 1
    conteo_h8[h3.cell_to_parent(h, 8)] += 1


def generar_geojson(conteo):
    features = []

    for h, total in conteo.items():
        boundary = h3.cell_to_boundary(h)

        coords = [[lng, lat] for lat, lng in boundary]

        features.append({
            "type": "Feature",
            "properties": {"soportes": total},
            "geometry": {
                "type": "Polygon",
                "coordinates": [coords]
            }
        })

    return {
        "type": "FeatureCollection",
        "features": features
    }


with open(os.path.join(DATA_DIR, "h6.geojson"), "w") as f:
    json.dump(generar_geojson(conteo_h6), f)

with open(os.path.join(DATA_DIR, "h8.geojson"), "w") as f:
    json.dump(generar_geojson(conteo_h8), f)

print("✅ hex generados correctamente")
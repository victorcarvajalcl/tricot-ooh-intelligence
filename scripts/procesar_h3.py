import json
import h3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Cargar datos
with open(os.path.join(DATA_DIR, "h3.geojson")) as f:
    h3_data = json.load(f)

with open(os.path.join(DATA_DIR, "soportes_h3.json")) as f:
    soportes = json.load(f)

with open(os.path.join(DATA_DIR, "tricot.json")) as f:
    tiendas = json.load(f)

# Función para obtener bounding box de un polígono
def get_bbox(feature):
    coords = feature['geometry']['coordinates'][0]
    lngs = [c[0] for c in coords]
    lats = [c[1] for c in coords]
    return {
        'min_lng': min(lngs),
        'max_lng': max(lngs),
        'min_lat': min(lats),
        'max_lat': max(lats)
    }

# Función para contar puntos dentro del bbox
def count_in_bbox(bbox, points):
    count = 0
    for p in points:
        if (bbox['min_lng'] <= p['lng'] <= bbox['max_lng'] and
            bbox['min_lat'] <= p['lat'] <= bbox['max_lat']):
            count += 1
    return count

# Procesar cada hexágono
mart = []
for feature in h3_data['features']:
    h3_id = feature['properties'].get('h3')
    if not h3_id:
        continue

    # Área aproximada en km²
    area = h3.cell_area(h3_id)

    # Bounding box
    bbox = get_bbox(feature)

    # Contar soportes y tiendas
    soportes_count = count_in_bbox(bbox, soportes)
    tiendas_count = count_in_bbox(bbox, tiendas)

    # Densidad (por km²)
    densidad_soportes = soportes_count / area if area > 0 else 0
    densidad_tiendas = tiendas_count / area if area > 0 else 0

    mart.append({
        'h3_id': h3_id,
        'soportes': soportes_count,
        'tiendas': tiendas_count,
        'densidad_soportes': round(densidad_soportes, 4),
        'densidad_tiendas': round(densidad_tiendas, 4)
    })

# Exportar resultado
with open(os.path.join(DATA_DIR, "mart_universal.json"), "w") as f:
    json.dump(mart, f, indent=2)

print(f"✅ Mart universal generado con {len(mart)} hexágonos procesados")
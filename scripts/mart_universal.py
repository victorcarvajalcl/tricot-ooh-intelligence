import json
import h3
from shapely.geometry import shape

# Cargar datos
with open('../data/h3.geojson', 'r') as f:
    h3_data = json.load(f)

with open('../data/soportes_h3.json', 'r') as f:
    soportes = json.load(f)

with open('../data/tricot.json', 'r') as f:
    tiendas = json.load(f)

# Función para contar puntos dentro de un hexágono
def count_in_hex(feature, points):
    # Usar bounds para aproximación
    coords = feature['geometry']['coordinates'][0]
    min_lng = min(c[0] for c in coords)
    max_lng = max(c[0] for c in coords)
    min_lat = min(c[1] for c in coords)
    max_lat = max(c[1] for c in coords)

    count = 0
    for p in points:
        if min_lng <= p['lng'] <= max_lng and min_lat <= p['lat'] <= max_lat:
            count += 1
    return count

# Procesar cada hexágono
mart = []
for feature in h3_data['features']:
    h3_id = feature['properties'].get('h3_id') or feature['properties'].get('id')
    if not h3_id:
        continue

    # Área en km²
    area = h3.cell_area(h3_id)

    # Contar soportes y tiendas
    soportes_count = count_in_hex(feature, soportes)
    tiendas_count = count_in_hex(feature, tiendas)

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

# Guardar JSON
with open('../data/mart_universal.json', 'w') as f:
    json.dump(mart, f, indent=2)

print(f"Mart universal generado con {len(mart)} hexágonos")
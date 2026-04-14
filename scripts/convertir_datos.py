import pandas as pd
import json
import os
from shapely.geometry import Point
import geopandas as gpd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def limpiar_texto(x):
    if pd.isna(x):
        return ""
    return str(x).strip()

# ================= CLASIFICACIÓN AUTOMÁTICA
def clasificar_categoria(nombre):
    n = str(nombre).lower()

    if "metro" in n:
        return "Metro"
    elif "mall" in n:
        return "Mall"
    elif "av" in n or "avenida" in n:
        return "Avenida"
    elif "pantalla" in n or "led" in n:
        return "Pantalla Digital"
    elif "paradero" in n:
        return "Paradero"
    else:
        return "Otros"

# ================= COMUNAS GEO
comunas = gpd.read_file(os.path.join(DATA_DIR, "comunas.geojson"))
comunas = comunas.to_crs(epsg=4326)

def obtener_comuna(lat, lng):
    punto = Point(lng, lat)
    for _, row in comunas.iterrows():
        if row.geometry.contains(punto):
            return row.get("NOM_COM") or row.get("Comuna")
    return "Sin comuna"

# ================= SOPORTES
df = pd.read_csv(os.path.join(DATA_DIR, "soportes_vista_actual.csv"))

col_lat = next((c for c in df.columns if 'lat' in c.lower()), None)
col_lng = next((c for c in df.columns if 'lng' in c.lower() or 'lon' in c.lower()), None)
col_nombre = next((c for c in df.columns if 'nombre' in c.lower() or 'name' in c.lower()), None)

df['lat'] = df[col_lat]
df['lng'] = df[col_lng]
df['nombre'] = df[col_nombre].apply(limpiar_texto) if col_nombre else "Soporte"

df = df.dropna(subset=['lat','lng'])

df['categoria'] = df['nombre'].apply(clasificar_categoria)
df['comuna'] = df.apply(lambda r: obtener_comuna(r['lat'], r['lng']), axis=1)

df = df.fillna("")

with open(os.path.join(DATA_DIR, "soportes.json"), "w") as f:
    json.dump(df.to_dict(orient='records'), f, indent=2, ensure_ascii=False)

print("✅ soportes.json generado")

# ================= TRICOT
df2 = pd.read_excel(os.path.join(DATA_DIR, "tricot_geocodificado.xlsx"))

col_lat2 = next((c for c in df2.columns if 'lat' in c.lower()), None)
col_lng2 = next((c for c in df2.columns if 'lng' in c.lower() or 'lon' in c.lower()), None)
col_nombre2 = next((c for c in df2.columns if 'nombre' in c.lower()), None)

df2['lat'] = df2[col_lat2]
df2['lng'] = df2[col_lng2]
df2['nombre'] = df2[col_nombre2].apply(limpiar_texto) if col_nombre2 else "Tienda"

df2 = df2.dropna(subset=['lat','lng'])

df2['comuna'] = df2.apply(lambda r: obtener_comuna(r['lat'], r['lng']), axis=1)

df2 = df2.fillna("")

with open(os.path.join(DATA_DIR, "tricot.json"), "w") as f:
    json.dump(df2.to_dict(orient='records'), f, indent=2, ensure_ascii=False)

print("✅ tricot.json generado")
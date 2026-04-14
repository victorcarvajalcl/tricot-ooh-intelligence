import pandas as pd
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def limpiar_texto(x):
    if pd.isna(x):
        return ""
    return str(x).strip()

def limpiar_comuna(c):
    if pd.isna(c):
        return "Sin comuna"
    return str(c).strip().title()


# ================= SOPORTES
df = pd.read_csv(os.path.join(DATA_DIR, "soportes_vista_actual.csv"))

# 🔥 detectar columnas automáticamente
col_comuna = next((c for c in df.columns if 'comuna' in c.lower()), None)
col_lat = next((c for c in df.columns if 'lat' in c.lower()), None)
col_lng = next((c for c in df.columns if 'lng' in c.lower() or 'lon' in c.lower()), None)
col_categoria = next((c for c in df.columns if 'categoria' in c.lower()), None)
col_tipo = next((c for c in df.columns if 'tipo' in c.lower()), None)

# crear campos estándar
df['comuna'] = df[col_comuna].apply(limpiar_comuna) if col_comuna else "Sin comuna"
df['lat'] = df[col_lat]
df['lng'] = df[col_lng]
df['categoria'] = df[col_categoria].apply(limpiar_texto) if col_categoria else ""
df['tipo'] = df[col_tipo].apply(limpiar_texto) if col_tipo else ""

df = df.dropna(subset=['lat','lng'])

with open(os.path.join(DATA_DIR, "soportes.json"), "w") as f:
    json.dump(df.to_dict(orient='records'), f, indent=2, ensure_ascii=False)

print("✅ soportes.json generado")


# ================= TRICOT
df2 = pd.read_excel(os.path.join(DATA_DIR, "tricot_geocodificado.xlsx"))

col_comuna2 = next((c for c in df2.columns if 'comuna' in c.lower()), None)
col_lat2 = next((c for c in df2.columns if 'lat' in c.lower()), None)
col_lng2 = next((c for c in df2.columns if 'lng' in c.lower() or 'lon' in c.lower()), None)
col_nombre = next((c for c in df2.columns if 'nombre' in c.lower()), None)

df2['comuna'] = df2[col_comuna2].apply(limpiar_comuna) if col_comuna2 else "Sin comuna"
df2['lat'] = df2[col_lat2]
df2['lng'] = df2[col_lng2]
df2['nombre'] = df2[col_nombre].apply(limpiar_texto) if col_nombre else "Tienda"

df2 = df2.dropna(subset=['lat','lng'])

with open(os.path.join(DATA_DIR, "tricot.json"), "w") as f:
    json.dump(df2.to_dict(orient='records'), f, indent=2, ensure_ascii=False)

print("✅ tricot.json generado")
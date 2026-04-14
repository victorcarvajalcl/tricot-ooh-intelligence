import pandas as pd
import json

# ================= SOPORTES
df = pd.read_csv("data/soportes_vista_actual.csv")

soportes = []

for _, row in df.iterrows():
    try:
        soportes.append({
            "nombre": str(row.get("nombre", "")),
            "lat": float(row["lat"]),
            "lng": float(row["lng"]),
            "comuna": str(row.get("comuna", "")),
            "categoria": str(row.get("categoria", ""))
        })
    except:
        continue

with open("data/soportes.json", "w") as f:
    json.dump(soportes, f)

print("✅ soportes.json generado")


# ================= TRICOT
df2 = pd.read_excel("data/tricot_geocodificado.xlsx")

tricot = []

for _, row in df2.iterrows():
    try:
        tricot.append({
            "nombre": str(row.get("nombre", "Tricot")),
            "lat": float(row["lat"]),
            "lng": float(row["lng"]),
            "comuna": str(row.get("comuna", ""))
        })
    except:
        continue

with open("data/tricot.json", "w") as f:
    json.dump(tricot, f)

print("✅ tricot.json generado")
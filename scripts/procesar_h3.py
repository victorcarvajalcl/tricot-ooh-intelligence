import json
import h3

RES_H3 = 4
RES_H6 = 6
RES_H8 = 8

def enrich(data):
    output = []

    for p in data:
        try:
            lat = float(p["lat"])
            lng = float(p["lng"])

            p["h3"] = h3.latlng_to_cell(lat, lng, RES_H3)
            p["h6"] = h3.latlng_to_cell(lat, lng, RES_H6)
            p["h8"] = h3.latlng_to_cell(lat, lng, RES_H8)

            output.append(p)

        except:
            continue

    return output


# ================= LOAD
with open("data/soportes.json") as f:
    soportes = json.load(f)

with open("data/tricot.json") as f:
    tricot = json.load(f)

# ================= PROCESS
soportes_h3 = enrich(soportes)
tricot_h3 = enrich(tricot)

# ================= SAVE
with open("data/soportes_h3.json", "w") as f:
    json.dump(soportes_h3, f)

with open("data/tricot_h3.json", "w") as f:
    json.dump(tricot_h3, f)

print("✅ H3 generado correctamente")
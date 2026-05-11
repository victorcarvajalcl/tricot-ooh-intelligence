import geopandas as gpd

gdf = gpd.read_file("data/raw/division_comunal/division_comunal.shp")

print("Columnas disponibles:")
print(gdf.columns)

# 👉 AJUSTA SEGÚN TU DATA
if "NOM_REG" in gdf.columns:
    gdf = gdf[gdf["NOM_REG"].str.contains("Metropolitana", case=False)]
elif "COD_REG" in gdf.columns:
    gdf = gdf[gdf["COD_REG"] == 13]

# simplificar geometría
gdf["geometry"] = gdf["geometry"].simplify(0.001)

# guardar
gdf.to_file("data/comunas.geojson", driver="GeoJSON")

print("✅ comunas.geojson generado")
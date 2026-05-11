# scripts/reproyectar_comunas.py

import geopandas as gpd

# Cargar shapefile original
gdf = gpd.read_file("data/raw/division_comunal/division_comunal.shp")

# Filtrar Región Metropolitana (ajusta nombre si cambia)
gdf = gdf[gdf["NOM_REG"].str.contains("Metropolitana", case=False)]

# 🔥 REPROYECTAR A WGS84
gdf = gdf.to_crs(epsg=4326)

# Guardar como GeoJSON
gdf.to_file("data/comunas.geojson", driver="GeoJSON")

print("✅ comunas.geojson corregido (WGS84)")
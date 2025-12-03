import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import folium
import json
import webbrowser

# Load datasets
crimeDF = pd.read_csv('./data/raw/crime_data.csv')
popDF = pd.read_csv('./data/raw/state_wise_population.csv')

print("\n[1] Crime Data Loaded:", crimeDF.shape)
print(crimeDF.head())
print("\n[2] Population Data Loaded:", popDF.shape)
print(popDF.head())

crimeDF.columns = crimeDF.columns.str.strip().str.lower().str.replace(" ", "_")
crimeDF.rename(columns={"states/uts": "state"}, inplace=True)

popDF.columns = popDF.columns.str.strip().str.lower().str.replace(" ", "_")

print("\n[3] Cleaned Column Names:")
print("Crime Columns:", crimeDF.columns)
print("Population Columns:", popDF.columns)

print("\n[CHECK] Crime Data Columns:")
print(crimeDF.columns)

before_rows = crimeDF.shape[0]

crimeDF = crimeDF[crimeDF["district"].str.lower() != "total"]

after_rows = crimeDF.shape[0]

print(f"\n[4] Removed 'Total' District Rows: {before_rows - after_rows} rows removed")
print("Remaining:", crimeDF.shape)


# -------------------------------------------
# GROUP BY STATE
# -------------------------------------------
print("\n[5] Grouping Crime Data by STATE...")

# Check if state column exists
if "state" not in crimeDF.columns:
    print("[ERROR] 'state' column not found!")
else:
    print("[OK] 'state' column found.")

# Perform grouping
stateCrime = crimeDF.groupby("state", as_index=False).sum(numeric_only=True)

print("\n[5] Crime Grouped by State Successfully!")
print(stateCrime.head())
print("State Crime Shape:", stateCrime.shape)

# ---------------------------------------------------------
print("\n[DEBUG] Unique states in Crime Data:")
print(sorted(crimeDF['state'].unique()))

print("\n[DEBUG] Unique states in Population Data:")
print(sorted(popDF['state'].unique()))
# ---------------------------------------------------------
# ---------------------------------------------------------

print("\n[6] Fixing State Name Mismatch...")

# Lowercase & strip spaces
crimeDF['state'] = crimeDF['state'].str.lower().str.strip()
popDF['state'] = popDF['state'].str.lower().str.strip()

# Create mapping from Crime → Population naming
state_mapping = {
    "a&n islands": "andaman & nicobar islands",
    "andhra pradesh": "andhra pradesh",
    "arunachal pradesh": None,     
    "assam": "assam",
    "bihar": "bihar",
    "chandigarh": "chandigarh",
    "chhattisgarh": "chhattisgarh",
    "d&n haveli": "dnh",
    "daman & diu": "dnh",          
    "delhi ut": "delhi",
    "goa": "goa",
    "gujarat": "gujarat",
    "haryana": "haryana",
    "himachal pradesh": "himachal pradesh",
    "jammu & kashmir": "j&k",
    "jharkhand": "jharkhand",
    "karnataka": "karnataka",
    "kerala": "kerala",
    "lakshadweep": None,           
    "madhya pradesh": "madhya pradesh",
    "maharashtra": "maharashtra",
    "manipur": "manipur",
    "meghalaya": "meghalaya",
    "mizoram": "mizoram",
    "nagaland": "nagaland",
    "odisha": "orissa",            # name difference
    "puducherry": "pondy",
    "punjab": "punjab",
    "rajasthan": "rajasthan",
    "sikkim": "sikkim",
    "tamil nadu": "tamil nadu",
    "telangana": "telangana",
    "tripura": "tripura",
    "uttar pradesh": "uttar pradesh",
    "uttarakhand": "uttarakhand",
    "west bengal": "west bengal"
}

# Apply mapping
crimeDF['state'] = crimeDF['state'].map(state_mapping)

# Remove rows where state is None (not present in population)
crimeDF = crimeDF[crimeDF['state'].notna()]

print("\n[6] After State Mapping:")
print(sorted(crimeDF['state'].unique()))
print("Remaining crime rows:", crimeDF.shape)

# ---------------------------------------------------------
stateCrime = crimeDF.groupby("state", as_index=False).sum(numeric_only=True)

print("\n[7] State-wise Crime After Mapping:")
print(stateCrime.head())
print("Shape:", stateCrime.shape)

# ---------------------------------------------------------
merged = pd.merge(stateCrime, popDF, on="state", how="inner")

print("\n[8] Merged Dataset Created Successfully!")
print(merged.head())
print("Merged Shape:", merged.shape)

# ---------------------------------------------------------
merged["total_crimes"] = merged["total_cognizable_ipc_crimes"]

print("\n[9] Total Crimes Added:")
print(merged[['state', 'total_crimes']].head())

# ---------------------------------------------------------
merged["crime_rate"] = (merged["total_crimes"] / merged["total_population"]) * 100000

print("\n[10] Crime Rate Calculated:")
print(merged[['state', 'crime_rate']].head())

# ---------------------------------------------------------
merged.to_csv("./data/processed/final_crime_data.csv", index=False)
print("\n[11] Saved final dataset -> ./data/processed/final_crime_data.csv")

# ---------------------------------------------------------

plt.figure(figsize=(12, 8))
sns.barplot(
    data=merged.sort_values("crime_rate", ascending=False),
    x="crime_rate", 
    y="state",
    hue="state", 
    palette="Reds_r",
    legend=False
)
plt.title("Crime Rate per 1 Lakh Population (State-wise)")
plt.tight_layout()
plt.savefig("./output/maps/crime_rate_by_state.png")
plt.show()
plt.close()

print("\n[12] Bar Chart Saved -> ./output/maps/crime_rate_by_state.png")

# ---------------------------------------------------------
#pairplot
sns.pairplot(
    merged,
    vars=["total_crimes", "total_population", "crime_rate"],
    diag_kind="kde",
)
plt.suptitle("Pairplot of Crime Data Features", y=1.02)
plt.show()
plt.savefig("./output/maps/crime_data_pairplot.png")
plt.close()
print("\n[12] Pairplot Saved -> ./output/maps/crime_data_pairplot.png")

# ---------------------------------------------------------
#scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=merged,
    x="total_population",
    y="total_crimes",
    hue="crime_rate",
    size="crime_rate",
    palette="viridis",
    sizes=(50, 500),
    alpha=0.7
)
plt.xscale("log")
plt.yscale("log")
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.title("Total Crimes vs Total Population (Log-Log Scale)")
plt.tight_layout()
plt.savefig("./output/maps/total_crimes_vs_population.png")
plt.show()
plt.close()
print("\n[13] Scatter Plot Saved -> ./output/maps/total_crimes_vs_population.png")

# ---------------------------------------------------------
print("\n[13] Preparing GeoJSON for Mapping...")

# Match GeoJSON state names with merged DF
merged["state"] = merged["state"].str.title().str.strip()

print("[13] Loading India State GeoJSON...")
with open('./data/raw/india_state_geo.json', 'r', encoding='utf-8') as f:
    india_geo = json.load(f)

print("[OK] GeoJSON Loaded Successfully!\n")

# ============================================================
# MAP 1 — MARKER MAP USING CENTROIDS
# ============================================================

print("[MAP 1] Creating India Marker Map...")

m_marker = folium.Map(location=[22.5, 78.9], zoom_start=5, tiles="cartodbpositron")

for feature in india_geo["features"]:
    props = feature["properties"]
    state_name = props["NAME_1"].title().strip()
    geom = feature["geometry"]

    # Handle Polygon / MultiPolygon
    try:
        if geom["type"] == "MultiPolygon":
            polygon = geom["coordinates"][0][0]  # first polygon
        else:
            polygon = geom["coordinates"][0]      # outer ring

        # Calculate centroid (mean of polygon points)
        lon = sum([pt[0] for pt in polygon]) / len(polygon)
        lat = sum([pt[1] for pt in polygon]) / len(polygon)

        folium.Marker(
            location=[lat, lon],
            popup=state_name,
            tooltip=state_name,
            icon=folium.Icon(color="red", icon="info-sign", prefix='glyphicon')
        ).add_to(m_marker)

    except Exception as e:
        print("Skipping:", state_name, "Error:", e)
        continue

m_marker.save("./output/maps/india_marker_map.html")
print("[MAP 1] Saved -> ./output/maps/india_marker_map.html")


# ============================================================
# MAP 2 — CRIME RATE CHOROPLETH
# ============================================================

print("\n[MAP 2] Creating Crime Rate Choropleth Map...")

m_choro = folium.Map(location=[22.5, 78.9], zoom_start=5, tiles="cartodbpositron")

# Choropleth Layer
folium.Choropleth(
    geo_data=india_geo,
    name="Crime Rate",
    data=merged,
    columns=["state", "crime_rate"],
    key_on="feature.properties.NAME_1",
    fill_color="YlOrRd",
    fill_opacity=0.8,
    line_opacity=0.3,
    nan_fill_color="gray",
    legend_name="Crime Rate per 1 Lakh Population",
    highlight=True
).add_to(m_choro)

# Tooltip Data
merged["tooltip_text"] = (
    merged["state"] + " | Crime Rate: " + merged["crime_rate"].round(2).astype(str)
)

# Attach tooltip field into GeoJSON
for feature in india_geo["features"]:
    state_g = feature["properties"]["NAME_1"].title().strip()
    match = merged[merged["state"] == state_g]
    feature["properties"]["tooltip_text"] = (
        match.iloc[0]["tooltip_text"] if not match.empty else "No data"
    )

# Tooltip Layer
folium.GeoJson(
    india_geo,
    style_function=lambda x: {"color": "transparent", "weight": 0},
    tooltip=folium.GeoJsonTooltip(
        fields=["tooltip_text"],
        aliases=["Info:"],
        labels=True,
        sticky=True
    )
).add_to(m_choro)

folium.LayerControl().add_to(m_choro)

m_choro.save("./output/maps/india_choropleth_map.html")
print("[MAP 2] Saved -> ./output/maps/india_choropleth_map.html")

# 5. Open Maps in Browser automatically
webbrowser.open("file:///D:/Python/Data%20Visualisation/india-crime-analysis/output/maps/india_marker_map.html")
webbrowser.open("file:///D:/Python/Data%20Visualisation/india-crime-analysis/output/maps/india_choropleth_map.html")

print("\n[DONE] Analysis Complete. All outputs saved and maps opened in browser!")


print("\n[13] Both Maps Generated Successfully!")

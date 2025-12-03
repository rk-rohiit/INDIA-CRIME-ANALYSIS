# 🇮🇳 India Crime Rate Analysis – Data Visualization & Geo-Mapping

This project analyzes **state-wise crime statistics of India** using Python and creates powerful **visualizations**, **statistical charts**, and **interactive Folium geospatial maps**.  
It provides insights into crime patterns, population impact, and regional crime intensity.

---

## 📊 Project Features

### ✔ 1. Data Cleaning & Preprocessing
- Standardized column names  
- Removed invalid rows (`Total` district entries)  
- Corrected mismatched state names  
- Merged crime data with population dataset  
- Calculated:
  - **Total Crimes**
  - **Crime Rate per 1 lakh population**

---

## 📈 Visualizations (Matplotlib + Seaborn)

### 🔹 Crime Rate Bar Chart  
Shows highest & lowest crime rate states.

### 🔹 Pairplot  
Relationship between:
- Total crimes  
- Total population  
- Crime rate  

### 🔹 Scatter Plot (Log Scale)  
Population vs. crimes with scaling effect.

All charts are saved inside:


---

## 🗺️ Interactive Folium Maps

### 🌍 MAP 1 — Marker Map (Centroid Based)
- Red markers automatically placed on each state  
- Tooltip + popup show state name  
- Output file:


---

### 🟥 MAP 2 — Crime Rate Choropleth
- Heat-colored states (YlOrRd palette)  
- Tooltip shows: `State | Crime Rate`  
- Highlighted boundaries  
- Output file:


---

## 📦 Project Folder Structure

india-crime-analysis/
│
├── data/
│ ├── raw/
│ │ ├── crime_data.csv
│ │ ├── state_wise_population.csv
│ │ ├── india_state_geo.json
│ │
│ └── processed/
│ └── final_crime_data.csv
│
├── output/
│ ├── maps/
│ │ ├── crime_rate_by_state.png
│ │ ├── crime_data_pairplot.png
│ │ ├── total_crimes_vs_population.png
│ │ ├── india_marker_map.html
│ │ └── india_choropleth_map.html
│
├── src/
│ └── main.py
│
└── README.md


---

## 🧰 Technologies Used

### **Python Libraries**
- Pandas  
- NumPy  
- Matplotlib  
- Seaborn  
- Folium  
- JSON  
- Webbrowser (auto-open maps)

### **Data Formats**
- CSV  
- GeoJSON  

---

## 🧮 Key Formula

### Crime Rate:

\[
#### {Crime Rate} = frac{{Total Crimes}}{{Total Population}}) \times 100000
\]

Used to compare crime levels fairly across states.

---

## 🚀 How to Run the Project

### 1️⃣ Install Dependencies  
```bash
pip install pandas numpy matplotlib seaborn folium
python src/main.py

```
👨‍💻 Author

Rohit Kumar (Rohit Sharma)
Data Visualization & Fullstack Developer

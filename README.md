# seismic-risk-engine-
A data-driven interactive web application built with Python and Streamlit that analyzes global earthquake patterns, computes regional risk scores, and visualizes high-risk zones on an interactive heatmap.
## 🎯 Purpose
Earthquakes are one of the most devastating natural disasters on Earth, causing massive destruction and loss of life every year. The **Seismic Risk Engine** is designed to help identify which regions of the world have historically been most vulnerable to seismic activity. By processing real USGS earthquake data and applying a risk scoring model, this app transforms raw seismic records into meaningful, visual insights that are easy to understand for anyone — not just scientists or geologists.
The goal is not to predict future earthquakes, but to highlight patterns from the past so that we can better understand where the risks are highest.
## 📌 Objectives
- Load and process real-world earthquake data from the USGS catalog using the **Polars** DataFrame engine
- Clean and filter the dataset by removing null values and invalid records
- Group earthquake events into geographic grid regions using latitude and longitude binning
- Calculate a **Seismic Risk Score** for each region based on event frequency and average magnitude
- Visualize high-risk zones on a beautiful interactive global heatmap using **Folium**
- Display key statistics like total events, average magnitude, max magnitude, and average depth
- Generate automated insights directly from the data
- Allow users to interactively filter data by magnitude range, depth, and map style
- Provide a downloadable filtered dataset for further analysis

## 🗃️ Dataset
- **Provider:** United States Geological Survey (USGS) Earthquake Catalog
- **Format:** CSV (Comma Separated Values) with 22 feature columns
- **Total Records:** 1,369 earthquake events
- **Time Range:** May 2023 — June 2026
- **Minimum Magnitude:** 5.5 Mw (only significant earthquakes included)
- **Geographic Coverage:** Global — all continents and ocean regions
- **Key Fields Used:**
  - `latitude` — North/South geographic position
  - `longitude` — East/West geographic position
  - `mag` — Earthquake magnitude (Mw scale)
  - `depth` — Depth below surface in kilometers
  - `place` — Human-readable location description
  - `time` — Date and time of the seismic event
 
  - ## 📊 Risk Score Formula
The seismic risk score for each region is calculated as:
Risk Score = Number of Earthquakes × Average Magnitude

This means a region that experiences many earthquakes AND has high average magnitudes will score much higher than a region with only occasional or weak tremors. The higher the score, the more seismically dangerous the region is considered to be based on historical data.

## 🖥️ App Features
- 🗺️ **Interactive Heatmap** — Global map with pink gradient showing risk intensity by region
- 📊 **Magnitude Distribution Chart** — Histogram showing how earthquake magnitudes are distributed
- 🏆 **Top 10 Risk Regions Table** — Ranked list of most dangerous regions with scores
- 📋 **About Section** — Project purpose, objectives, data source and methodology
- 💡 **Auto Insights** — Key findings automatically extracted from the data
- ⚙️ **Sidebar Filters** — Filter by magnitude range, depth, and map style
- 🔍 **Raw Data Viewer** — Explore the full filtered dataset in a table
- 💾 **Download Button** — Export the filtered dataset as a CSV file

- ## 📁 Project Structure
seismic-risk-engine/
│
├── app.py               # Main Streamlit application
├── earthquake.csv       # USGS earthquake dataset
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
## 🌐 Live Demo
https://seismicriskanalysis.streamlit.app/
## 👩‍💻 Author
**Nandini Gaur**
Student 
    

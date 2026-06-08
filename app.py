import streamlit as st
import polars as pl
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

# ─── PAGE CONFIG ───────────────────────────────────────────────
st.set_page_config(
    page_title="Seismic Risk Engine",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Seismic Risk Engine")
st.markdown("Identifying earthquake-prone regions from historical data")

# ─── LOAD DATA WITH POLARS ─────────────────────────────────────
@st.cache_data
@st.cache_data
def load_data():
    df = pl.read_csv("earthquake.csv", infer_schema_length=10000, ignore_errors=True)
    df = df.drop_nulls(subset=["latitude", "longitude", "mag"])
    df = df.filter(pl.col("mag") > 0)
    return df

df = load_data()

# ─── SIDEBAR FILTERS ───────────────────────────────────────────
st.sidebar.header("🔧 Filters")

mag_min = float(df["mag"].min())
mag_max = float(df["mag"].max())

min_mag, max_mag = st.sidebar.slider(
    "Magnitude Range",
    min_value=mag_min,
    max_value=mag_max,
    value=(5.5, mag_max)
)

depth_max = st.sidebar.slider(
    "Max Depth (km)",
    min_value=0,
    max_value=int(df["depth"].max()),
    value=int(df["depth"].max())
)

# Apply filters
df_filtered = df.filter(
    (pl.col("mag") >= min_mag) &
    (pl.col("mag") <= max_mag) &
    (pl.col("depth") <= depth_max)
)

# ─── SUMMARY METRICS ───────────────────────────────────────────
st.markdown("### 📊 Summary")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Earthquakes", len(df_filtered))
col2.metric("Avg Magnitude",     round(df_filtered["mag"].mean(), 2))
col3.metric("Max Magnitude",     round(df_filtered["mag"].max(), 2))
col4.metric("Avg Depth (km)",    round(df_filtered["depth"].mean(), 2))

# ─── RISK SCORE CALCULATION ────────────────────────────────────
df_risk = df_filtered.with_columns([
    pl.col("latitude").round(1).alias("lat_bin"),
    pl.col("longitude").round(1).alias("lon_bin")
])

risk = df_risk.group_by(["lat_bin", "lon_bin"]).agg([
    pl.len().alias("frequency"),
    pl.col("mag").mean().alias("avg_mag")
])

risk = risk.with_columns(
    (pl.col("frequency") * pl.col("avg_mag")).alias("risk_score")
)

# ─── HEATMAP ───────────────────────────────────────────────────
st.markdown("### 🗺️ Seismic Risk Heatmap")

m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")

heat_data = list(zip(
    risk["lat_bin"].to_list(),
    risk["lon_bin"].to_list(),
    risk["risk_score"].to_list()
))

HeatMap(heat_data, radius=15, blur=10, max_zoom=5).add_to(m)
st_folium(m, width=1200, height=500)

# ─── CHARTS ────────────────────────────────────────────────────
st.markdown("### 📈 Analysis")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Magnitude Distribution")
    mag_values = df_filtered["mag"].to_list()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(mag_values, bins=30, color="#e74c3c", edgecolor="white")
    ax.set_xlabel("Magnitude", color="white")
    ax.set_ylabel("Count", color="white")
    ax.set_facecolor("#1a1a2e")
    fig.patch.set_facecolor("#1a1a2e")
    ax.tick_params(colors="white")
    st.pyplot(fig)

with col2:
    st.markdown("#### 🏆 Top 10 High-Risk Regions")
    top_risk = risk.sort("risk_score", descending=True).head(10)
    top_risk_pd = top_risk.to_pandas()
    top_risk_pd["Region"] = (
        top_risk_pd["lat_bin"].astype(str) + ", " +
        top_risk_pd["lon_bin"].astype(str)
    )
    st.dataframe(
        top_risk_pd[["Region", "frequency", "avg_mag", "risk_score"]],
        use_container_width=True
    )

# ─── RAW DATA ──────────────────────────────────────────────────
with st.expander("📂 View Raw Data"):
    st.dataframe(df_filtered.to_pandas(), use_container_width=True)

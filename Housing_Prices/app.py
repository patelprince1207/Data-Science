import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Metro City House Price Analysis", layout="wide")

CITIES = ["Bangalore", "Chennai", "Delhi", "Hyderabad", "Kolkata", "Mumbai"]

AMENITY_COLS = [
    "MaintenanceStaff", "Gymnasium", "SwimmingPool", "LandscapedGardens",
    "JoggingTrack", "RainWaterHarvesting", "IndoorGames", "ShoppingMall",
    "Intercom", "SportsFacility", "ATM", "ClubHouse", "School",
    "24X7Security", "PowerBackup", "CarParking", "StaffQuarter", "Cafeteria",
    "MultipurposeRoom", "Hospital", "WashingMachine", "Gasconnection", "AC",
    "Wifi", "Children'splayarea", "LiftAvailable", "BED", "VaastuCompliant",
    "Microwave", "GolfCourse", "TV", "DiningTable", "Sofa", "Wardrobe",
    "Refrigerator",
]


@st.cache_data
def load_data():
    frames = []
    for city in CITIES:
        temp = pd.read_csv(f"{city}.csv")
        temp["city"] = city
        frames.append(temp)
    df = pd.concat(frames, ignore_index=True)

    # 9 encodes missing values in this dataset, not NaN -- replace before cleaning
    df = df.replace(9, np.nan)
    df = df.drop_duplicates()
    df = df.fillna(0)
    df["PricePerSqft"] = df["Price"] / df["Area"].replace(0, np.nan)
    return df


df = load_data()

st.title("🏠 Metro City House Price Analysis")
st.caption("Housing listing data across 6 major Indian metro cities: Bangalore, Chennai, Delhi, Hyderabad, Kolkata, Mumbai")

# ---- Sidebar filters ----
st.sidebar.header("Filters")
selected_cities = st.sidebar.multiselect("City", CITIES, default=CITIES)
bedroom_options = sorted(df["No. of Bedrooms"].unique())
selected_bedrooms = st.sidebar.multiselect("No. of Bedrooms", bedroom_options, default=bedroom_options)
price_min, price_max = int(df["Price"].min()), int(df["Price"].max())
price_range = st.sidebar.slider(
    "Price range (₹)", price_min, price_max, (price_min, min(price_max, 20000000)), step=100000
)

filtered = df[
    df["city"].isin(selected_cities)
    & df["No. of Bedrooms"].isin(selected_bedrooms)
    & df["Price"].between(price_range[0], price_range[1])
]

st.markdown(f"**{len(filtered):,} listings** match your filters")

# ---- Key metrics ----
c1, c2, c3, c4 = st.columns(4)
c1.metric("Avg Price", f"₹{filtered['Price'].mean():,.0f}")
c2.metric("Median Price", f"₹{filtered['Price'].median():,.0f}")
c3.metric("Avg Area (sqft)", f"{filtered['Area'].mean():,.0f}")
c4.metric("Avg Price/sqft", f"₹{filtered['PricePerSqft'].mean():,.0f}")

# ---- Charts ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("Average Price by City")
    city_avg = filtered.groupby("city")["Price"].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(city_avg, x="city", y="Price", color="city")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Price Distribution")
    fig2 = px.histogram(filtered, x="Price", color="city", nbins=50, marginal="box")
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Price vs Area")
    sample = filtered.sample(min(2000, len(filtered))) if len(filtered) > 0 else filtered
    fig3 = px.scatter(sample, x="Area", y="Price", color="city", hover_data=["No. of Bedrooms"])
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Avg Price/sqft by Bedrooms")
    bed_avg = filtered.groupby("No. of Bedrooms")["PricePerSqft"].mean().reset_index()
    fig4 = px.line(bed_avg, x="No. of Bedrooms", y="PricePerSqft", markers=True)
    st.plotly_chart(fig4, use_container_width=True)

st.subheader("Top Amenities Availability (%)")
amenity_pct = (filtered[AMENITY_COLS].mean() * 100).sort_values(ascending=False).head(15)
fig5 = px.bar(amenity_pct, orientation="h")
fig5.update_layout(showlegend=False, xaxis_title="% listings with amenity", yaxis_title="")
st.plotly_chart(fig5, use_container_width=True)

with st.expander("📋 View raw data"):
    st.dataframe(filtered.head(500))

st.caption("Data cleaning note: missing values in the source data are encoded as `9`, not NaN — these are replaced with NaN before cleaning.")

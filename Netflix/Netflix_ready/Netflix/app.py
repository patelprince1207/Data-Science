import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Netflix Titles Analysis", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(BASE_DIR, "netflix_titles.csv"))
    df["date_added"] = pd.to_datetime(df["date_added"].str.strip(), errors="coerce")
    return df


df = load_data()

st.title("🎬 Netflix Titles — Exploratory Data Analysis")
st.caption(f"{len(df):,} titles (Movies & TV Shows) available on Netflix")

# ---- Sidebar filters ----
st.sidebar.header("Filters")
type_options = sorted(df["type"].dropna().unique())
selected_types = st.sidebar.multiselect("Type", type_options, default=type_options)

year_min, year_max = int(df["release_year"].min()), int(df["release_year"].max())
year_range = st.sidebar.slider("Release Year", year_min, year_max, (2000, year_max))

all_countries = sorted(df["country"].dropna().str.split(", ").explode().unique())
selected_countries = st.sidebar.multiselect("Country (optional)", all_countries)

filtered = df[
    df["type"].isin(selected_types)
    & df["release_year"].between(year_range[0], year_range[1])
]
if selected_countries:
    country_mask = filtered["country"].dropna().apply(
        lambda x: any(c in x for c in selected_countries)
    )
    filtered = filtered[filtered.index.isin(country_mask[country_mask].index)]

st.markdown(f"**{len(filtered):,} titles** match your filters")

# ---- Key metrics ----
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Titles", f"{len(filtered):,}")
c2.metric("Movies", f"{(filtered['type'] == 'Movie').sum():,}")
c3.metric("TV Shows", f"{(filtered['type'] == 'TV Show').sum():,}")
c4.metric("Unique Countries", f"{filtered['country'].dropna().str.split(', ').explode().nunique():,}")

# ---- Charts ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("Movies vs TV Shows")
    type_count = filtered["type"].value_counts().reset_index()
    type_count.columns = ["type", "count"]
    fig = px.bar(type_count, x="type", y="count", color="type")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Content Growth Over Years")
    year_growth = filtered["release_year"].value_counts().sort_index().reset_index()
    year_growth.columns = ["release_year", "count"]
    fig2 = px.line(year_growth, x="release_year", y="count", markers=True)
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Top 10 Countries by Content")
    country_data = filtered["country"].dropna().str.split(", ").explode()
    top_countries = country_data.value_counts().head(10).reset_index()
    top_countries.columns = ["country", "count"]
    fig3 = px.bar(top_countries, x="country", y="count")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Content Ratings")
    rating_count = filtered["rating"].value_counts().reset_index()
    rating_count.columns = ["rating", "count"]
    fig4 = px.bar(rating_count, x="count", y="rating", orientation="h")
    st.plotly_chart(fig4, use_container_width=True)

st.subheader("Top 10 Genres")
genre_data = filtered["listed_in"].dropna().str.split(", ").explode()
top_genres = genre_data.value_counts().head(10).reset_index()
top_genres.columns = ["genre", "count"]
fig5 = px.bar(top_genres, x="genre", y="count")
st.plotly_chart(fig5, use_container_width=True)

st.subheader("Top 10 Directors")
top_directors = filtered["director"].dropna().value_counts().head(10).reset_index()
top_directors.columns = ["director", "count"]
fig6 = px.bar(top_directors, x="director", y="count")
st.plotly_chart(fig6, use_container_width=True)

with st.expander("📋 View raw data"):
    st.dataframe(filtered.head(500))

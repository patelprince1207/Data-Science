import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="AI Usage & Impact Analysis", page_icon="🤖", layout="wide")

# ---------- Load Data ----------
@st.cache_data
def load_data():
    df = pd.read_csv(Path(__file__).parent / "ai_usage_cleaned.csv")
    df["Plan"] = np.where(df["Monthly_AI_Cost"] == 0, "Free", "Paid")
    return df

df = load_data()

st.title("🤖 AI Usage & Impact Analysis: Students vs Professionals")
st.markdown("Interactive dashboard to explore how students and professionals use AI tools.")

# ---------- Sidebar Filters ----------
st.sidebar.header("Filters")

user_type = st.sidebar.multiselect("User Type", sorted(df["User_Type"].unique()),
                                   default=sorted(df["User_Type"].unique()))
country = st.sidebar.multiselect("Country", sorted(df["Country"].unique()),
                                 default=sorted(df["Country"].unique()))
tool = st.sidebar.multiselect("AI Tool", sorted(df["AI_Tool"].unique()),
                              default=sorted(df["AI_Tool"].unique()))
purpose = st.sidebar.multiselect("AI Purpose", sorted(df["AI_Purpose"].unique()),
                                 default=sorted(df["AI_Purpose"].unique()))
plan = st.sidebar.multiselect("Plan", ["Free", "Paid"], default=["Free", "Paid"])

fdf = df[
    df["User_Type"].isin(user_type)
    & df["Country"].isin(country)
    & df["AI_Tool"].isin(tool)
    & df["AI_Purpose"].isin(purpose)
    & df["Plan"].isin(plan)
]

if fdf.empty:
    st.warning("No data for the selected filters. Please change the filters.")
    st.stop()

# ---------- KPI Cards ----------
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Users", len(fdf))
c2.metric("Avg Usage (hrs/day)", round(fdf["AI_Usage_Hours_Per_Day"].mean(), 2))
c3.metric("Avg Productivity", round(fdf["Productivity_Score"].mean(), 2))
c4.metric("Avg Satisfaction", round(fdf["Satisfaction_Score"].mean(), 2))
c5.metric("Avg Time Saved (hrs/wk)", round(fdf["Time_Saved_Hours_Per_Week"].mean(), 2))

st.markdown("---")

# ---------- Row 1 ----------
col1, col2 = st.columns(2)

with col1:
    tool_count = fdf["AI_Tool"].value_counts().reset_index()
    tool_count.columns = ["AI_Tool", "Users"]
    fig = px.bar(tool_count, x="Users", y="AI_Tool", orientation="h",
                 title="Most Used AI Tools", color="Users")
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, width="stretch")

with col2:
    pur = fdf.groupby(["AI_Purpose", "User_Type"]).size().reset_index(name="Users")
    fig = px.bar(pur, x="AI_Purpose", y="Users", color="User_Type", barmode="group",
                 title="AI Purpose: Students vs Professionals")
    st.plotly_chart(fig, width="stretch")

# ---------- Row 2 ----------
col3, col4 = st.columns(2)

with col3:
    fig = px.scatter(fdf, x="AI_Usage_Hours_Per_Day", y="Time_Saved_Hours_Per_Week",
                     color="User_Type", title="Daily AI Usage vs Weekly Time Saved")
    # trend line (numpy, no statsmodels needed)
    if len(fdf) > 2:
        m, b = np.polyfit(fdf["AI_Usage_Hours_Per_Day"], fdf["Time_Saved_Hours_Per_Week"], 1)
        x_line = np.array([fdf["AI_Usage_Hours_Per_Day"].min(), fdf["AI_Usage_Hours_Per_Day"].max()])
        fig.add_scatter(x=x_line, y=m * x_line + b, mode="lines", name="Trend",
                        line=dict(color="red", dash="dash"))
    st.plotly_chart(fig, width="stretch")

with col4:
    fig = px.box(fdf, x="User_Type", y="Productivity_Score", color="User_Type",
                 title="Productivity Score: Students vs Professionals")
    st.plotly_chart(fig, width="stretch")

# ---------- Row 3 ----------
col5, col6 = st.columns(2)

with col5:
    plan_avg = fdf.groupby("Plan")[["Productivity_Score", "Satisfaction_Score",
                                    "Time_Saved_Hours_Per_Week"]].mean().round(2).reset_index()
    plan_long = plan_avg.melt(id_vars="Plan", var_name="Metric", value_name="Average")
    fig = px.bar(plan_long, x="Metric", y="Average", color="Plan", barmode="group",
                 title="Free vs Paid Users (average)")
    st.plotly_chart(fig, width="stretch")

with col6:
    rec = fdf[fdf["Would_Recommend"] != "Unknown"]["Would_Recommend"].value_counts().reset_index()
    rec.columns = ["Answer", "Users"]
    fig = px.pie(rec, names="Answer", values="Users", title="Would Recommend AI Tool?", hole=0.4)
    st.plotly_chart(fig, width="stretch")

# ---------- Row 4 ----------
col7, col8 = st.columns(2)

with col7:
    sat = fdf.groupby("AI_Tool")["Satisfaction_Score"].mean().round(2).reset_index()
    fig = px.bar(sat, x="AI_Tool", y="Satisfaction_Score", color="Satisfaction_Score",
                 title="Average Satisfaction by AI Tool")
    st.plotly_chart(fig, width="stretch")

with col8:
    num_cols = ["Age", "AI_Usage_Hours_Per_Day", "Monthly_AI_Cost", "Productivity_Score",
                "Accuracy_Rating", "Satisfaction_Score", "Time_Saved_Hours_Per_Week",
                "Work_or_Study_Hours_Per_Day"]
    fig = px.imshow(fdf[num_cols].corr().round(2), text_auto=True,
                    color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                    title="Correlation Heatmap")
    st.plotly_chart(fig, width="stretch")

# ---------- Raw Data ----------
st.markdown("---")
if st.checkbox("Show Raw Data"):
    st.dataframe(fdf, width="stretch")
    st.download_button("Download filtered data (CSV)", fdf.to_csv(index=False),
                       "filtered_ai_usage.csv", "text/csv")

st.caption("Note: This is a small survey dataset. Results show correlation, not causation.")

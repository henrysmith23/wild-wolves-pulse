# ABOUTME: Streamlit dashboard showing Liverpool FC cumulative goals by matchweek.
# ABOUTME: Overlays current season against last season for scored and conceded.

import json
import os

import altair as alt
import pandas as pd
import streamlit as st

st.title("Liverpool Pulse")

DATA_FILE = "data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, "r") as f:
        return json.load(f)


data = load_data()

if not data or not data.get("seasons"):
    st.info("No match data yet. Run the collector to fetch results.")
    st.stop()

rows_scored = []
rows_conceded = []

for season_label, matches in data["seasons"].items():
    for m in matches:
        rows_scored.append({
            "Matchweek": m["matchweek"],
            "Goals": m["cum_scored"],
            "Season": season_label,
        })
        rows_conceded.append({
            "Matchweek": m["matchweek"],
            "Goals": m["cum_conceded"],
            "Season": season_label,
        })

df_scored = pd.DataFrame(rows_scored)
df_conceded = pd.DataFrame(rows_conceded)

st.subheader("Cumulative Goals Scored")

if not df_scored.empty:
    chart_scored = (
        alt.Chart(df_scored)
        .mark_line(point=True)
        .encode(
            x=alt.X("Matchweek:Q", scale=alt.Scale(domain=[1, 38])),
            y=alt.Y("Goals:Q"),
            color=alt.Color("Season:N"),
            tooltip=["Season", "Matchweek", "Goals"],
        )
        .properties(height=400)
    )
    st.altair_chart(chart_scored, width="stretch")

st.subheader("Cumulative Goals Conceded")

if not df_conceded.empty:
    chart_conceded = (
        alt.Chart(df_conceded)
        .mark_line(point=True)
        .encode(
            x=alt.X("Matchweek:Q", scale=alt.Scale(domain=[1, 38])),
            y=alt.Y("Goals:Q"),
            color=alt.Color("Season:N"),
            tooltip=["Season", "Matchweek", "Goals"],
        )
        .properties(height=400)
    )
    st.altair_chart(chart_conceded, width="stretch")

st.caption(f"Last updated: {data.get('last_updated', 'unknown')}")

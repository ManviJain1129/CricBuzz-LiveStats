import streamlit as st
import pandas as pd

st.set_page_config(page_title="Top Stats - Cricbuzz", layout="wide")
st.title("📊 ODI Player Statistics & Top Performers")

# Load ODI data CSVs from each folder
batting = pd.read_csv('Batting\ODI data.csv')
bowling = pd.read_csv('Bowling\Bowling_ODI.csv')
fielding = pd.read_csv('Fielding\Fielding_ODI.csv')

# Display Top Run-Scorers in ODIs
st.header("🏏 Top ODI Run-Scorers")
batting['Runs'] = pd.to_numeric(batting['Runs'], errors='coerce').fillna(0)
top_batters = batting.sort_values(by="Runs", ascending=False).head(20)
st.dataframe(top_batters, height=400)

# Display Top ODI Wicket Takers
st.header("🎯 Top ODI Wicket-Takers")
bowling['Wkts'] = pd.to_numeric(bowling['Wkts'], errors='coerce').fillna(0)
top_bowlers = bowling.sort_values(by="Wkts", ascending=False).head(20)
st.dataframe(top_bowlers, height=350)

import sys
import os

# Adjust the base directory to your project root (one level up or two based on actual folder depth)
BASE_DIR = r"C:\Users\pc\Desktop\MANVI LABMENTIX\CricBuzz Project"
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utils.db_connection import engine
from utils.models import Base
from data_fetching import get_live_matches

import streamlit as st

# Your Streamlit code here...

st.set_page_config(page_title="Cricbuzz LiveStats", layout="wide")
st.title("🏏 Live Cricket Matches")

# Get live matches
live_matches = get_live_matches()
if not live_matches:
    st.warning("No live matches currently or data unavailable.")
else:
    for match in live_matches:
        st.subheader(match['matchDesc'])
        st.write(f"Teams: {match['team1']} vs {match['team2']}")
        st.write(f"Status: {match['status']}")
        st.write(f"Start Time: {match['startTime']}")
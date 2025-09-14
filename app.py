import streamlit as st

st.set_page_config(page_title="Cricbuzz LiveStats", layout="wide")

st.title("🏏 Cricbuzz LiveStats Dashboard")

st.markdown("""
Welcome to the Cricbuzz LiveStats cricket analytics dashboard!

This platform provides:
- ⚡ Real-time live match updates
- 📊 Detailed player statistics and top performers
- 🔍 Powerful SQL-driven analytics queries
- 🛠️ CRUD operations to manage players and matches

Navigate through the sidebar on the left to explore these features.

---

### How to Use:
- Click *Live Matches* to see ongoing matches and scores.
- Go to *Top Stats* for player performance data.
- Visit *SQL Queries* to run analytics on the cricket database.
- Open *CRUD Operations* to add, edit, or remove player and match info.

---

Happy Cricketing! 🏏
""")

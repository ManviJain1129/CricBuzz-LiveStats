import streamlit as st

def app():
    st.set_page_config(page_title="Cricbuzz LiveStats Dashboard", layout="wide")
    
    # Header with cricket bat emoji
    st.markdown("# 🏏 Cricbuzz LiveStats Dashboard")
    
    st.markdown("""
    Welcome to the Cricbuzz LiveStats cricket analytics dashboard!  
    
    This platform provides:
    """)
    
    # Features with emojis & Unicode icons
    st.markdown("""
    - ⚡ *Real-time live match updates*  
    - 📊 *Detailed player statistics and top performers*  
    - 🔍 *Powerful SQL-driven analytics queries*  
    - 🛠️ *CRUD operations to manage players and matches*
    """)
    
    # Add a cricket image/banner (local image or from web)
    st.image(
    "https://www.cricbuzz.com/a/img/v1/192x192/i1/c170297/cricket_new.jpg",
    caption="Cricket Live Stats & Analytics",
    width=300  # Set image width in pixels
)
    
    st.markdown("---")
    
    # How to use section
    st.header("How to Use:")
    st.markdown("""
    - Click *Live Matches* to see ongoing matches and scores.  
    - Go to *Top Stats* for player performance data.  
    - Visit *SQL Queries* to run analytics on the cricket database.  
    - Open *CRUD Operations* to add, edit, or remove player and match info.
    """)
    
    st.markdown("### Happy Cricketing! 🏏")

if __name__ == "__main__":
    app()
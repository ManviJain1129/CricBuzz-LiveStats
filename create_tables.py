import sqlite3

conn = sqlite3.connect("your_database.db")  # Replace with your actual DB file name
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in database:")
for table in tables:
    print(table[0])

conn.close()

import sqlite3

conn = sqlite3.connect("your_database.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(players);")
columns = cursor.fetchall()

print("Columns in 'players' table:")
for col in columns:
    print(f"Name: {col[1]}, Type: {col[2]}")

conn.close()

import sqlite3

conn = sqlite3.connect("your_database.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(matches);")
columns = cursor.fetchall()

print("Columns in 'matches' table:")
for col in columns:
    print(f"Name: {col[1]}, Type: {col[2]}")

conn.close()

import sqlite3

conn = sqlite3.connect("your_database.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(player_stats);")
columns = cursor.fetchall()

print("Columns in 'player_stats' table:")
for col in columns:
    print(f"Name: {col[1]}, Type: {col[2]}")

conn.close()

import sqlite3

conn = sqlite3.connect("your_database.db")
cursor = conn.cursor()

# Add 'country' column with default 'Unknown'
try:
    cursor.execute("ALTER TABLE players ADD COLUMN country VARCHAR DEFAULT 'Unknown';")
    print("Column 'country' added successfully.")
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e).lower():
        print("Column 'country' already exists, skipping.")
    else:
        print("Error:", e)

conn.commit()
conn.close()

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.models import Base
from utils.db_connection import engine
import sqlite3

def check_table_data():
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()
    tables = ['players', 'matches', 'teams', 'player_stats']
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        count = cursor.fetchone()[0]
        print(f"Table '{table}' has {count} rows.")
    conn.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables created or confirmed existing!")
    
    check_table_data()
    
    import sqlite3
import pandas as pd

conn = sqlite3.connect("your_database.db")  # Use your actual DB filename
df = pd.read_sql_query("SELECT * FROM players;", conn)
print(df)
conn.close()
 
from utils.db_connection import SessionLocal
from utils.models import Player
from sqlalchemy import func

def show_all_players():
    session = SessionLocal()
    players = session.query(Player).all()
    print(f"Total players: {len(players)}")
    for p in players:
        print(f"{p.full_name} | Role: {p.playing_role} | Batting: {p.batting_style} | Bowling: {p.bowling_style} | Country: {p.country}")
    session.close()

def show_players_country_count():
    session = SessionLocal()
    country_counts = session.query(Player.country, func.count(Player.id)).group_by(Player.country).all()
    print("Players count by country:")
    for country, count in country_counts:
        print(f"{country}: {count}")
    session.close() 
    
    from utils.models import Base
    from utils.db_connection import engine
    
    if __name__ == "__main__":
        Base.metadata.create_all(bind=engine)
        print("Tables created or confirmed existing!")

    # Show all players (detailed)
        show_all_players()

    # Show summary count of players per country
        show_players_country_count()
      
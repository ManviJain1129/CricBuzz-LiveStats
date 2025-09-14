import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from bs4 import BeautifulSoup

url = "https://www.cricbuzz.com/cricket-team/india/2/players"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "lxml")

# Get all text and extract player names manually
page_text = soup.get_text()

# List of current India players (visible in your screenshot)
india_players = [
    'Shubman Gill', 'Yashasvi Jaiswal', 'Sai Sudharsan', 'Rohit Sharma',
    'Virat Kohli', 'Suryakumar Yadav', 'Shreyas Iyer', 'Rinku Singh'
    # Add more as you see them on the page
]

players_to_store = []
for player in india_players:
    if player in page_text:
        players_to_store.append({
            'full_name': player,
            'playing_role': 'Player'
        })

print(players_to_store)
print("Total players extracted:", len(players_to_store))



import requests
from bs4 import BeautifulSoup

def scrape_players():
    url = "https://www.cricbuzz.com/cricket-team/india/2/players"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")

    # Get all text and extract player names manually
    page_text = soup.get_text()

    # List of current India players (visible in your screenshot)
    india_players = [
        'Shubman Gill', 
        'Yashasvi Jaiswal', 
        'Sai Sudharsan', 
        'Rohit Sharma',
        'Virat Kohli', 
        'Suryakumar Yadav', 
        'Shreyas Iyer', 
        'Rinku Singh'
    ]

    players_to_store = []
    for player in india_players:
        if player in page_text:
            players_to_store.append({
                'full_name': player,
                'playing_role': 'Player'
            })

    print(f"Found {len(players_to_store)} players")
    for player in players_to_store:
        print(f"- {player['full_name']}")
    
    return players_to_store

if __name__== "__main__":
    players = scrape_players()
    
    from utils.db_connection import SessionLocal
from utils.models import Player  # Assumes your Player SQLAlchemy model exists

def save_players_to_db(players):
    session = SessionLocal()
    try:
        for player in players:
            # Avoid duplicates by checking if already exists
            exists = session.query(Player).filter_by(full_name=player['full_name']).first()
            if not exists:
                new_player = Player(
                    full_name=player['full_name'],
                    playing_role=player['playing_role']
                )
                session.add(new_player)
        session.commit()
        print(f"{len(players)} players saved to database.")
    except Exception as e:
        print(f"Database error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    players = scrape_players()
    save_players_to_db(players)
    
    from utils.db_connection import SessionLocal
from utils.models import Player

session = SessionLocal()
players = session.query(Player).all()
for player in players:
    print(f"{player.id} | {player.full_name} | {player.playing_role}")
session.close()

import requests
from bs4 import BeautifulSoup

from utils.db_connection import SessionLocal
from utils.models import Player
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def scrape_and_save_australia_players():
    url = "https://www.cricbuzz.com/cricket-team/australia/4/players"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")

    # This selector matches all player names (as seen in your DevTools for India)
    player_tags = soup.find_all('div', class_='cb-font-16 text-hvr-underline')
    players_to_store = []
    for tag in player_tags:
        name = tag.get_text(strip=True)
        if name:
            players_to_store.append({'full_name': name, 'playing_role': 'Player'})

    print(f"Found {len(players_to_store)} Australian players")
    for player in players_to_store:
        print(f"- {player['full_name']}")

    # Save to database
    session = SessionLocal()
    try:
        for player in players_to_store:
            exists = session.query(Player).filter_by(full_name=player['full_name']).first()
            if not exists:
                new_player = Player(
                    full_name=player['full_name'],
                    playing_role=player['playing_role']
                )
                session.add(new_player)
        session.commit()
        print(f"{len(players_to_store)} Australian players saved to database.")
    except Exception as e:
        print("Database error:", e)
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    scrape_and_save_australia_players()
    
    
import requests
from bs4 import BeautifulSoup

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_connection import SessionLocal
from utils.models import Player

def scrape_and_save_england_players():
    url = "https://www.cricbuzz.com/cricket-team/england/9/players"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")

    # This selector matches all player names for England as seen in the HTML
    player_tags = soup.find_all('div', class_='cb-font-16 text-hvr-underline')
    players_to_store = []
    for tag in player_tags:
        name = tag.get_text(strip=True)
        if name:
            players_to_store.append({'full_name': name, 'playing_role': 'Player'})

    print(f"Found {len(players_to_store)} England players")
    for player in players_to_store:
        print(f"- {player['full_name']}")

    # Save to database
    session = SessionLocal()
    try:
        for player in players_to_store:
            exists = session.query(Player).filter_by(full_name=player['full_name']).first()
            if not exists:
                new_player = Player(
                    full_name=player['full_name'],
                    playing_role=player['playing_role']
                )
                session.add(new_player)
        session.commit()
        print(f"{len(players_to_store)} England players saved to database.")
    except Exception as e:
        print("Database error:", e)
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    scrape_and_save_england_players() 
    
    
    import requests
from bs4 import BeautifulSoup
import sys
import os

# Ensure Python can find your utils modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_connection import SessionLocal
from utils.models import Player

def scrape_and_save_south_africa_players():
    url = "https://www.cricbuzz.com/cricket-team/south-africa/5/players"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")

    # Select all player names just like for previous countries
    player_tags = soup.find_all('div', class_='cb-font-16 text-hvr-underline')
    players_to_store = []
    for tag in player_tags:
        name = tag.get_text(strip=True)
        if name:
            players_to_store.append({'full_name': name, 'playing_role': 'Player'})

    print(f"Found {len(players_to_store)} South African players")
    for player in players_to_store:
        print(f"- {player['full_name']}")

    # Save to database
    session = SessionLocal()
    try:
        for player in players_to_store:
            exists = session.query(Player).filter_by(full_name=player['full_name']).first()
            if not exists:
                new_player = Player(
                    full_name=player['full_name'],
                    playing_role=player['playing_role']
                )
                session.add(new_player)
        session.commit()
        print(f"{len(players_to_store)} South African players saved to database.")
    except Exception as e:
        print("Database error:", e)
        session.rollback()
    finally:
        session.close()

# Run this function as needed for South Africa!
if __name__ == "__main__":
    scrape_and_save_south_africa_players()
    
    
    import requests
from bs4 import BeautifulSoup
import sys
import os

# Ensure Python can find your utils modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_connection import SessionLocal
from utils.models import Player

def scrape_and_save_pakistan_players():
    url = "https://www.cricbuzz.com/cricket-team/pakistan/3/players"  # Pakistan Team Players Page
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")

    # Select all player names using the same method as previous
    player_tags = soup.find_all('div', class_='cb-font-16 text-hvr-underline')
    players_to_store = []
    for tag in player_tags:
        name = tag.get_text(strip=True)
        if name:
            players_to_store.append({'full_name': name, 'playing_role': 'Player'})
    print(f"Found {len(players_to_store)} Pakistan players")
    for player in players_to_store:
        print(f"- {player['full_name']}")
    # Save to database
    session = SessionLocal()
    try:
        for player in players_to_store:
            exists = session.query(Player).filter_by(full_name=player['full_name']).first()
            if not exists:
                new_player = Player(
                    full_name=player['full_name'],
                    playing_role=player['playing_role']
                )
                session.add(new_player)
        session.commit()
        print(f"{len(players_to_store)} Pakistan players saved to database.")
    except Exception as e:
        print("Database error:", e)
        session.rollback()
    finally:
        session.close()

# Run this function as needed for Pakistan!
if __name__ == "__main__":
    scrape_and_save_pakistan_players()
    
    import requests
from bs4 import BeautifulSoup
import sys
import os

# Ensure Python can find your utils modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_connection import SessionLocal
from utils.models import Player

def scrape_and_save_new_zealand_players():
    url = "https://www.cricbuzz.com/cricket-team/new-zealand/13/players"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")

    # Select all player names just like for previous countries
    player_tags = soup.find_all('div', class_='cb-font-16 text-hvr-underline')
    players_to_store = []
    for tag in player_tags:
        name = tag.get_text(strip=True)
        if name:
            players_to_store.append({'full_name': name, 'playing_role': 'Player'})
    print(f"Found {len(players_to_store)} New Zealand players")
    for player in players_to_store:
        print(f"- {player['full_name']}")
    # Save to database
    session = SessionLocal()
    try:
        for player in players_to_store:
            exists = session.query(Player).filter_by(full_name=player['full_name']).first()
            if not exists:
                new_player = Player(
                    full_name=player['full_name'],
                    playing_role=player['playing_role']
                )
                session.add(new_player)
        session.commit()
        print(f"{len(players_to_store)} New Zealand players saved to database.")
    except Exception as e:
        print("Database error:", e)
        session.rollback()
    finally:
        session.close()

# Run this function as needed for New Zealand!
if __name__ == "__main__":
    scrape_and_save_new_zealand_players()
    
    import requests
from bs4 import BeautifulSoup
import sys
import os

# Ensure Python can find your utils modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_connection import SessionLocal
from utils.models import Player

def scrape_and_save_sri_lanka_players():
    url = "https://www.cricbuzz.com/cricket-team/sri-lanka/5/players"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")

    # Select all player names just like for previous countries
    player_tags = soup.find_all('div', class_='cb-font-16 text-hvr-underline')
    players_to_store = []
    for tag in player_tags:
        name = tag.get_text(strip=True)
        if name:
            players_to_store.append({'full_name': name, 'playing_role': 'Player'})
    print(f"Found {len(players_to_store)} Sri Lanka players")
    for player in players_to_store:
        print(f"- {player['full_name']}")
    # Save to database
    session = SessionLocal()
    try:
        for player in players_to_store:
            exists = session.query(Player).filter_by(full_name=player['full_name']).first()
            if not exists:
                new_player = Player(
                    full_name=player['full_name'],
                    playing_role=player['playing_role']
                )
                session.add(new_player)
        session.commit()
        print(f"{len(players_to_store)} Sri Lanka players saved to database.")
    except Exception as e:
        print("Database error:", e)
        session.rollback()
    finally:
        session.close()

# Run this function as needed for Sri Lanka!
if __name__ == "__main__":
    scrape_and_save_sri_lanka_players()
    
    import requests
from bs4 import BeautifulSoup
import sys
import os

# Ensure Python can find your utils modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_connection import SessionLocal
from utils.models import Player

def scrape_and_save_bangladesh_players():
    url = "https://www.cricbuzz.com/cricket-team/bangladesh/25/players"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")

    # Select all player names just like for previous countries
    player_tags = soup.find_all('div', class_='cb-font-16 text-hvr-underline')
    players_to_store = []
    for tag in player_tags:
        name = tag.get_text(strip=True)
        if name:
            players_to_store.append({'full_name': name, 'playing_role': 'Player'})
    print(f"Found {len(players_to_store)} Bangladesh players")
    for player in players_to_store:
        print(f"- {player['full_name']}")
    # Save to database
    session = SessionLocal()
    try:
        for player in players_to_store:
            exists = session.query(Player).filter_by(full_name=player['full_name']).first()
            if not exists:
                new_player = Player(
                    full_name=player['full_name'],
                    playing_role=player['playing_role']
                )
                session.add(new_player)
        session.commit()
        print(f"{len(players_to_store)} Bangladesh players saved to database.")
    except Exception as e:
        print("Database error:", e)
        session.rollback()
    finally:
        session.close()

# Run this function as needed for Bangladesh!
if __name__ == "__main__":
    scrape_and_save_bangladesh_players()
    
    import requests
from bs4 import BeautifulSoup
import sys
import os

# Ensure Python can find your utils modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_connection import SessionLocal
from utils.models import Player

def scrape_and_save_west_indies_players():
    url = "https://www.cricbuzz.com/cricket-team/west-indies/4/players"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")

    # Select all player names just like for previous countries
    player_tags = soup.find_all('div', class_='cb-font-16 text-hvr-underline')
    players_to_store = []
    for tag in player_tags:
        name = tag.get_text(strip=True)
        if name:
            players_to_store.append({'full_name': name, 'playing_role': 'Player'})
    print(f"Found {len(players_to_store)} West Indies players")
    for player in players_to_store:
        print(f"- {player['full_name']}")
    # Save to database
    session = SessionLocal()
    try:
        for player in players_to_store:
            exists = session.query(Player).filter_by(full_name=player['full_name']).first()
            if not exists:
                new_player = Player(
                    full_name=player['full_name'],
                    playing_role=player['playing_role']
                )
                session.add(new_player)
        session.commit()
        print(f"{len(players_to_store)} West Indies players saved to database.")
    except Exception as e:
        print("Database error:", e)
        session.rollback()
    finally:
        session.close()

# Run this function as needed for West Indies!
if __name__ == "__main__":
    scrape_and_save_west_indies_players()
    
    import requests
from bs4 import BeautifulSoup
import sys
import os

# Ensure Python can find your utils modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_connection import SessionLocal
from utils.models import Player

def scrape_and_save_afghanistan_players():
    url = "https://www.cricbuzz.com/cricket-team/afghanistan/40/players"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")

    # Select all player names just like for previous countries
    player_tags = soup.find_all('div', class_='cb-font-16 text-hvr-underline')
    players_to_store = []
    for tag in player_tags:
        name = tag.get_text(strip=True)
        if name:
            players_to_store.append({'full_name': name, 'playing_role': 'Player'})
    print(f"Found {len(players_to_store)} Afghanistan players")
    for player in players_to_store:
        print(f"- {player['full_name']}")
    # Save to database
    session = SessionLocal()
    try:
        for player in players_to_store:
            exists = session.query(Player).filter_by(full_name=player['full_name']).first()
            if not exists:
                new_player = Player(
                    full_name=player['full_name'],
                    playing_role=player['playing_role']
                )
                session.add(new_player)
        session.commit()
        print(f"{len(players_to_store)} Afghanistan players saved to database.")
    except Exception as e:
        print("Database error:", e)
        session.rollback()
    finally:
        session.close()

# Run this function as needed for Afghanistan!
if __name__ == "__main__":
    scrape_and_save_afghanistan_players()
    
    import requests
from bs4 import BeautifulSoup
import sys
import os

# Ensure Python can find your utils modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_connection import SessionLocal
from utils.models import Player

def scrape_and_save_ireland_players():
    url = "https://www.cricbuzz.com/cricket-team/ireland/55/players"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")

    # Select all player names just like for previous countries
    player_tags = soup.find_all('div', class_='cb-font-16 text-hvr-underline')
    players_to_store = []
    for tag in player_tags:
        name = tag.get_text(strip=True)
        if name:
            players_to_store.append({'full_name': name, 'playing_role': 'Player'})
    print(f"Found {len(players_to_store)} Ireland players")
    for player in players_to_store:
        print(f"- {player['full_name']}")
    # Save to database
    session = SessionLocal()
    try:
        for player in players_to_store:
            exists = session.query(Player).filter_by(full_name=player['full_name']).first()
            if not exists:
                new_player = Player(
                    full_name=player['full_name'],
                    playing_role=player['playing_role']
                )
                session.add(new_player)
        session.commit()
        print(f"{len(players_to_store)} Ireland players saved to database.")
    except Exception as e:
        print("Database error:", e)
        session.rollback()
    finally:
        session.close()

# Run this function as needed for Ireland!
if __name__ == "__main__":
    scrape_and_save_ireland_players()
    
    import requests
from bs4 import BeautifulSoup
import sys
import os

# Ensure Python can find your utils modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_connection import SessionLocal
from utils.models import Player

def scrape_and_save_zimbabwe_players():
    url = "https://www.cricbuzz.com/cricket-team/zimbabwe/9/players"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")

    # Select all player names just like for previous countries
    player_tags = soup.find_all('div', class_='cb-font-16 text-hvr-underline')
    players_to_store = []
    for tag in player_tags:
        name = tag.get_text(strip=True)
        if name:
            players_to_store.append({'full_name': name, 'playing_role': 'Player'})
    print(f"Found {len(players_to_store)} Zimbabwe players")
    for player in players_to_store:
        print(f"- {player['full_name']}")
    # Save to database
    session = SessionLocal()
    try:
        for player in players_to_store:
            exists = session.query(Player).filter_by(full_name=player['full_name']).first()
            if not exists:
                new_player = Player(
                    full_name=player['full_name'],
                    playing_role=player['playing_role']
                )
                session.add(new_player)
        session.commit()
        print(f"{len(players_to_store)} Zimbabwe players saved to database.")
    except Exception as e:
        print("Database error:", e)
        session.rollback()
    finally:
        session.close()

# Run this function as needed for Zimbabwe!
if __name__ == "__main__":
    scrape_and_save_zimbabwe_players()
    
    
    new_player = Player(
    full_name=player['full_name'],
    playing_role=player['playing_role'],
    country="India"  # pass the respective country name here for each scraper
)
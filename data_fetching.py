import os
import sys
import requests
from datetime import datetime

# Add parent directory (project root) to sys.path so utils imports work
project_path = r"C:/Users/pc/Desktop/MANVI LABMENTIX/CricBuzz Project"
if project_path not in sys.path:
    sys.path.insert(0, project_path)

from utils.db_connection import engine, SessionLocal
from utils.models import Base, Match, Team, Player

# Create all tables if not already present
Base.metadata.create_all(bind=engine)
print("All tables created (if not already present).")

# Your RapidAPI credentials
RAPIDAPI_HOST = "cricbuzz-cricket.p.rapidapi.com"
RAPIDAPI_KEY = "2cd68ffe5dmsh66a7797f04645a5p1837aajsncd1e5502a233"

headers = {
    "X-RapidAPI-Host": RAPIDAPI_HOST,
    "X-RapidAPI-Key": RAPIDAPI_KEY
}

# Function to fetch live matches from the API
def get_live_matches():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch live matches.")
        return []

    data = response.json()
    match_list = []
    for series in data.get('typeMatches', []):
        if 'seriesMatches' in series:
            for ser in series['seriesMatches']:
                if 'seriesAdWrapper' in ser and 'matches' in ser['seriesAdWrapper']:
                    for match in ser['seriesAdWrapper']['matches']:
                        info = match['matchInfo']
                        match_list.append({
                            'matchDesc': info['matchDesc'],
                            'team1': info['team1']['teamName'],
                            'team2': info['team2']['teamName'],
                            'status': info.get('status', 'Status Unavailable'),
                            'startTime': info.get('startTime', 'Start time unknown')
                        })
    return match_list

# Fetch recent matches and prepare to store in DB
def fetch_and_store_recent_matches():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch recent matches.")
        return

    data = response.json()
    matches_to_store = []

    for series in data.get('typeMatches', []):
        if 'seriesMatches' in series:
            for ser in series['seriesMatches']:
                if 'seriesAdWrapper' in ser and 'matches' in ser['seriesAdWrapper']:
                    for match in ser['seriesAdWrapper']['matches']:
                        info = match['matchInfo']
                        date_epoch = info.get('startDate')
                        match_date = datetime.fromtimestamp(int(date_epoch) / 1000).date() if date_epoch else None
                        matches_to_store.append({
                            'match_id': info.get('matchId'),
                            'description': info.get('matchDesc'),
                            'team1': info.get('team1', {}).get('teamName'),
                            'team2': info.get('team2', {}).get('teamName'),
                            'venue': info.get('venueInfo', {}).get('ground'),
                            'city': info.get('venueInfo', {}).get('city'),
                            'country': info.get('venueInfo', {}).get('country'),
                            'match_date': match_date,
                            'series_name': info.get('seriesName')
                        })

    session = SessionLocal()
    try:
        for match in matches_to_store:
            exists = session.query(Match).filter_by(
                description=match['description'],
                team1=match['team1'],
                team2=match['team2'],
                match_date=match['match_date']
            ).first()
            if not exists:
                m = Match(
                    description=match['description'],
                    team1=match['team1'],
                    team2=match['team2'],
                    venue=match['venue'],
                    city=match['city'],
                    country=match['country'],
                    match_date=match['match_date']
                )
                session.add(m)
        session.commit()
        print("Recent matches saved to database.")
    except Exception as e:
        session.rollback()
        print("Error saving matches:", e)
    finally:
        session.close()

# Fetch and store teams from the recent matches data
def fetch_and_store_teams(data):
    teams_to_store = []
    for series in data.get('typeMatches', []):
        for ser in series.get('seriesMatches', []):
            for match in ser.get('seriesAdWrapper', {}).get('matches', []):
                for team_key in ['team1', 'team2']:
                    team_info = match['matchInfo'].get(team_key)
                    if team_info:
                        team_dict = {
                            'team_id': team_info.get('teamId'),
                            'team_name': team_info.get('teamName'),
                            'short_name': team_info.get('teamSName')
                        }
                        if team_dict not in teams_to_store:
                            teams_to_store.append(team_dict)
    session = SessionLocal()
    try:
        for t in teams_to_store:
            exists = session.query(Team).filter_by(team_id=t['team_id']).first()
            if not exists:
                team = Team(team_id=t['team_id'], team_name=t['team_name'], short_name=t['short_name'])
                session.add(team)
        session.commit()
        print(f"{len(teams_to_store)} teams saved to the database.")
    except Exception as e:
        session.rollback()
        print("Error saving teams:", e)
    finally:
        session.close()

# Fetch and store players for a given list of team IDs
def fetch_and_store_players(team_ids):
    players_to_store = []
    session = SessionLocal()
    try:
        for team_id in team_ids:
            url = f"https://cricbuzz-cricket.p.rapidapi.com/teams/v1/{team_id}"
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to fetch team {team_id} players.")
                continue
            data = response.json()
            for squad in data.get('squads', []):
                for player in squad.get('players', []):
                    player_dict = {
                        'full_name': player.get('name'),
                        'playing_role': player.get('playingRole'),
                        'batting_style': player.get('battingStyle'),
                        'bowling_style': player.get('bowlingStyle')
                    }
                    if player_dict not in players_to_store:
                        players_to_store.append(player_dict)
        # Insert players into DB avoiding duplicates
        for p in players_to_store:
            exists = session.query(Player).filter_by(full_name=p['full_name']).first()
            if not exists:
                player = Player(
                    full_name=p['full_name'],
                    playing_role=p['playing_role'],
                    batting_style=p['batting_style'],
                    bowling_style=p['bowling_style']
                )
                session.add(player)
        session.commit()
        print(f"{len(players_to_store)} players saved to the database.")
    except Exception as e:
        session.rollback()
        print("Error saving players:", e)
    finally:
        session.close()

# --- Example usage ---
if __name__ == "__main__":
    # Fetch and print live matches
    live_matches = get_live_matches()
    print("Live Matches:")
    for m in live_matches:
        print(f"{m['matchDesc']}: {m['team1']} vs {m['team2']} - Status: {m['status']}")

    # Fetch recent matches and store them
    fetch_and_store_recent_matches()
    
    # You can add calls to fetch_and_store_teams(data) and fetch_and_store_players(team_ids) as needed,
    # once you have the data available
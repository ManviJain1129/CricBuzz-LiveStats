from utils.db_connection import SessionLocal
from utils.models import Player, Match, PlayerStats

def query_sample_data():
    session = SessionLocal()
    try:
        players = session.query(Player).all()
        print("Players:")
        for player in players:
            print(f" - {player.full_name}, Role: {player.playing_role}")

        matches = session.query(Match).all()
        print("\nMatches:")
        for match in matches:
            print(f" - {match.description} on {match.match_date}")

        stats = session.query(PlayerStats).all()
        print("\nPlayer Stats:")
        for stat in stats:
            print(f"Player ID: {stat.player_id}, Match ID: {stat.match_id}, Runs: {stat.runs_scored}, Wickets: {stat.wickets_taken}")
    finally:
        session.close()

if __name__ == "__main__":
    query_sample_data()
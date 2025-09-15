from datetime import date
from utils.db_connection import SessionLocal
from utils.models import Player, Match, PlayerStats

def add_sample_data():
    session = SessionLocal()
    
    # Delete existing data - properly indented inside the function
    session.query(PlayerStats).delete()
    session.query(Player).delete()
    session.query(Match).delete()
    session.commit()

    try:
        # Add sample players
        player1 = Player(full_name="Virat Kohli", playing_role="Batsman", batting_style="Right-hand bat", bowling_style="Right-arm medium")
        player2 = Player(full_name="Jasprit Bumrah", playing_role="Bowler", batting_style="Left-hand bat", bowling_style="Right-arm fast")
        session.add_all([player1, player2])
        session.commit()  # Commit here to get player IDs assigned

        # Add sample match
        match1 = Match(description="India vs Australia", team1="India", team2="Australia", venue="MCG", city="Melbourne", country="Australia", match_date=date(2023, 10, 15))
        session.add(match1)
        session.commit()  # Commit here to get match ID assigned

        # Add sample player stats
        stats1 = PlayerStats(player_id=player1.id, match_id=match1.id, runs_scored=85, wickets_taken=0, catches=2)
        stats2 = PlayerStats(player_id=player2.id, match_id=match1.id, runs_scored=10, wickets_taken=3, catches=0)
        session.add_all([stats1, stats2])
        session.commit()

        print("Sample data added successfully.")
    finally:
        session.close()

if __name__== "__main__":
    add_sample_data()
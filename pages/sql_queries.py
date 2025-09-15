import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cricket SQL Queries with Sample Answers", layout="wide")
st.title("📊 Cricket SQL Queries - Questions & Sample Answers")

queries_and_answers = [
    {
        "title": "1. Players representing India",
        "sql": """
SELECT full_name, playing_role, batting_style, bowling_style 
FROM players 
WHERE country = 'India';
        """,
        "data": {
            "full_name": ["Sachin Tendulkar", "Virat Kohli", "MS Dhoni"],
            "playing_role": ["Batsman", "Batsman", "Wicketkeeper"],
            "batting_style": ["Right-hand bat", "Right-hand bat", "Right-hand bat"],
            "bowling_style": ["None", "Right-arm medium", "None"]
        }
    },
    {
        "title": "2. Cricket matches played in last 30 days",
        "sql": """
SELECT description, team1, team2, venue || ', ' || city AS venue_city, match_date
FROM matches
WHERE match_date >= date('now', '-30 day')
ORDER BY match_date DESC;
        """,
        "data": {
            "description": ["India vs Australia", "England vs Pakistan"],
            "team1": ["India", "England"],
            "team2": ["Australia", "Pakistan"],
            "venue_city": ["Mumbai, Mumbai", "London, London"],
            "match_date": ["2025-08-20", "2025-08-15"]
        }
    },
    {
        "title": "3. Top 10 highest ODI run scorers",
        "sql": """
SELECT p.full_name, SUM(ps.runs_scored) AS total_runs, 
       ROUND(AVG(CASE WHEN ps.runs_scored > 0 THEN ps.runs_scored END),2) AS batting_avg,
       SUM(CASE WHEN ps.runs_scored >= 100 THEN 1 ELSE 0 END) AS centuries
FROM player_stats ps
JOIN players p ON ps.player_id = p.id
JOIN matches m ON ps.match_id = m.id
WHERE m.match_type = 'ODI'
GROUP BY p.full_name
ORDER BY total_runs DESC
LIMIT 10;
        """,
        "data": {
            "full_name": ["Sachin Tendulkar", "Virat Kohli", "Rohit Sharma"],
            "total_runs": [18426, 12169, 9115],
            "batting_avg": [44.83, 59.07, 48.96],
            "centuries": [49, 43, 29]
        }
    },
    {
        "title": "4. Venues with capacity > 50,000",
        "sql": """
SELECT venue_name, city, country, capacity
FROM venues
WHERE capacity > 50000
ORDER BY capacity DESC;
        """,
        "data": {
            "venue_name": ["Melbourne Cricket Ground", "Eden Gardens"],
            "city": ["Melbourne", "Kolkata"],
            "country": ["Australia", "India"],
            "capacity": [100000, 90000]
        }
    },
    {
        "title": "5. Matches won per team",
        "sql": """
SELECT team_name, COUNT(*) AS wins
FROM matches
WHERE winner IS NOT NULL
GROUP BY team_name
ORDER BY wins DESC;
        """,
        "data": {
            "team_name": ["Australia", "India", "England"],
            "wins": [950, 900, 875]
        }
    },
    {
        "title": "6. Count of players per playing role",
        "sql": """
SELECT playing_role, COUNT(*) AS player_count
FROM players
GROUP BY playing_role;
        """,
        "data": {
            "playing_role": ["Batsman", "Bowler", "All-rounder", "Wicketkeeper"],
            "player_count": [350, 300, 150, 50]
        }
    },
    {
        "title": "7. Highest individual batting score per format",
        "sql": """
SELECT m.match_type, MAX(ps.runs_scored) AS highest_score
FROM player_stats ps
JOIN matches m ON ps.match_id = m.id
GROUP BY m.match_type;
        """,
        "data": {
            "match_type": ["Test", "ODI", "T20"],
            "highest_score": [400, 264, 175]
        }
    },
    {
        "title": "8. Cricket series started in 2024",
        "sql": """
SELECT series_name, host_country, match_type, start_date, number_of_matches
FROM series
WHERE strftime('%Y', start_date) = '2024';
        """,
        "data": {
            "series_name": ["Asia Cup 2024", "The Ashes 2024"],
            "host_country": ["Sri Lanka", "England"],
            "match_type": ["ODI", "Test"],
            "start_date": ["2024-07-10", "2024-08-15"],
            "number_of_matches": [10, 5]
        }
    },
    {
        "title": "9. All-rounder players with >1000 runs and >50 wickets",
        "sql": """
SELECT p.full_name, SUM(ps.runs_scored) AS total_runs, SUM(ps.wickets_taken) AS total_wickets, m.match_type
FROM player_stats ps
JOIN players p ON ps.player_id = p.id
JOIN matches m ON ps.match_id = m.id
WHERE p.playing_role = 'All-rounder'
GROUP BY p.full_name, m.match_type
HAVING total_runs > 1000 AND total_wickets > 50;
        """,
        "data": {
            "full_name": ["Jacques Kallis", "Ben Stokes"],
            "total_runs": [11500, 3500],
            "total_wickets": [273, 150],
            "match_type": ["Test", "ODI"]
        }
    },
    {
        "title": "10. Last 20 completed matches details",
        "sql": """
SELECT description, team1, team2, winner, victory_margin, victory_type, venue
FROM matches
WHERE status = 'completed'
ORDER BY match_date DESC
LIMIT 20;
        """,
        "data": {
            "description": ["Match 101", "Match 100"],
            "team1": ["India", "Australia"],
            "team2": ["England", "New Zealand"],
            "winner": ["India", "Australia"],
            "victory_margin": [45, 7],
            "victory_type": ["runs", "wickets"],
            "venue": ["Eden Gardens", "MCG"]
        }
    },
    {
        "title": "11. Player performance across formats (2+ formats played)",
        "sql": """
SELECT p.full_name,
       SUM(CASE WHEN m.match_type = 'Test' THEN ps.runs_scored ELSE 0 END) AS Test_runs,
       SUM(CASE WHEN m.match_type = 'ODI' THEN ps.runs_scored ELSE 0 END) AS ODI_runs,
       SUM(CASE WHEN m.match_type = 'T20I' THEN ps.runs_scored ELSE 0 END) AS T20I_runs,
       AVG(ps.runs_scored) AS overall_batting_avg
FROM player_stats ps
JOIN players p ON ps.player_id = p.id
JOIN matches m ON ps.match_id = m.id
GROUP BY p.full_name
HAVING COUNT(DISTINCT m.match_type) >= 2;
        """,
        "data": {
            "full_name": ["Virat Kohli", "Shakib Al Hasan"],
            "Test_runs": [5000, 3500],
            "ODI_runs": [12000, 4000],
            "T20I_runs": [3000, 1000],
            "overall_batting_avg": [50.5, 42.7]
        }
    },
    {
        "title": "12. Team performance home vs away",
        "sql": """
SELECT t.team_name, 
       SUM(CASE WHEN m.venue_country = t.country AND winner = t.team_name THEN 1 ELSE 0 END) AS home_wins,
       SUM(CASE WHEN m.venue_country != t.country AND winner = t.team_name THEN 1 ELSE 0 END) AS away_wins
FROM matches m
JOIN teams t ON t.team_name IN (m.team1, m.team2)
GROUP BY t.team_name;
        """,
        "data": {
            "team_name": ["India", "Australia"],
            "home_wins": [300, 320],
            "away_wins": [150, 145]
        }
    },
    {
        "title": "13. Batting partnerships of 100+ runs",
        "sql": """
SELECT b1.player_name AS batsman1, 
       b2.player_name AS batsman2,
       SUM(b1.runs_scored + b2.runs_scored) AS partnership_runs,
       b1.match_id, b1.innings
FROM batting_stats b1
JOIN batting_stats b2 ON b1.match_id = b2.match_id 
    AND b1.innings = b2.innings 
    AND b1.batting_position + 1 = b2.batting_position
GROUP BY b1.match_id, b1.innings, b1.batting_position
HAVING partnership_runs >= 100;
        """,
        "data": {
            "batsman1": ["Player A", "Player B"],
            "batsman2": ["Player C", "Player D"],
            "partnership_runs": [120, 105],
            "match_id": [101, 102],
            "innings": [1, 2]
        }
    },
    {
        "title": "14. Bowling performance at venues (3+ matches bowled, 4+ overs)",
        "sql": """
SELECT p.full_name, m.venue, 
       AVG(bs.economy_rate) AS avg_economy, 
       SUM(bs.wickets_taken) AS total_wickets,
       COUNT(DISTINCT m.id) AS matches_played
FROM bowling_stats bs
JOIN players p ON bs.player_id = p.id
JOIN matches m ON bs.match_id = m.id
WHERE bs.overs_bowled >= 4
GROUP BY p.full_name, m.venue
HAVING matches_played >= 3;
        """,
        "data": {
            "full_name": ["James Anderson", "Mitchell Starc"],
            "venue": ["Lord's", "MCG"],
            "avg_economy": [2.85, 3.10],
            "total_wickets": [50, 45],
            "matches_played": [10, 12]
        }
    },
    {
        "title": "15. Player performance in close matches (<50 runs or <5 wickets margin)",
        "sql": """
SELECT p.full_name,
       AVG(ps.runs_scored) AS avg_runs,
       COUNT(DISTINCT ps.match_id) AS close_matches_played,
       SUM(CASE WHEN m.winner = 
         CASE WHEN t.team_name = p.country THEN t.team_name ELSE NULL END THEN 1 ELSE 0 END) AS close_match_wins
FROM player_stats ps
JOIN players p ON ps.player_id = p.id
JOIN matches m ON ps.match_id = m.id
JOIN teams t ON t.team_name IN (m.team1, m.team2)
WHERE (m.victory_margin < 50 AND m.victory_type = 'runs') 
   OR (m.victory_margin < 5 AND m.victory_type = 'wickets')
GROUP BY p.full_name;
        """,
        "data": {
            "full_name": ["Player X", "Player Y"],
            "avg_runs": [45.5, 39.7],
            "close_matches_played": [15, 12],
            "close_match_wins": [9, 8]
        }
    },
    {
        "title": "16. Player batting performance per year since 2020",
        "sql": """
SELECT p.full_name, strftime('%Y', m.match_date) AS year,
       AVG(ps.runs_scored) AS avg_runs, AVG(ps.strike_rate) AS avg_strike_rate,
       COUNT(DISTINCT m.id) AS matches_played
FROM player_stats ps
JOIN players p ON ps.player_id = p.id
JOIN matches m ON ps.match_id = m.id
WHERE m.match_date >= '2020-01-01'
GROUP BY p.full_name, year
HAVING matches_played >= 5
ORDER BY year DESC;
        """,
        "data": {
            "full_name": ["Player A", "Player B"],
            "year": ["2024", "2023"],
            "avg_runs": [50.2, 47.6],
            "avg_strike_rate": [90.5, 88.3],
            "matches_played": [8, 7]
        }
    },
    {
        "title": "17. Toss winner advantage by toss decision",
        "sql": """
SELECT toss_decision,
       ROUND(100.0*SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END)/COUNT(*), 2) AS win_percentage
FROM matches
GROUP BY toss_decision;
        """,
        "data": {
            "toss_decision": ["bat", "field"],
            "win_percentage": [53.4, 48.7]
        }
    },
    {
        "title": "18. Most economical bowlers in ODI and T20",
        "sql": """
SELECT p.full_name, 
       ROUND(SUM(bs.runs_conceded)*1.0/SUM(bs.overs_bowled),2) AS economy_rate,
       SUM(bs.wickets_taken) AS total_wickets
FROM bowling_stats bs
JOIN players p ON bs.player_id = p.id
JOIN matches m ON bs.match_id = m.id
WHERE m.match_type IN ('ODI', 'T20')
GROUP BY p.full_name
HAVING COUNT(DISTINCT bs.match_id) >= 10
   AND AVG(bs.overs_bowled) >= 2
ORDER BY economy_rate ASC;
        """,
        "data": {
            "full_name": ["Bowler A", "Bowler B"],
            "economy_rate": [4.5, 5.0],
            "total_wickets": [80, 75]
        }
    },
    {
        "title": "19. Most consistent batsmen since 2022",
        "sql": """
SELECT p.full_name,
       AVG(ps.runs_scored) AS avg_runs,
       STDDEV(ps.runs_scored) AS runs_stddev
FROM player_stats ps
JOIN players p ON ps.player_id = p.id
JOIN matches m ON ps.match_id = m.id
WHERE ps.balls_faced >= 10 AND m.match_date >= '2022-01-01'
GROUP BY p.full_name
ORDER BY runs_stddev ASC;
        """,
        "data": {
            "full_name": ["Player M", "Player N"],
            "avg_runs": [45.2, 40.1],
            "runs_stddev": [8.5, 9.3]
        }
    },
    {
        "title": "20. Matches played and batting average per format for players with 20+ total matches",
        "sql": """
SELECT p.full_name,
       SUM(CASE WHEN m.match_type = 'Test' THEN 1 ELSE 0 END) AS Test_matches,
       SUM(CASE WHEN m.match_type = 'ODI' THEN 1 ELSE 0 END) AS ODI_matches,
       SUM(CASE WHEN m.match_type = 'T20' THEN 1 ELSE 0 END) AS T20_matches,
       AVG(ps.runs_scored) AS batting_avg
FROM player_stats ps
JOIN players p ON ps.player_id = p.id
JOIN matches m ON ps.match_id = m.id
GROUP BY p.full_name
HAVING SUM(CASE WHEN m.match_type IN ('Test','ODI','T20') THEN 1 ELSE 0 END) >= 20
ORDER BY batting_avg DESC;
        """,
        "data": {
            "full_name": ["Player X", "Player Y"],
            "Test_matches": [15, 20],
            "ODI_matches": [40, 35],
            "T20_matches": [25, 30],
            "batting_avg": [45.6, 42.1]
        }
    },
    {
        "title": "21. Player performance ranking combined score",
        "sql": """
SELECT p.full_name,
       (SUM(ps.runs_scored)*0.01 + AVG(ps.batting_average)*0.5 + AVG(ps.strike_rate)*0.3) AS batting_points,
       (SUM(ps.wickets_taken)*2 + (50 - AVG(ps.bowling_average))*0.5 + (6 - AVG(ps.economy_rate))*2) AS bowling_points,
       (SUM(ps.catches)*3 + SUM(ps.stumpings)*5) AS fielding_points,
       ((SUM(ps.runs_scored)*0.01 + AVG(ps.batting_average)*0.5 + AVG(ps.strike_rate)*0.3) + 
       (SUM(ps.wickets_taken)*2 + (50 - AVG(ps.bowling_average))*0.5 + (6 - AVG(ps.economy_rate))*2) +
       (SUM(ps.catches)*3 + SUM(ps.stumpings)*5)) AS total_score
FROM player_stats ps
JOIN players p ON ps.player_id = p.id
GROUP BY p.full_name
ORDER BY total_score DESC
LIMIT 20;
        """,
        "data": {
            "full_name": ["Player A", "Player B"],
            "batting_points": [150, 140],
            "bowling_points": [90, 95],
            "fielding_points": [40, 50],
            "total_score": [280, 285]
        }
    },
    {
        "title": "22. Head-to-head match stats between teams (last 3 years, 5+ matches)",
        "sql": """
WITH head_to_head AS (
  SELECT 
    CASE WHEN m.team1 < m.team2 THEN m.team1 ELSE m.team2 END AS team_a,
    CASE WHEN m.team1 < m.team2 THEN m.team2 ELSE m.team1 END AS team_b,
    COUNT(*) AS matches_played,
    SUM(CASE WHEN winner = m.team1 THEN 1 ELSE 0 END) AS team1_wins,
    SUM(CASE WHEN winner = m.team2 THEN 1 ELSE 0 END) AS team2_wins,
    AVG(CASE WHEN winner = m.team1 THEN victory_margin ELSE NULL END) AS avg_margin_team1,
    AVG(CASE WHEN winner = m.team2 THEN victory_margin ELSE NULL END) AS avg_margin_team2
  FROM matches m
  WHERE m.match_date >= date('now', '-3 years')
  GROUP BY team_a, team_b
  HAVING matches_played >= 5
)
SELECT * FROM head_to_head
ORDER BY matches_played DESC;
        """,
        "data": {
            "team_a": ["India", "Australia"],
            "team_b": ["England", "New Zealand"],
            "matches_played": [12, 8],
            "team1_wins": [7, 5],
            "team2_wins": [5, 3],
            "avg_margin_team1": [25.4, 15.8],
            "avg_margin_team2": [22.6, 11.3]
        }
    },
    {
        "title": "23. Recent form and momentum in last 10 batting performances",
        "sql": """
WITH last_10 AS (
    SELECT ps.*, ROW_NUMBER() OVER (PARTITION BY ps.player_id ORDER BY m.match_date DESC) AS rn
    FROM player_stats ps
    JOIN matches m ON ps.match_id = m.id
),
form_agg AS (
    SELECT player_id,
      AVG(CASE WHEN rn <= 5 THEN runs_scored ELSE NULL END) AS avg_last_5,
      AVG(CASE WHEN rn <= 10 THEN runs_scored ELSE NULL END) AS avg_last_10,
      SUM(CASE WHEN rn <= 10 AND runs_scored >= 50 THEN 1 ELSE 0 END) AS fifties_count,
      STDDEV(CASE WHEN rn <= 10 THEN runs_scored ELSE NULL END) AS consistency_sd
    FROM last_10
    GROUP BY player_id
)
SELECT p.full_name, fa.avg_last_5, fa.avg_last_10, fa.fifties_count, fa.consistency_sd,
  CASE 
    WHEN fa.avg_last_5 >= 50 THEN 'Excellent Form'
    WHEN fa.avg_last_5 >= 30 THEN 'Good Form'
    WHEN fa.avg_last_5 >= 15 THEN 'Average Form'
    ELSE 'Poor Form' END AS form_category
FROM form_agg fa
JOIN players p ON fa.player_id = p.id
ORDER BY fa.avg_last_5 DESC;
        """,
        "data": {
            "full_name": ["Player X", "Player Y"],
            "avg_last_5": [60.5, 45.3],
            "avg_last_10": [55.2, 40.1],
            "fifties_count": [4, 3],
            "consistency_sd": [8.2, 10.1],
            "form_category": ["Excellent Form", "Good Form"]
        }
    },
    {
        "title": "24. Successful batting partnerships (5+ partnerships)",
        "sql": """
WITH partnerships AS (
  SELECT 
    b1.player_name AS batsman1,
    b2.player_name AS batsman2,
    AVG(b1.runs_scored + b2.runs_scored) AS avg_partnership_runs,
    COUNT(*) AS partnerships_count,
    MAX(b1.runs_scored + b2.runs_scored) AS highest_partnership,
    100.0 * SUM(CASE WHEN b1.runs_scored + b2.runs_scored > 50 THEN 1 ELSE 0 END) / COUNT(*) AS success_rate
  FROM batting_stats b1
  JOIN batting_stats b2 ON b1.match_id = b2.match_id 
    AND b1.innings = b2.innings 
    AND b1.batting_position + 1 = b2.batting_position
  GROUP BY batsman1, batsman2
  HAVING partnerships_count >= 5
)
SELECT * FROM partnerships
ORDER BY success_rate DESC, avg_partnership_runs DESC;
        """,
        "data": {
            "batsman1": ["Player A", "Player B"],
            "batsman2": ["Player C", "Player D"],
            "avg_partnership_runs": [65.4, 62.3],
            "partnerships_count": [6, 7],
            "highest_partnership": [120, 101],
            "success_rate": [85.0, 80.5]
        }
    },
    {
        "title": "25. Player performance time-series quarterly evolution",
        "sql": """
WITH quarterly_stats AS (
  SELECT 
    p.id AS player_id, 
    p.full_name,
    strftime('%Y-Q%q', m.match_date) AS quarter,
    AVG(ps.runs_scored) AS avg_runs,
    AVG(ps.strike_rate) AS avg_strike_rate,
    COUNT(DISTINCT m.id) AS matches_played
  FROM player_stats ps
  JOIN players p ON ps.player_id = p.id
  JOIN matches m ON ps.match_id = m.id
  GROUP BY player_id, quarter
  HAVING matches_played >= 3
), perf_diff AS (
  SELECT player_id, quarter, avg_runs,
    LAG(avg_runs) OVER (PARTITION BY player_id ORDER BY quarter) AS prev_avg_runs,
    avg_runs - LAG(avg_runs) OVER (PARTITION BY player_id ORDER BY quarter) AS diff_runs,
    avg_strike_rate,
    LAG(avg_strike_rate) OVER (PARTITION BY player_id ORDER BY quarter) AS prev_avg_sr,
    avg_strike_rate - LAG(avg_strike_rate) OVER (PARTITION BY player_id ORDER BY quarter) AS diff_sr
  FROM quarterly_stats
)
SELECT player_id, full_name, quarter, avg_runs, diff_runs, avg_strike_rate, diff_sr,
  CASE 
    WHEN diff_runs > 1 AND diff_sr > 1 THEN 'Career Ascending'
    WHEN diff_runs < -1 AND diff_sr < -1 THEN 'Career Declining'
    ELSE 'Career Stable'
  END AS career_phase
FROM perf_diff
ORDER BY player_id, quarter;
        """,
        "data": {
            "player_id": [1, 1, 2, 2],
            "full_name": ["Player A", "Player A", "Player B", "Player B"],
            "quarter": ["2025-Q1", "2025-Q2", "2025-Q1", "2025-Q2"],
            "avg_runs": [45.2, 48.5, 38.0, 35.0],
            "diff_runs": [3.3, 0.0, -3.0, 0.0],
            "avg_strike_rate": [90.1, 92.0, 85.0, 84.0],
            "diff_sr": [1.9, 0.0, -1.0, 0.0],
            "career_phase": ["Career Ascending", "Career Stable", "Career Declining", "Career Stable"]
        }
    }
]

for item in queries_and_answers:
    st.subheader(item["title"])
    st.code(item["sql"], language='sql')
    df = pd.DataFrame(item["data"])
    st.dataframe(df)
    st.markdown("---")
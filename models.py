from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()

class Player(Base):
    __tablename__= 'players'
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, unique=True, index=True)
    playing_role = Column(String)
    batting_style = Column(String)
    bowling_style = Column(String)
    country = Column(String, index=True)

class Match(Base):
    __tablename__= 'matches'
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    team1 = Column(String)
    team2 = Column(String)
    venue = Column(String)
    city = Column(String)
    country = Column(String)
    match_date = Column(Date)

class PlayerStats(Base):
    __tablename__= 'player_stats'
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    match_id = Column(Integer, ForeignKey('matches.id'))
    runs_scored = Column(Integer)
    wickets_taken = Column(Integer)
    catches = Column(Integer)
    player = relationship("Player")
    match = relationship("Match")

class Team(Base):   # <-- Fix: move here, NOT indented inside another class!
    __tablename__= 'teams'
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, unique=True, nullable=False)   # From API
    team_name = Column(String, unique=True, nullable=False)
    short_name = Column(String)
    


    
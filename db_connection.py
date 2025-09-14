from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite database file inside the project folder
DATABASE_URL = "sqlite:///C:/Users/pc/Desktop/MANVI LABMENTIX/CricBuzz Project/your_database.db"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
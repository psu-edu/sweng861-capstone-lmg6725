from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# Create SQLite database
engine = create_engine('sqlite:///users.db',
                       connect_args={"check_same_thread": False})

# Create database sessions (queries and transactions)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
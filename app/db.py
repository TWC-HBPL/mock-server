from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite DB will live in the root directory of the container
DATABASE_URL = "sqlite:///./mock.db"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Call this once at startup
def init_db():
    Base.metadata.create_all(bind=engine)

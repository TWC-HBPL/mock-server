from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    method = Column(String)
    path = Column(String)
    body = Column(String)
    response = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


class MockResponse(Base):
    __tablename__ = "mock_responses"
    id = Column(Integer, primary_key=True, index=True)
    method = Column(String)
    path = Column(String, unique=True)
    response = Column(String)

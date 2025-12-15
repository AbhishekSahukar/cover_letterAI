from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///chat.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
    role = Column(String)
    content = Column(Text)

Base.metadata.create_all(engine)

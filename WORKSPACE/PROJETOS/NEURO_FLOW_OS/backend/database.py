from sqlmodel import SQLModel, create_engine, Session
from .models import NeuralTask, BrainState, FlowSession
import os

DATABASE_URL = os.getenv("NEURO_DATABASE_URL", "sqlite:///./neuro_flow.db")
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

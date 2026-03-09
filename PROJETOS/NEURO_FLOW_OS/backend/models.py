from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field, Relationship, JSON, Column
import uuid

class NeuralTask(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str
    cognitive_weight: int = Field(default=5)  # 1-10
    status: str = Field(default="todo")  # todo, in_progress, done
    priority: float = Field(default=0.0)
    focus_score: float = Field(default=0.0)
    metadata: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    flow_session_id: Optional[str] = Field(default=None, foreign_key="flowsession.id")
    flow_session: Optional["FlowSession"] = Relationship(back_populates="tasks")

class BrainState(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str
    dopamine_level: float
    hrv: float = Field(default=60.0)
    alpha_power: float = Field(default=1.0)
    e2ee_digest: bytes = Field(default=b"")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class FlowSession(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str
    mode: str = Field(default="deep_work")  # deep_work, burnout_recovery
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = Field(default=None)
    foco_atingido: bool = Field(default=False)
    heatmap_data: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    tasks: List[NeuralTask] = Relationship(back_populates="flow_session")

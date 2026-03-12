from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from .database import engine, init_db, get_session
from .models import NeuralTask, BrainState, FlowSession
from .logic import FocusScorer, PriorityMatrix
from .neuro_consilium import neuro_consilium

app = FastAPI(title="NEURO-FLOW OS API", version="3.1")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/tasks", response_model=List[NeuralTask])
def read_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(NeuralTask)).all()
    # Auto-reorder based on current physics
    return PriorityMatrix.reorder(tasks)

@app.post("/tasks", response_model=NeuralTask)
def create_task(task: NeuralTask, session: Session = Depends(get_session)):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.post("/brain-state", response_model=BrainState)
def record_brain_state(state: BrainState, session: Session = Depends(get_session)):
    session.add(state)
    session.commit()
    session.refresh(state)
    
    # Update latest tasks focus score based on this state
    tasks = session.exec(select(NeuralTask).where(NeuralTask.status == "in_progress")).all()
    new_focus = FocusScorer.calculate(state)
    for task in tasks:
        task.focus_score = new_focus
        session.add(task)
    
    session.commit()
    return state

@app.post("/tasks/{task_id}/deliberate")
async def deliberate_task(task_id: str, session: Session = Depends(get_session)):
    task = session.get(NeuralTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    result = await neuro_consilium.deliberate_task(task)
    task.metadata["council_verdict"] = result.get("verdict")
    session.add(task)
    session.commit()
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

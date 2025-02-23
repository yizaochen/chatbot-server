from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database import get_db
from ..models import Assistant
from ..schemas.assistants import AssistantCreate, AssistantUpdate, AssistantResponse

router = APIRouter(prefix="/api/assistant", tags=["Assistant"])


# Create Assistant
@router.post("/", response_model=AssistantResponse)
def create_assistant(assistant_in: AssistantCreate, db: Session = Depends(get_db)):
    new_assistant = Assistant(**assistant_in.model_dump())
    db.add(new_assistant)
    db.commit()
    db.refresh(new_assistant)
    return new_assistant


# Read All Assistants
@router.get("/", response_model=List[AssistantResponse])
def get_assistants(db: Session = Depends(get_db)):
    return db.query(Assistant).all()


# Read Single Assistant
@router.get("/{assistant_id}", response_model=AssistantResponse)
def get_assistant(assistant_id: int, db: Session = Depends(get_db)):
    assistant = db.query(Assistant).filter(Assistant.id == assistant_id).first()
    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")
    return assistant


# Update Assistant
@router.put("/{assistant_id}", response_model=AssistantResponse)
def update_assistant(
    assistant_id: int, assistant_in: AssistantUpdate, db: Session = Depends(get_db)
):
    assistant = db.query(Assistant).filter(Assistant.id == assistant_id).first()
    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")
    for key, value in assistant_in.model_dump().items():
        setattr(assistant, key, value)
    assistant.updated_at = datetime.now()
    db.commit()
    db.refresh(assistant)
    return assistant


# Delete Assistant
@router.delete("/{assistant_id}", response_model=dict)
def delete_assistant(assistant_id: int, db: Session = Depends(get_db)):
    assistant = db.query(Assistant).filter(Assistant.id == assistant_id).first()
    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")
    db.delete(assistant)
    db.commit()
    return {"message": "Assistant deleted successfully"}


# http://127.0.0.1:8000/api/chat/stream?query=Tell+me+a+story

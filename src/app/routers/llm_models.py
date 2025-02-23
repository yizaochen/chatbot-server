from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from sqlalchemy.future import select
from typing import List
from ..database import get_db
from ..models import LLMModel
from ..schemas.llm_models import LLMModelCreate, LLMModelRead

router = APIRouter(prefix="/api/llm_model", tags=["LLM Models"])


@router.post("/", response_model=LLMModelRead)
def create_llm_model(model: LLMModelCreate, db: Session = Depends(get_db)):
    new_model = LLMModel(name=model.name)
    db.add(new_model)
    db.commit()
    db.refresh(new_model)
    return new_model


@router.get("/", response_model=List[LLMModelRead])
def read_llm_models(db: Session = Depends(get_db)):
    result = db.execute(select(LLMModel))
    return result.scalars().all()


@router.get("/{model_id}", response_model=LLMModelRead)
def read_llm_model(model_id: int, db: Session = Depends(get_db)):
    model = db.get(LLMModel, model_id)
    if model is None:
        raise HTTPException(status_code=404, detail="LLM Model not found")
    return model


@router.put("/{model_id}", response_model=LLMModelRead)
def update_llm_model(
    model_id: int, model_data: LLMModelCreate, db: Session = Depends(get_db)
):
    model = db.get(LLMModel, model_id)
    if model is None:
        raise HTTPException(status_code=404, detail="LLM Model not found")
    model.name = model_data.name
    db.commit()
    db.refresh(model)
    return model


@router.delete("/{model_id}")
def delete_llm_model(model_id: int, db: Session = Depends(get_db)):
    model = db.get(LLMModel, model_id)
    if model is None:
        raise HTTPException(status_code=404, detail="LLM Model not found")
    db.delete(model)
    db.commit()
    return {"message": "LLM Model deleted successfully"}

from typing import Any
import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Thread
from app.database import get_db

router = APIRouter(prefix="/threads", tags=["Threads"])
logger = logging.getLogger(__name__)


@router.get("/{user_id}", response_model=dict[str, Any])
def get_threads(user_id: int, db: Session = Depends(get_db)):
    try:
        threads = (
            db.query(Thread)
            .filter(Thread.user_id == user_id, Thread.activated == True)
            .order_by(Thread.id.desc())
            .all()
        )

        if not threads:
            logger.warning(f"No threads found for user_id: {user_id}")
            raise HTTPException(status_code=404, detail="No threads found")

        return {
            "success": True,
            "data": [
                {
                    "id": thread.id,
                    "title": thread.name,
                    "assistant_id": thread.assistant_id,
                }
                for thread in threads
            ],
        }
    except Exception as e:
        logger.error(f"Error fetching threads for user_id {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

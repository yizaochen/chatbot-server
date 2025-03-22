from typing import Any
import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Message
from app.database import get_db

router = APIRouter(prefix="/messages", tags=["messages"])
logger = logging.getLogger(__name__)


@router.get("/{thread_id}", response_model=dict[str, Any])
def get_messages(thread_id: int, db: Session = Depends(get_db)):
    try:
        messages = (
            db.query(Message)
            .filter(Message.thread_id == thread_id)
            .order_by(Message.id.asc())
            .all()
        )

        if not messages:
            logger.warning(f"No messages found for thread_id: {thread_id}")
            raise HTTPException(status_code=404, detail="No messages found")

        return {
            "success": True,
            "data": [
                {
                    "content": message.content,
                    "ai_generated": message.ai_generated,
                }
                for message in messages
            ],
        }
    except Exception as e:
        logger.error(f"Error fetching messages for thread_id {thread_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

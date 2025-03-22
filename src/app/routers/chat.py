from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from app.ai_cores.bc_graph import chat_graph

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    thread_id: int
    input_message: str


@router.post("/")
async def chat(request: ChatRequest):
    # Prepare the configuration dynamically
    config = {
        "configurable": {
            "thread_id": request.thread_id,
        }
    }

    # Construct the user input message
    input_message = HumanMessage(content=request.input_message)

    # Invoke the chat model
    try:
        result = chat_graph.invoke({"messages": [input_message]}, config)
        ai_message = result.get("messages")[-1].content
        return {"message": ai_message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

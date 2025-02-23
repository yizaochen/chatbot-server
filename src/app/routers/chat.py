from typing import AsyncIterable
from dotenv import load_dotenv

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model


load_dotenv()


async def send_message(chain, question: str) -> AsyncIterable[str]:
    try:
        async for token in chain.astream({"question": question}):
            yield token
    except Exception as e:
        print(f"Caught exception: {e}")


router = APIRouter(prefix="/api/chat", tags=["Chat"])
llm = init_chat_model(model="gpt-4o-mini", model_provider="openai")
prompt_rag = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a chatbot designed to answer physics questions",
        ),
        ("human", "{question}"),
    ]
)


@router.get("/stream")
async def stream_llm_response(query: str):
    chain = prompt_rag | llm | StrOutputParser()
    generator = send_message(chain, query)
    return StreamingResponse(generator, media_type="text/event-stream")


# http://127.0.0.1:8000/api/chat/stream?query=Tell+me+a+story

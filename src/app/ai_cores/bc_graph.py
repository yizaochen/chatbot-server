from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.models import Thread, Message
from app.database import SessionLocal

load_dotenv()


def create_chat_model():
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a friendly AI Assistant! Your task is to provide clear and concise answers.",
            ),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )
    return prompt | ChatOpenAI(model="gpt-4o-mini-2024-07-18")


chat_chain = create_chat_model()


def get_db_session():
    with SessionLocal() as session:
        yield session


def get_chat_history(db: Session, thread_id: int) -> list[BaseMessage]:
    thread = db.query(Thread).filter(Thread.id == thread_id).first()
    if not thread or not thread.messages:
        return []
    return [
        (
            AIMessage(content=msg.content)
            if msg.ai_generated
            else HumanMessage(content=msg.content)
        )
        for msg in sorted(thread.messages, key=lambda x: x.created_at)
    ]


def ensure_thread_exists(db: Session, config: dict) -> Thread:
    thread_id = config["configurable"]["thread_id"]
    thread = db.query(Thread).filter(Thread.id == thread_id).first()
    if thread:
        return thread

    new_thread = Thread(
        id=thread_id,
        user_id=config["configurable"]["user_id"],
        assistant_id=config["configurable"]["assistant_id"],
        name=config["configurable"].get("thread_name", "Untitled"),
    )
    db.add(new_thread)
    db.commit()
    return new_thread


def add_messages(db: Session, thread_id: int, messages: list[BaseMessage]):
    message_objects = [
        Message(
            thread_id=thread_id,
            ai_generated=isinstance(msg, AIMessage),
            content=msg.content,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        for msg in messages
    ]
    db.bulk_save_objects(message_objects)
    db.commit()


def call_model(state: MessagesState, config: RunnableConfig) -> dict:
    with next(get_db_session()) as db:
        thread_id = config["configurable"]["thread_id"]
        chat_history = get_chat_history(db, thread_id)
        ai_message = chat_chain.invoke(
            {"history": chat_history, "question": state["messages"][-1].content}
        )
        add_messages(db, thread_id, state["messages"] + [ai_message])
    return {"messages": ai_message}


builder = StateGraph(state_schema=MessagesState)
builder.add_edge(START, "model")
builder.add_node("model", call_model)
chat_graph = builder.compile()

if __name__ == "__main__":
    config = {
        "configurable": {
            "user_id": 1,
            "assistant_id": 1,
            "thread_id": 1,
            "thread_name": "test",
        }
    }

    for message_content in [
        "Use my name to tell a story",
        "use my name to tell a joke",
    ]:
        input_message = HumanMessage(content=message_content)
        for event in chat_graph.stream(
            {"messages": [input_message]}, config, stream_mode="values"
        ):
            event["messages"][-1].pretty_print()

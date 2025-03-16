"""
Reference: https://python.langchain.com/docs/versions/migrating_memory/chat_history/
"""

from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


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
llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18")
chain = prompt | llm

"""
Example:
The thread_id will be in SQL table Thread-id (primary key)

This is a dictionary emulating the SQL table

threads = {
    1: [
        ("human", "hi! I'm bob"),
        ("ai", "hi bob!"),
        ("human", "what was my name?"),
        ("ai", "bob"),
    ],
    2: [
        ("human", "hi! I'm alice"),
        ("ai", "hi alice!"),
        ("human", "what was my name?"),
        ("ai", "alice"),
    ],
}
"""
threads = {}


def get_chat_history_messages(thread_id: int) -> list[BaseMessage]:
    if thread_id not in threads:
        return []
    messages = []
    chat_session = threads[thread_id]
    for message in chat_session:
        if message[0] == "human":
            messages.append(HumanMessage(content=message[1]))
        elif message[0] == "ai":
            messages.append(AIMessage(content=message[1]))
    return messages


def add_messages(thread_id: int, messages: list[BaseMessage]):
    if thread_id not in threads:
        threads[thread_id] = []
    for message in messages:
        if isinstance(message, HumanMessage):
            threads[thread_id].append(("human", message.content))
        elif isinstance(message, AIMessage):
            threads[thread_id].append(("ai", message.content))


# Define the function that calls the model
def call_model(state: MessagesState, config: RunnableConfig) -> list[BaseMessage]:
    # Make sure that config is populated with the session id
    if "configurable" not in config or "thread_id" not in config["configurable"]:
        raise ValueError(
            "Make sure that the config includes the following information: {'configurable': {'thread_id': 'some_value'}}"
        )
    # Fetch the history of messages and append to it any new messages.
    chat_history_messages = get_chat_history_messages(
        config["configurable"]["thread_id"]
    )

    ai_message = chain.invoke(
        {"history": chat_history_messages, "question": state["messages"][-1].content}
    )
    # Finally, update the chat message history to include
    # the new input message from the user together with the
    # repsonse from the model.
    add_messages(config["configurable"]["thread_id"], state["messages"] + [ai_message])
    print("threads", threads)
    return {"messages": ai_message}


# Define a new graph
builder = StateGraph(state_schema=MessagesState)

# Define the two nodes we will cycle between
builder.add_edge(START, "model")
builder.add_node("model", call_model)

graph = builder.compile()


if __name__ == "__main__":
    thread_id = 1
    config = {"configurable": {"thread_id": thread_id}}

    print("threads", threads)

    input_message = HumanMessage(content="hi! I'm bob")
    for event in graph.stream(
        {"messages": [input_message]}, config, stream_mode="values"
    ):
        event["messages"][-1].pretty_print()

    # Here, let's confirm that the AI remembers our name!
    input_message = HumanMessage(content="what was my name?")
    for event in graph.stream(
        {"messages": [input_message]}, config, stream_mode="values"
    ):
        event["messages"][-1].pretty_print()

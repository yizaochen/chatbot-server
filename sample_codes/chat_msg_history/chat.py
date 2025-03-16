from dotenv import load_dotenv

load_dotenv()

import uuid

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import START, MessagesState, StateGraph

from history import get_chat_history

# Define a new graph
builder = StateGraph(state_schema=MessagesState)

# Define a chat model
model = ChatOpenAI(model="gpt-4o-mini-2024-07-18")


# Define the function that calls the model
def call_model(state: MessagesState, config: RunnableConfig) -> list[BaseMessage]:
    # Make sure that config is populated with the session id
    if "configurable" not in config or "session_id" not in config["configurable"]:
        raise ValueError(
            "Make sure that the config includes the following information: {'configurable': {'session_id': 'some_value'}}"
        )
    # Fetch the history of messages and append to it any new messages.
    chat_history = get_chat_history(config["configurable"]["session_id"])
    messages = list(chat_history.messages) + state["messages"]
    ai_message = model.invoke(messages)
    # Finally, update the chat message history to include
    # the new input message from the user together with the
    # repsonse from the model.
    chat_history.add_messages(state["messages"] + [ai_message])
    return {"messages": ai_message}


# Define the two nodes we will cycle between
builder.add_edge(START, "model")
builder.add_node("model", call_model)

graph = builder.compile()

# Here, we'll create a unique session ID to identify the conversation
session_id = uuid.uuid4()
config = {"configurable": {"session_id": session_id}}

input_message = HumanMessage(content="hi! I'm bob")
for event in graph.stream({"messages": [input_message]}, config, stream_mode="values"):
    event["messages"][-1].pretty_print()

# Here, let's confirm that the AI remembers our name!
input_message = HumanMessage(
    content="Do you remember who am I? And Tell me a summary about Harry Potter by roughly 400 words."
)


for msg, metadata in graph.stream(
    {"messages": input_message}, config, stream_mode="messages"
):
    if msg.content and not isinstance(msg, HumanMessage):
        print(msg.content, end="|", flush=True)

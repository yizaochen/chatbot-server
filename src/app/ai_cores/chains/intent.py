"""
Reference: https://python.langchain.com/docs/how_to/structured_output/#the-with_structured_output-method
"""

from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain.schema.runnable import RunnableLambda


load_dotenv()

system = """You are an intent classifier designed for semiconductor IC Design Engineers. Your job is to classify the user's intent into one of two categories:  

- no-RAG => The user is asking a general question that does not require retrieval-augmented generation (RAG).  
- do-RAG => The user is asking a technical question that would benefit from retrieving external knowledge.  

Return a structured response containing the intent classification.

Here are some examples:

example_user: What is a MOSFET?  
example_assistant: {{"intent": "do-RAG"}}  

example_user: How's the weather today?  
example_assistant: {{"intent": "no-RAG"}}  

example_user: Explain the concept of clock skew in digital circuits.  
example_assistant: {{"intent": "do-RAG"}}  

example_user: Good morning!  
example_assistant: {{"intent": "no-RAG"}}"""


class Intent(BaseModel):
    """
    The intent of the user input.
    """

    intent: str = Field(
        description="The intent of the user input, now only supports 'no-RAG' and 'do-RAG'."
    )


# Define a simple callback function
def callback(result):
    print("Finish")
    print("--- In Callback ---")
    print(result)
    return result  # Ensure the result is returned


llm = init_chat_model(model="gpt-4o-mini", model_provider="openai")
structured_llm = llm.with_structured_output(Intent)
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", "{input}")])
few_shot_structured_llm = prompt | structured_llm | RunnableLambda(callback)

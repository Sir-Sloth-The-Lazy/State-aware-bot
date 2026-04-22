from typing_extensions import TypedDict, List
from langgraph.graph.message import add_messages
from typing import Annotated

class State(TypedDict):
    """
    Represents the structure of the state in the LangGraph Agentic AI application.
    """
    
    messages: Annotated[list, add_messages]

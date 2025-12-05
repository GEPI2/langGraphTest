from typing import TypedDict, Annotated, List, Dict, Any, Union
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    The state of the agent in the dynamic graph.
    """
    # Messages history (standard LangGraph pattern)
    messages: Annotated[List[BaseMessage], add_messages]
    
    # Dynamic context storage for variables passed between nodes
    context: Dict[str, Any]
    
    # Error tracking
    error: Union[str, None]

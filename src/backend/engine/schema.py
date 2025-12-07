from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field

class NodeConfig(BaseModel):
    """Configuration for a single node in the graph."""
    id: str = Field(..., description="Unique identifier for the node")
    type: Literal["LLMNode", "CodeNode", "RAGNode", "HumanNode", "StartNode", "EndNode"] = Field(..., description="Type of the node")
    config: Dict[str, Any] = Field(default_factory=dict, description="Specific configuration for the node type")
    position: Optional[Dict[str, float]] = Field(None, description="UI position (x, y)")

class EdgeConfig(BaseModel):
    """Configuration for a directed edge between nodes."""
    source: str = Field(..., description="Source node ID")
    target: str = Field(..., description="Target node ID")
    condition: Optional[str] = Field(None, description="Condition for conditional edges (optional)")

class GraphConfig(BaseModel):
    """Complete configuration for a dynamic LangGraph."""
    id: str = Field(..., description="Unique identifier for the graph")
    name: str = Field(..., description="Human-readable name of the graph")
    description: Optional[str] = Field(None, description="Description of the graph")
    nodes: List[NodeConfig] = Field(..., description="List of nodes")
    edges: List[EdgeConfig] = Field(..., description="List of edges")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

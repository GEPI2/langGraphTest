from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from .schema import GraphConfig
from .state import AgentState
from .node_factory import NodeFactory

class GraphBuilder:
    """
    Builds a LangGraph StateGraph from a GraphConfig.
    """
    def __init__(self):
        self.node_factory = NodeFactory()

    def build_graph(self, config: GraphConfig):
        """
        Constructs and compiles the StateGraph.
        """
        workflow = StateGraph(AgentState)
        
        # 1. Add Nodes
        for node_config in config.nodes:
            node_func = self.node_factory.create_node(node_config)
            workflow.add_node(node_config.id, node_func)
            
        # 2. Add Edges
        for edge_config in config.edges:
            source = edge_config.source
            target = edge_config.target
            
            # Handle START/END mapping if necessary
            # In LangGraph, START and END are special constants
            # If the JSON uses "START" string, we might need to map it, 
            # but usually add_edge handles string "START" if it matches the constant's value or usage.
            # Let's assume the JSON uses "START" and "END" strings which match LangGraph's expectations 
            # or we explicitly map them if they are different objects.
            
            # LangGraph's START is often just "START" string in recent versions, but let's be safe.
            real_source = START if source == "START" else source
            real_target = END if target == "END" else target
            
            if edge_config.condition:
                # TODO: Handle conditional edges dynamically
                # This requires parsing the condition string or having a registry of condition functions
                # For MVP, we skip dynamic conditions or implement a simple one
                pass
            else:
                workflow.add_edge(real_source, real_target)

        # 3. Connect START to StartNode if exists and not already connected
        start_nodes = [n for n in config.nodes if n.type == "StartNode"]
        if start_nodes:
            # Assuming only one StartNode for now
            start_node_id = start_nodes[0].id
            # Check if there is already an edge from START
            has_start_edge = any(e.source == "START" for e in config.edges)
            if not has_start_edge:
                workflow.add_edge(START, start_node_id)
        else:
            # Fallback: Connect START to the first node if no StartNode is defined
            # and no edge from START exists
            has_start_edge = any(e.source == "START" for e in config.edges)
            if not has_start_edge and config.nodes:
                first_node_id = config.nodes[0].id
                print(f"DEBUG: No StartNode found. Auto-connecting START to {first_node_id}")
                workflow.add_edge(START, first_node_id)
                
        # 3. Compile
        # TODO: Add persistence (checkpointer) configuration
        memory = MemorySaver()
        app = workflow.compile(checkpointer=memory)
        
        return app

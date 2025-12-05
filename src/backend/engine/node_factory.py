from typing import Callable, Any, Dict
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from .schema import NodeConfig, NodeConfig
from .state import AgentState

class NodeFactory:
    """
    Factory class to create executable node functions from NodeConfig.
    """
    
    def create_node(self, node_config: NodeConfig) -> Callable[[AgentState], Dict[str, Any]]:
        """
        Creates a node function based on the configuration.
        """
        if node_config.type == "LLMNode":
            return self._create_llm_node(node_config)
        elif node_config.type == "CodeNode":
            return self._create_code_node(node_config)
        elif node_config.type == "RAGNode":
            return self._create_rag_node(node_config)
        elif node_config.type == "HumanNode":
            return self._create_human_node(node_config)
        else:
            raise ValueError(f"Unknown node type: {node_config.type}")

    def _create_llm_node(self, config: NodeConfig):
        """
        Creates a node that calls an LLM.
        """
        model_name = config.config.get("model", "gemini-2.0-flash-exp")
        system_prompt = config.config.get("system_prompt", "You are a helpful assistant.")
        
        # Initialize LLM (In production, this should be cached or managed)
        llm = ChatGoogleGenerativeAI(model=model_name, temperature=0)

        def llm_node_func(state: AgentState):
            messages = state["messages"]
            # Prepend system prompt if needed (or use system message)
            # For simplicity, we just invoke the LLM with the history
            # In a real app, we might want to format the system prompt properly
            
            response = llm.invoke(messages)
            return {"messages": [response]}
        
        return llm_node_func

    def _create_code_node(self, config: NodeConfig):
        """
        Creates a node that executes Python code.
        WARNING: This is a security risk if not sandboxed. 
        For MVP, we assume trusted input or local execution.
        """
        code_str = config.config.get("code", "")
        function_name = config.config.get("function_name", "process")
        
        def code_node_func(state: AgentState):
            print(f"DEBUG: Executing CodeNode with code: {code_str[:50]}...")
            # Dynamic code execution logic
            # We create a local scope and execute the code definition
            local_scope = {}
            try:
                exec(code_str, globals(), local_scope)
                if function_name not in local_scope:
                    raise ValueError(f"Function '{function_name}' not found in code block.")
                
                func = local_scope[function_name]
                result = func(state)
                print(f"DEBUG: CodeNode result: {result}")
                return result
            except Exception as e:
                print(f"DEBUG: CodeNode error: {e}")
                return {"error": str(e)}

        return code_node_func

    def _create_rag_node(self, config: NodeConfig):
        """
        Placeholder for RAG node.
        """
        def rag_node_func(state: AgentState):
            # TODO: Implement RAG logic
            return {"context": {"retrieved_docs": []}}
        return rag_node_func

    def _create_human_node(self, config: NodeConfig):
        """
        Placeholder for Human-in-the-loop node.
        """
        def human_node_func(state: AgentState):
            # This node doesn't do much logic, it's mostly a checkpoint marker
            # But it could process feedback if present
            return {}
        return human_node_func

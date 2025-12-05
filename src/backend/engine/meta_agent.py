from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class MetaAgent:
    """
    An agent that generates code for other agents (nodes).
    """
    def __init__(self, model_name: str = "gemini-2.0-flash-exp"):
        self.llm = ChatGoogleGenerativeAI(model=model_name, temperature=0)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert Python developer for LangGraph agents.
Your task is to generate a Python function based on the user's description.

The function must follow this signature:
```python
from typing import Dict, Any
from .state import AgentState

def process(state: AgentState) -> Dict[str, Any]:
    # Your logic here
    return {"key": "value"} # Updates the state
```

Rules:
1. The function name MUST be `process`.
2. The input argument MUST be `state: AgentState`.
3. The return value MUST be a dictionary that updates the state (LangGraph reducer pattern).
4. Do NOT include any markdown formatting (like ```python) in the output, just the raw code.
5. Import necessary modules inside the function if needed, or at the top level if standard.
6. Handle errors gracefully if possible, returning `{"error": "message"}`.
"""),
            ("user", "{description}")
        ])
        self.chain = self.prompt | self.llm | StrOutputParser()

    def generate_node_code(self, description: str) -> str:
        """
        Generates Python code for a node based on the description.
        """
        code = self.chain.invoke({"description": description})
        
        # Clean up markdown if present (just in case)
        code = code.replace("```python", "").replace("```", "").strip()
        return code

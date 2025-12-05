from src.features.coding_agent.graph import app

# Mermaid 그래프 생성
print(app.get_graph().draw_mermaid())

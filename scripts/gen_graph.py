from src.features.coding_agent.graph import app

mermaid_code = app.get_graph().draw_mermaid()
with open("graph_viz.mermaid", "w", encoding="utf-8") as f:
    f.write(mermaid_code)
print("Graph saved to graph_viz.mermaid")

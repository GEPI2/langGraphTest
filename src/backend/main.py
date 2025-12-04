from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from src.features.coding_agent.graph import app as graph_app
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI(
    title="LangGraph Agent",
    version="1.0",
    description="A simple API server using LangGraph's Runnable interfaces",
)

# CORS 설정 (React 프론트엔드 통신용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 개발 편의상 모든 도메인 허용 (프로덕션에서는 구체적으로 지정 필요)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LangGraph 서빙
# /agent/invoke, /agent/stream, /agent/playground 등의 엔드포인트가 생성됨
def per_req_config_modifier(config, request):
    thread_id = request.headers.get("X-Thread-Id")
    print(f"DEBUG: per_req_config_modifier called. Thread ID from header: {thread_id}")
    if thread_id:
        config["configurable"] = config.get("configurable", {})
        config["configurable"]["thread_id"] = thread_id
    print(f"DEBUG: Final config: {config}")
    return config

add_routes(
    app,
    graph_app,
    path="/agent",
    input_type=dict,
    output_type=dict,
    per_req_config_modifier=per_req_config_modifier,
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

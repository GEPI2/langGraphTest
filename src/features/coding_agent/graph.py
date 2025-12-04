from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from .schema import AgentState
from .nodes import generate_code, execute_code, human_review

def should_continue(state: AgentState):
    """
    실행 후 다음 단계를 결정합니다.
    """
    error = state.get('error')
    iterations = state.get('iterations', 0)
    
    if error:
        if iterations > 3:
            return END  # 3회 이상 실패 시 포기
        return "generate_code"  # 재시도
    
    return "human_review"  # 성공 -> 검토

def after_review(state: AgentState):
    """
    사람 검토 후 다음 단계를 결정합니다.
    """
    feedback = state.get('human_feedback')
    
    if feedback == "APPROVE":
        return END
    
    return "generate_code"  # 피드백 반영 -> 재시도

# 그래프 정의
workflow = StateGraph(AgentState)

# 노드 추가
workflow.add_node("generate_code", generate_code)
workflow.add_node("execute_code", execute_code)
workflow.add_node("human_review", human_review)

# 진입점 설정
workflow.set_entry_point("generate_code")

# 엣지 추가
workflow.add_edge("generate_code", "execute_code")

# 조건부 엣지 추가
workflow.add_conditional_edges(
    "execute_code",
    should_continue,
    {
        "generate_code": "generate_code",
        "human_review": "human_review",
        END: END
    }
)

workflow.add_conditional_edges(
    "human_review",
    after_review,
    {
        "generate_code": "generate_code",
        END: END
    }
)

from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

# ... (기존 코드)

# 체크포인터 설정 (SQLite)
# DB 파일이 없으면 자동 생성됩니다.
conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
memory = SqliteSaver(conn)

# 컴파일 (human_review 전에 중단)
app = workflow.compile(checkpointer=memory, interrupt_before=["human_review"])

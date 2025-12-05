from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from .schema import AgentState
from .nodes import generate_code, execute_code, human_review, general_chat

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
# 노드 추가
workflow.add_node("generate_code", generate_code)
workflow.add_node("execute_code", execute_code)
workflow.add_node("human_review", human_review)
workflow.add_node("general_chat", general_chat) # 일반 대화 노드 추가

# 라우팅 로직 (조건부 진입점)
def route_request(state: AgentState):
    messages = state['messages']
    if not messages:
        return "general_chat"
        
    last_message = messages[-1]
    if hasattr(last_message, 'content'):
        content = last_message.content
    elif isinstance(last_message, dict):
        content = last_message.get('content', '')
    else:
        content = str(last_message)
    
    # 간단한 키워드 기반 라우팅 (실제로는 LLM을 써서 분류하는 게 더 정확함)
    # 여기서는 "코드", "짜줘", "만들어", "함수", "클래스" 등이 있으면 코딩 요청으로 간주
    coding_keywords = ["코드", "짜줘", "만들어", "구현", "작성", "함수", "클래스", "code", "python", "파이썬"]
    if any(keyword in content for keyword in coding_keywords):
        return "generate_code"
    else:
        return "general_chat"

workflow.set_conditional_entry_point(
    route_request,
    {
        "generate_code": "generate_code",
        "general_chat": "general_chat"
    }
)

# 엣지 추가
workflow.add_edge("generate_code", "execute_code")
workflow.add_edge("general_chat", END) # 일반 대화는 바로 종료

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

from langgraph.checkpoint.memory import MemorySaver

# ... (기존 코드)

# 체크포인터 설정 (Memory)
memory = MemorySaver()

# 컴파일 (human_review 전에 중단)
app = workflow.compile(checkpointer=memory, interrupt_before=["human_review"])

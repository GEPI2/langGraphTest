import sys
import io
from typing import Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from .schema import AgentState

# --- 현재는 Mock LLM 사용 (나중에 실제 ChatOpenAI로 교체 예정) ---
# llm = ChatOpenAI(model="gpt-4o")

def generate_code(state: AgentState) -> Dict[str, Any]:
    """
    현재 상태를 기반으로 코드를 생성하거나 수정합니다.
    """
    messages = state['messages']
    error = state.get('error')
    human_feedback = state.get('human_feedback')
    code = state.get('code')
    iterations = state.get('iterations', 0)

    print(f"--- 코드 생성 중 (반복 횟수: {iterations}) ---")

    # 컨텍스트에 따라 프롬프트 구성
    if error:
        prompt = f"이전 코드가 다음 에러로 실패했습니다:\n{error}\n\n코드를 수정해주세요."
        messages.append(HumanMessage(content=prompt))
    elif human_feedback:
        prompt = f"사용자 피드백:\n{human_feedback}\n\n코드를 업데이트해주세요."
        messages.append(HumanMessage(content=prompt))
    elif not code:
        # 초기 생성
        pass 
    
    # 실제 시나리오에서는 여기서 LLM을 호출합니다.
    # 데모를 위해 간단한 생성을 시뮬레이션합니다.
    
    # 시뮬레이션 로직
    if not code:
        # 초안 1: 구문 에러 포함 (데모용 의도적 에러)
        new_code = "print('Hello World')\nprint(1/0) # 의도적 에러"
    elif error and "division by zero" in error:
        # 에러 수정
        new_code = "print('Hello World')\nprint('수정됨: 0으로 나누기 방지')"
    elif human_feedback and "polite" in human_feedback:
        new_code = "print('안녕하십니까, 존경하는 세상이여!')"
    else:
        new_code = code # 변경 없음

    return {"code": new_code, "iterations": iterations + 1, "error": None}

def execute_code(state: AgentState) -> Dict[str, Any]:
    """
    생성된 코드를 (비교적) 안전하게 실행합니다.
    """
    code = state['code']
    print(f"--- 코드 실행 중 ---\n{code}\n--------------------")
    
    # 표준 출력 캡처
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    
    try:
        # 경고: exec()는 위험합니다. 실제 서비스에서는 샌드박스(E2B, Docker 등)를 사용하세요.
        exec(code, {}, {})
        output = redirected_output.getvalue()
        return {"execution_output": output, "error": None}
    except Exception as e:
        return {"error": str(e), "execution_output": None}
    finally:
        sys.stdout = old_stdout

def human_review(state: AgentState) -> Dict[str, Any]:
    """
    사람의 검토를 위한 플레이스홀더입니다.
    실제 앱에서는 여기서 외부 입력을 기다리는 중단점(Breakpoint)이 됩니다.
    """
    print("--- 사람 검토 대기 중 ---")
    # interrupt_before를 사용하면 이 노드는 실제로 아무것도 안 해도 됩니다.
    return {}

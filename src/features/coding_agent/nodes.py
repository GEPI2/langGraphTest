import sys
import io
import os
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from .schema import AgentState

# 환경 변수 로드 (.env)
load_dotenv()

# Gemini 모델 초기화
# API 키는 .env 파일의 GOOGLE_API_KEY를 사용합니다.
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

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

    # 시스템 메시지 추가 (최초 1회)
    if not messages:
        system_prompt = (
            "당신은 파이썬 코딩 전문가입니다. "
            "사용자의 요청에 따라 실행 가능한 파이썬 코드를 작성하세요. "
            "코드는 마크다운 코드 블록(```python ... ```) 없이 순수 코드만 반환하거나, "
            "코드 블록을 포함한다면 파싱 가능한 형태로 제공하세요."
        )
        messages.append(SystemMessage(content=system_prompt))

    # 컨텍스트에 따라 프롬프트 구성
    if error:
        prompt = f"이전 코드가 다음 에러로 실패했습니다:\n{error}\n\n코드를 수정해주세요."
        messages.append(HumanMessage(content=prompt))
    elif human_feedback:
        prompt = f"사용자 피드백:\n{human_feedback}\n\n코드를 업데이트해주세요."
        messages.append(HumanMessage(content=prompt))
    elif not code:
        # 초기 생성 (이미 messages에 사용자 요청이 있다고 가정)
        pass 
    
    # LLM 호출
    response = llm.invoke(messages)
    new_code = response.content
    
    # 마크다운 코드 블록 제거 (간단한 파싱)
    if "```python" in new_code:
        new_code = new_code.split("```python")[1].split("```")[0].strip()
    elif "```" in new_code:
        new_code = new_code.split("```")[1].split("```")[0].strip()

    # 메시지 기록 업데이트 (AI 응답 추가)
    messages.append(response)

    return {"code": new_code, "iterations": iterations + 1, "error": None, "messages": messages}

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

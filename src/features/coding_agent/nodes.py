import sys
import io
import os
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from src.shared.utils.sandbox import run_in_sandbox
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
    생성된 코드를 샌드박스(Docker) 환경에서 실행합니다.
    """
    code = state['code']
    print("--- 코드 실행 중 (Sandbox) ---")
    print(code)
    print("-" * 20)
    
    # 샌드박스 실행
    try:
        # Docker가 없거나 실패할 경우를 대비한 안전장치 (개발 환경용)
        # 실제 프로덕션에서는 Docker가 필수여야 합니다.
        import docker
        try:
            docker.from_env().ping()
            output = run_in_sandbox(code)
        except Exception as e:
            print(f"Docker 연결 실패, 로컬 실행으로 대체합니다: {e}")
            # Fallback to local exec (WARNING: INSECURE)
            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()
            try:
                exec(code)
                output = redirected_output.getvalue()
            except Exception as exec_e:
                output = str(exec_e)
                return {"error": str(exec_e), "execution_output": None}
            finally:
                sys.stdout = old_stdout

    except Exception as e:
        return {"error": str(e), "execution_output": None}

    print(f"Output: {output}")

    # 에러 감지 (간단한 문자열 체크)
    if "Error" in output or "Traceback" in output:
        return {"error": output, "execution_output": None}
    
    return {"execution_output": output, "error": None}

def human_review(state: AgentState) -> Dict[str, Any]:
    """
    사람의 검토를 위한 플레이스홀더입니다.
    실제 앱에서는 여기서 외부 입력을 기다리는 중단점(Breakpoint)이 됩니다.
    """
    print("--- 사람 검토 대기 중 ---")
    # interrupt_before를 사용하면 이 노드는 실제로 아무것도 안 해도 됩니다.
    return {}

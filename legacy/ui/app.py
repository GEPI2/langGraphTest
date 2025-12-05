import streamlit as st
import sys
import os

# 프로젝트 루트 경로 추가 (모듈 임포트 문제 해결)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.features.coding_agent.graph import app
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(page_title="Coding Agent", layout="wide")

st.title("🤖 Self-Correcting Coding Agent")

import uuid

# ... (기존 코드)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    # 매번 새로운 세션 ID 생성 (새로고침 시 대화 초기화)
    st.session_state.thread_id = str(uuid.uuid4())
    print(f"New Thread ID: {st.session_state.thread_id}")
if "waiting_for_review" not in st.session_state:
    st.session_state.waiting_for_review = False
if "current_code" not in st.session_state:
    st.session_state.current_code = ""
# ... (imports)
import pandas as pd

# ... (existing setup)

# 사이드바: 실행 기록 시각화
st.sidebar.title("🔍 실행 기록 (Execution History)")

try:
    # 현재 상태 스냅샷 가져오기
    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    snapshot = app.get_state(config)
    
    if snapshot.values:
        # 1. 현재 상태 정보
        st.sidebar.subheader("현재 상태 (Current State)")
        st.sidebar.json(snapshot.values)
        
        # 2. 실행 히스토리 (노드 방문 순서)
        st.sidebar.subheader("실행 경로 (Execution Path)")
        
        # 히스토리 데이터 복원 (메타데이터 활용)
        # LangGraph의 get_state_history는 최신순으로 반환합니다.
        history = list(app.get_state_history(config))
        
        if history:
            history_data = []
            for state in history:
                meta = state.metadata
                if meta:
                    step = meta.get("step", -1)
                    source = meta.get("source", "unknown")
                    writes = meta.get("writes", {})
                    # 어떤 노드가 실행되었는지 추정 (writes 키 확인)
                    node_name = list(writes.keys())[0] if writes else source
                    
                    history_data.append({
                        "Step": step,
                        "Node": node_name,
                        "Source": source
                    })
            
            # DataFrame으로 변환 및 정렬 (Step 오름차순)
            df = pd.DataFrame(history_data).sort_values("Step")
            st.sidebar.dataframe(df, use_container_width=True)
            
            # 간단한 차트로 시각화 (선택 사항)
            # st.sidebar.line_chart(df.set_index("Step")["Node"]) # 노드 이름은 차트로 그리기 어려움

    else:
        st.sidebar.info("아직 실행 기록이 없습니다.")

except Exception as e:
    st.sidebar.error(f"히스토리 로드 실패: {e}")

# 채팅 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("파이썬 코드를 요청하세요..."):
    # 사용자 메시지 표시 및 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 에이전트 실행
    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    inputs = {
        "messages": [HumanMessage(content=prompt)],
        "iterations": 0
    }

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # 그래프 실행 (스트리밍)
        execution_steps = []
        for event in app.stream(inputs, config):
            for key, value in event.items():
                execution_steps.append(key) # 실행된 노드 기록
                
                if key == "generate_code":
                    new_code = value.get("code", "")
                    st.session_state.current_code = new_code
                    full_response += f"📝 **코드 생성 완료**\n```python\n{new_code}\n```\n\n"
                    message_placeholder.markdown(full_response)
                elif key == "execute_code":
                    output = value.get("execution_output")
                    error = value.get("error")
                    if error:
                        full_response += f"❌ **실행 에러**\n```text\n{error}\n```\n🔄 **자가 수정 중...**\n\n"
                    else:
                        full_response += f"✅ **실행 성공**\n```text\n{output}\n```\n\n"
                    message_placeholder.markdown(full_response)
                elif key == "general_chat":
                    # 일반 대화 응답 표시
                    messages = value.get("messages", [])
                    if messages:
                        last_msg = messages[-1]
                        content = last_msg.content if hasattr(last_msg, "content") else str(last_msg)
                        full_response += f"{content}\n\n"
                        message_placeholder.markdown(full_response)
        
        # 사이드바에 실행 경로 그래프 그리기
        if execution_steps:
            st.sidebar.subheader("실행 경로 시각화 (Execution Graph)")
            graph = "digraph ExecutionPath {\n"
            graph += "  rankdir=LR;\n" # 왼쪽에서 오른쪽으로
            graph += "  node [shape=box, style=filled, fillcolor=lightblue];\n"
            
            # 시작 노드
            graph += "  start [label=\"Start\", shape=circle, fillcolor=lightgray];\n"
            graph += f"  start -> {execution_steps[0]};\n"
            
            # 실행된 노드들 연결
            for i in range(len(execution_steps) - 1):
                graph += f"  {execution_steps[i]} -> {execution_steps[i+1]};\n"
            
            # 마지막 노드
            if execution_steps[-1] == "human_review":
                 graph += f"  {execution_steps[-1]} [fillcolor=orange];\n" # 검토 대기는 주황색
            else:
                 graph += f"  {execution_steps[-1]} -> end;\n"
                 graph += "  end [label=\"End\", shape=circle, fillcolor=lightgray];\n"

            graph += "}"
            st.sidebar.graphviz_chart(graph)

        # 실행이 멈췄는지 확인 (Human Review)
        state = app.get_state(config)
        if state.next and state.next[0] == "human_review":
            st.session_state.waiting_for_review = True
            full_response += "🛑 **사람의 검토가 필요합니다.** 아래에서 승인 또는 거절해주세요."
            message_placeholder.markdown(full_response)
            
            # 마지막 AI 메시지 저장
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# Human Review 컨트롤
if st.session_state.waiting_for_review:
    st.divider()
    st.subheader("👀 코드 검토 (Human Review)")
    st.code(st.session_state.current_code, language="python")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ 승인 (Approve)", type="primary", use_container_width=True):
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            app.update_state(config, {"human_feedback": "APPROVE"})
            
            with st.spinner("마무리 중..."):
                for event in app.stream(None, config):
                    pass # 종료 처리
            
            st.success("승인되었습니다! 작업이 완료되었습니다.")
            st.session_state.waiting_for_review = False
            st.rerun()
            
    with col2:
        feedback = st.text_input("수정 요청 사항 (거절 시 입력)", placeholder="예: 변수명을 더 직관적으로 바꿔줘")
        if st.button("❌ 거절 및 수정 요청 (Reject)", type="secondary", use_container_width=True):
            if feedback:
                config = {"configurable": {"thread_id": st.session_state.thread_id}}
                app.update_state(config, {"human_feedback": feedback})
                
                st.info("수정 요청을 보냈습니다. 에이전트가 코드를 수정합니다.")
                st.session_state.waiting_for_review = False
                st.rerun()
            else:
                st.warning("수정 요청 사항을 입력해주세요.")

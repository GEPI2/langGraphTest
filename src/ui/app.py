import streamlit as st
import sys
import os

# 프로젝트 루트 경로 추가 (모듈 임포트 문제 해결)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.features.coding_agent.graph import app
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(page_title="Coding Agent", layout="wide")

st.title("🤖 Self-Correcting Coding Agent")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "demo_thread_1"
if "waiting_for_review" not in st.session_state:
    st.session_state.waiting_for_review = False
if "current_code" not in st.session_state:
    st.session_state.current_code = ""

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
        for event in app.stream(inputs, config):
            for key, value in event.items():
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

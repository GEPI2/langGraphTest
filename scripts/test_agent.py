from src.features.coding_agent.graph import app

def run_test():
    print("=== Starting Coding Agent Test ===")
    
    # Initial input
    # 의도적으로 에러가 발생하는 코드를 요청하여 자가 치유 기능을 테스트합니다.
    from langchain_core.messages import HumanMessage
    initial_state = {
        "messages": [HumanMessage(content="Hello World를 출력하고, 그 다음 줄에서 0으로 나누는 파이썬 코드를 작성해줘.")], 
        "iterations": 0
    }
    
    # Run until interruption (Human Review)
    print("\n[1] Running until Human Review...")
    thread_config = {"configurable": {"thread_id": "test_thread"}}
    
    for event in app.stream(initial_state, thread_config):
        for key, value in event.items():
            print(f"Node: {key}")
            if "execution_output" in value:
                print(f"Output: {value['execution_output']}")
            if "error" in value:
                print(f"Error: {value['error']}")

    # Check state at interruption
    current_state = app.get_state(thread_config)
    print(f"\n[Status] Next Node: {current_state.next}")
    print(f"[Status] Current Code:\n{current_state.values['code']}")

    # Simulate Human Approval
    print("\n[2] Simulating Human Approval...")
    app.update_state(thread_config, {"human_feedback": "APPROVE"})
    
    for event in app.stream(None, thread_config):
        print(f"Event: {event}")

    print("\n=== Test Complete ===")

if __name__ == "__main__":
    run_test()

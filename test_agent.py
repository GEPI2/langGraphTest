from src.features.coding_agent.graph import app

def run_test():
    print("=== Starting Coding Agent Test ===")
    
    # Initial input
    initial_state = {"messages": [], "iterations": 0}
    
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

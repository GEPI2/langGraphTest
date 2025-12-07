import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY not found in environment variables.")
    exit(1)

print(f"Loaded API Key: {api_key[:5]}...{api_key[-5:]}")

try:
    print("Initializing ChatOpenAI...")
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)
    
    print("Sending request to OpenAI...")
    response = llm.invoke([HumanMessage(content="Hello, are you working?")])
    
    print("\n--- Response from OpenAI ---")
    print(response.content)
    print("----------------------------")
    print("Success! API Key is valid and working.")

except Exception as e:
    print("\n--- Error Occurred ---")
    print(e)
    print("----------------------")
    print("Failed to get response from OpenAI.")

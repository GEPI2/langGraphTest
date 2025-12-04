from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    print(f"Key loaded: {api_key[:4]}...{api_key[-4:]}")
else:
    print("Key NOT loaded")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
try:
    print("Invoking Gemini...")
    res = llm.invoke("Hi")
    print("Success!")
    print(res.content)
except Exception as e:
    print("Error occurred:")
    print(e)

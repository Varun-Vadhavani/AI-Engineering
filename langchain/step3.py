from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

messages = [
    SystemMessage(content="You are a pirate. Always answer in pirate speak, max 2 sentences."),
    HumanMessage(content="What is LangChain?"),
]

response = model.invoke(messages)

print(response.content)
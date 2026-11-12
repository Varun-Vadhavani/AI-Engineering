from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

response = model.invoke("In one sentence, what is LangChain?")

print(response.content)
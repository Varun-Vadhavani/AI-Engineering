from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

response = model.invoke("In one sentence, what is LangChain?")

print("TYPE:", type(response))
print("CONTENT:", response.content)
print("USAGE:", response.usage_metadata)
print("METADATA:", response.response_metadata)
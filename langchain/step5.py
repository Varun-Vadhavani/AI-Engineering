from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {persona}. Answer in at most {max_sentences} sentences."),
    ("human", "{question}"),
])

# 1) Fill the template and LOOK at the result (no model call yet)
filled = prompt.invoke({
    "persona": "pirate",
    "max_sentences": 2,
    "question": "What is LangChain?",
})
print(filled.to_messages())

# 2) Send the filled prompt to the model
print(model.invoke(filled).content)

# 3) Same thing, using a chain: prompt | model
chain = prompt | model
print(chain.invoke({
    "persona": "strict teacher",
    "max_sentences": 1,
    "question": "What is LangChain?",
}).content)
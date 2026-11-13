from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from models import get_model

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {persona}. Keep answers under 80 words."),
    ("human", "{question}"),
])

chain = prompt | get_model() | StrOutputParser()

for piece in chain.stream({
    "persona": "friendly tutor",
    "question": "Why does streaming make an app feel faster?",
}):
    print(piece, end="", flush=True)
print()
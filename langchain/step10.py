from langchain_core.prompts import ChatPromptTemplate
from models import get_model

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer in at most two sentences."),
    ("human", "{question}"),
])

chain = prompt | get_model()
r = chain.invoke({"question": "What is a prompt template?"})
print(r.content)
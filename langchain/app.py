from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from models import get_model

LABELS = ["code", "math", "general"]

def clean(raw):
    raw = raw.strip().lower()
    return next((l for l in LABELS if l in raw), "general")

def build():
    base = get_model()
    classify = (
        ChatPromptTemplate.from_template(
            "Classify this question with one word: code, math or general.\n\nQuestion: {question}")
        | base.with_config(tags=["step:classify"])
        | StrOutputParser()
    )
    answer = (
        ChatPromptTemplate.from_template(
            "This is a {label} question. Answer it clearly.\n\nQuestion: {question}")
        | base.with_config(tags=["step:answer"])
        | StrOutputParser()
    )
    return RunnablePassthrough.assign(label=classify | clean) | answer
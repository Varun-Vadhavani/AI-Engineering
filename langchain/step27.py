from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from models import get_model

model = get_model()

points_chain = (
    ChatPromptTemplate.from_template(
        "List the 3 most important points of this text as short bullet lines:\n\n{text}"
    )
    | model
    | StrOutputParser()
)

tweet_chain = (
    ChatPromptTemplate.from_template(
        "Turn these points into one friendly tweet under 250 characters:\n\n{points}"
    )
    | model
    | StrOutputParser()
)

# Join them. The lambda in the middle is ordinary Python:
# it reshapes step A's output into the dict that step B's prompt expects.
pipeline = points_chain | (lambda points: {"points": points.strip()}) | tweet_chain

article = """Streaming sends a model's answer piece by piece instead of waiting for the
whole thing. It does not make the model faster, but users see the first words almost
immediately, so the app feels much quicker. Developers still need to collect the pieces
into a full answer to save it, and must handle cancelled or broken streams."""

# Debug the first step alone, which is the benefit of splitting
print("STEP A ONLY:\n", points_chain.invoke({"text": article}), "\n")

# Now the whole chain
result = pipeline.invoke({"text": article})
print("FINAL TWEET:\n", result)
print("Length:", len(result))
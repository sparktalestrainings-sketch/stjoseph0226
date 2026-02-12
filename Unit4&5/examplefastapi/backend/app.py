from fastapi import FastAPI
from langserve import add_routes
from langchain_core.runnables import RunnableLambda
from langchain_groq import ChatGroq

app = FastAPI()


def stock_chat(data: dict):
    user_input = data["message"]
    api_key = data["api_key"]

    # Initialize LLM dynamically using sidebar key
    llm = ChatGroq(
        groq_api_key=api_key,
        model="llama-3.3-70b-versatile"
    )

    # Simple stock demo logic
    if "price" in user_input.lower():
        symbol = user_input.split()[-1].upper()
        return f"Demo: Current price of {symbol} is $100"

    # Otherwise use LLM
    return llm.invoke(user_input).content


chain = RunnableLambda(stock_chat)

add_routes(app, chain, path="/chat")

### Router

from typing import Literal, TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama


# Data model
class RouteQuery(TypedDict):
    """Route a user query to the most relevant datasource."""
    datasource: Literal["vectorstore", "web_search"]  # Given a user question choose to route it to web search or a vectorstore.


def create_question_router(model="gpt-4o-mini", temperature=0):
    """
    Cria e retorna um router que decide se uma pergunta deve ser direcionada
    para vectorstore ou web search.
    
    Returns:
        RunnableSequence: Pipeline de routing que retorna RouteQuery
    """
    # LLM with function call
    if model.startswith("gpt"):
        llm = ChatOpenAI(model=model, temperature=temperature).with_structured_output(RouteQuery)
    elif model.startswith("llama") or model.startswith("deepseek"):
        llm = ChatOllama(model=model).with_structured_output(RouteQuery)
    else:
        raise ValueError(f"Invalid model: {model}")

    # Prompt
    system = """You are an expert at routing a user question to a vectorstore or web search working for Norte, a Venture Capital firm.
    The vectorstore contains documents in Norte's internal meetings, engaged companies meeting notes, investment comitee meetings, etc.
    Use the vectorstore for questions on these topics. Otherwise, use web-search."""
    route_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "{question}"),
        ]
    )

    return route_prompt | llm

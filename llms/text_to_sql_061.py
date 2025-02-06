from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_anthropic import ChatAnthropic
from langchain_community.agent_toolkits import create_sql_agent

def create_text_to_sql(model="gpt-4o", temperature=0):
    """
    Cria e retorna uma chain RAG (Retrieval Augmented Generation) para responder
    perguntas com base em documentos recuperados.
    
    Returns:
        RunnableSequence: Pipeline RAG que retorna uma resposta em texto
    """
    # Prompt

    if model == "o1-mini" or model == "o1-preview" or model == "o1":
        temperature = 1

    # LLM
    if model.startswith("gpt"):
        llm = ChatOpenAI(model=model, temperature=temperature)
    elif model.startswith("llama") or model.startswith("deepseek"):
        llm = ChatOllama(model=model, temperature=temperature)
    elif model.startswith("claude") or model.startswith("opus"):
        llm = ChatAnthropic(model=model, temperature=temperature)
    else:
        raise ValueError(f"Invalid model: {model}")

    # Chain
    return llm

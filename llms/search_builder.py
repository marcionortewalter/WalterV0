from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

def construct_search_query(model="gpt-4o-mini", temperature=0):
    """
    Transforma uma pergunta em uma frase para ser usada em uma busca de dados num search engine.
    
    Args:
        docs: Lista de documentos com page_content e metadata
        
    Returns:
        str: Documentos formatados em texto
    """
    
    if model.startswith("gpt"):
        llm = ChatOpenAI(model=model, temperature=temperature)
    elif model.startswith("llama") or model.startswith("deepseek"):
        llm = ChatOllama(model=model, temperature=temperature)
    else:
        raise ValueError(f"Invalid model: {model}")

    prompt = PromptTemplate.from_template("""
    You are an expert at creating search queries for search engines.
    You are given a question and you need to create a search query for a search engine. Just return the search query, no other text.
    Limit your search to 5 essential words. Make company names and fund names the first words of each query.
    Question: {question}
    Search query:
    """)

    return prompt | llm


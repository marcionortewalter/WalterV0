from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama.llms import OllamaLLM
from langchain_anthropic import ChatAnthropic

def format_docs(docs):
    """
    Formata uma lista de documentos em uma string única com metadados.
    
    Args:
        docs: Lista de documentos com page_content e metadata
        
    Returns:
        str: Documentos formatados em texto
    """
    return "\n\n".join(f"{doc.page_content}\nMetadata: {doc.metadata}" for doc in docs)

def create_rag_chain(model="gpt-4o", temperature=0):
    """
    Cria e retorna uma chain RAG (Retrieval Augmented Generation) para responder
    perguntas com base em documentos recuperados.
    
    Returns:
        RunnableSequence: Pipeline RAG que retorna uma resposta em texto
    """
    # Prompt
    custom_prompt = PromptTemplate.from_template("""
    You are an experienced partner at Norte, a Venture Capital firm in Brazil that has been asked a question.
    Use the all of the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know, but display the information.
    Your answer should be a detailed technical analysis founded on reality. Use common information if needed.
    You are to be used by Venture Capital firm executives. So you need to be detailed, but also give strategic insight. Think outside the box.
    Be transparent about where you are taking information from, quoting documents for key information (don't overdo it). In the end, display a well formatted summary with:
    url, created_at, file name, file type. For web search results, just display the url.
    Question: {question}
    Context: {context}
    Answer:
    """)

    if model == "o1-mini" or model == "o1-preview" or model == "o1":
        temperature = 1

    # LLM with function call
    if model.startswith("gpt"):
        llm = ChatOpenAI(model=model, temperature=temperature)
    elif model.startswith("llama") or model.startswith("deepseek"):
        llm = OllamaLLM(model=model)
    elif model.startswith("claude"):
        llm = ChatAnthropic(model=model, temperature=temperature)
    else:
        raise ValueError(f"Invalid model: {model}")

    # Chain
    return custom_prompt | llm | StrOutputParser()

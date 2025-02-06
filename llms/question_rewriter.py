### Question Re-writer

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

def create_question_rewriter(model="gpt-4o-mini", temperature=0):
    """
    Cria e retorna um rewriter que converte uma pergunta para uma versão melhorada que é otimizada para busca em vectorstore.
    
    Returns:
        RunnableSequence: Pipeline de rewriter que retorna a pergunta melhorada
    """

    # LLM with function call
    if model.startswith("gpt"):
        llm = ChatOpenAI(model=model, temperature=temperature)
    elif model.startswith("llama") or model.startswith("deepseek"):
        llm = ChatOllama(model=model)
    else:
        raise ValueError(f"Invalid model: {model}")

    # Prompt
    system = """You a question re-writer that converts an input question to a better version that is optimized \n 
        for vectorstore retrieval. Look at the input and try to reason about the underlying semantic intent / meaning.
        Since we are looking up in the "Norte" company database, remove "Norte" from the search.
        Keep in mind that Norte is a Venture Capital firm in Brazil.
        """
    re_write_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            (
                "human",
                "Here is the initial question: \n\n {question} \n Formulate an improved question.",
            ),
        ]
    )

    return re_write_prompt | llm | StrOutputParser()
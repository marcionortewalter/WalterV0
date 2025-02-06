### Retrieval Grader

from typing import Literal, TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

# Data model
class GradeDocuments(TypedDict):
    """Binary score for relevance check on retrieved documents."""

    binary_score: Literal["yes", "no"]


def create_document_grader(model="gpt-4o-mini", temperature=0):
    """
    Cria e retorna um grader que avalia a relevância de documentos recuperados
    em relação à pergunta do usuário.
    
    Returns:
        RunnableSequence: Pipeline de grading que retorna GradeDocuments
    """
    # LLM with function call
    if model.startswith("gpt"):
        llm = ChatOpenAI(model=model, temperature=temperature).with_structured_output(GradeDocuments)
    elif model.startswith("llama") or model.startswith("deepseek"):
        llm = ChatOllama(model=model).with_structured_output(GradeDocuments)
    else:
        raise ValueError(f"Invalid model: {model}")


    # Prompt
    system = """You are a grader assessing relevance of a retrieved document to a user question. \n 
        If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
        It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.\n
        When in doubt, grade it as relevant.\n
        For example, if a document mentions a relevant company, fund, or person that shows up in the question, grade it as relevant.
        """
    grade_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
        ]
    )

    return grade_prompt | llm
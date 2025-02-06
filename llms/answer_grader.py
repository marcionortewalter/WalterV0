### Answer Grader

from typing import Literal, TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
# Data model
class GradeAnswer(TypedDict):
    """Binary score to assess answer addresses question."""

    binary_score: Literal["yes", "no"] # Answer should be yes or no

def create_answer_grader(model="gpt-4o-mini", temperature=0):
    """
    Cria e retorna um grader que avalia se uma resposta resolve uma pergunta.
    
    Returns:
        RunnableSequence: Pipeline de grader que retorna GradeAnswer
    """
    # LLM with function call
    if model.startswith("gpt"):
        llm = ChatOpenAI(model=model, temperature=temperature).with_structured_output(GradeAnswer)
    elif model.startswith("llama") or model.startswith("deepseek"):
        llm = ChatOllama(model=model).with_structured_output(GradeAnswer)
    else:
        raise ValueError(f"Invalid model: {model}")

    # Prompt
    system = """You are a grader assessing whether an answer addresses / resolves a question \n 
        Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question."""
    answer_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
        ]
    )

    return answer_prompt | llm
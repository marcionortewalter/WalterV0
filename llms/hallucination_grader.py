from typing import Literal, TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

# Data model
class GradeHallucinations(TypedDict):
    """Binary score for hallucination present in generation answer."""

    binary_score: Literal["yes", "no"] # Answer should be yes or no

def create_hallucination_grader(model="gpt-4o-mini", temperature=0):
    """
    Cria e retorna um grader que avalia se uma resposta é baseada em fatos.
    
    Returns:
        RunnableSequence: Pipeline de grader que retorna GradeHallucinations
    """

    # LLM with function call
    if model.startswith("gpt"):
        llm = ChatOpenAI(model=model, temperature=temperature).with_structured_output(GradeHallucinations)
    elif model.startswith("llama") or model.startswith("deepseek"):
        llm = ChatOllama(model=model).with_structured_output(GradeHallucinations)
    else:
        raise ValueError(f"Invalid model: {model}")

    # Prompt
    system = """You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts. \n 
        Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts."""
    
    hallucination_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}"),
        ]
    )

    return hallucination_prompt | llm
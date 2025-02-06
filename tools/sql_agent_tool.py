from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.tools import Tool

from tools.utils.db_schema import get_db_schema_string
from database.engine import create_all_clients
from llms.text_to_sql_061 import create_text_to_sql
from llms.prompts.text_to_sql import prompt, examples
from langchain.tools import tool

### DATABASE ###
db, sqlalchemy_db, db_psycopg2, supabase_client = create_all_clients()

### LLM ###
llm = create_text_to_sql(model="claude-3-5-haiku-20241022")

### SCHEMA ###
TABLES_TO_EXCLUDE = ["documents", "documents_large", "notes_history", "fundraising_fund_2"]
VIEWS_TO_INCLUDE = ["view_intros"]

schema = get_db_schema_string(db, db_psycopg2, TABLES_TO_EXCLUDE, VIEWS_TO_INCLUDE)

def create_agent():
    """
    Cria e retorna um agente SQL.
    
    Returns:
        Agent: Agent SQL
    """

    ### Get relevant examples
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        OpenAIEmbeddings(),
        FAISS,
        k=5,
        input_keys=["input"],
    )

    ### Few shot prompt
    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=PromptTemplate.from_template(
            "User input: {input}\nSQL query: {query}"
        ),
        input_variables=["input", "dialect", "top_k", "schema"],
        prefix=prompt,
        suffix="",
    )

    ### Full prompt
    full_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate(prompt=few_shot_prompt),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    ### Create agent
    agent = create_sql_agent(
        llm=llm,
        db=db,
        prompt=full_prompt,
        verbose=True,
        agent_type="openai-tools" if llm.model.startswith("gpt") else "tool-calling"
    )

    return agent

def run_agent(input, schema=schema, dialect="postgresql", top_k=5):
    agent = create_agent()
    return agent.run({
        "input": input,
        "schema": schema,
        "dialect": dialect,
        "top_k": top_k
    })

@tool
def internal_sql_query(input: str):
    """
    Executa consultas SQL baseadas em linguagem natural. 
    Use esta ferramenta quando precisar consultar o banco de dados.
    O agente recebe uma pergunta e retorna sua análise a partir dessa pergunta ao fazer
    consultas ao banco de dados. Ao pedir dados de uma pessoa, empresa ou membro, sempre dê o maximo de informações possíveis.
    Para perguntas qualitativas, é útil usar também o retriever
    
    Args:
        input (str): A pergunta a ser analisada.

    Returns:
        str: A análise da pergunta a partir das consultas ao banco de dados.
    """
    return run_agent(input)

if __name__ == "__main__":
    run_agent("""
    What funds can help us coinvest in WeHandle?
    Please analyze:
    - Industry match
    - Ticket size compatibility with round size.
    - Round stage compatibility (Seed, Pre-seed, Series A, etc)
    - Fund VC Quality Perception of 5 (sort funds by this column. It goes from 1-5)
    - Remove funds with No Call meeting frequency
    - Fund meeting frequency
    - Any relevant observations
    
    Format the response with:
    1. Brief summary of the company's profile
    2. List of recommended funds with bullet points for key criteria
    3. Brief explanation of why each fund is a good match
    4. a list of all compatible funds, even those that are not very recommended (By compatibility, look only at stage and ticket size)""")


import os
from streamlit import secrets as st_secrets
os.environ["OPENAI_API_KEY"] = st_secrets.OPENAI_API_KEY
os.environ["ANTHROPIC_API_KEY"] = st_secrets.ANTHROPIC_API_KEY
os.environ["TAVILY_API_KEY"] = st_secrets.TAVILY_API_KEY
os.environ["SUPABASE_PASSWORD"] = st_secrets.SUPABASE_PASSWORD
os.environ["SUPABASE_URL"] = st_secrets.SUPABASE_URL
os.environ["SUPABASE_KEY"] = st_secrets.SUPABASE_KEY
os.environ["LANGSMITH_API_KEY"] = st_secrets.LANGSMITH_API_KEY
os.environ["LANGSMITH_PROJECT"] = st_secrets.LANGSMITH_PROJECT
os.environ["LANGGRAPH_API_URL"] = st_secrets.LANGGRAPH_API_URL
os.environ["LANGCHAIN_API_KEY"] = st_secrets.LANGCHAIN_API_KEY
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["NORTE_FOLDER_ID"] = st_secrets.NORTE_FOLDER_ID
os.environ["ATTIO_API_KEY"] = st_secrets.ATTIO_API_KEY


from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver

from tools.retriever_tool import internal_retriever
from tools.sql_agent_tool import internal_sql_query
from tools.email_tool import create_email_draft_tool, send_email_to_address_tool
from tools.calendar_tool import send_calendar_invite_tool, get_events_for_days_tool
from tools.attio_write_tool import create_new_attio_task_tool

from utils import _print_event

from datetime import datetime

model = ChatOpenAI(model="gpt-4o", streaming=True, callbacks=[StreamingStdOutCallbackHandler()])

checkpoint = MemorySaver()
config = {"configurable": {"thread_id": "test-thread"}}

tools = [
    # create_email_draft_tool,
    # send_email_to_address_tool,
    internal_retriever,
    internal_sql_query,
    # send_calendar_invite_tool,
    # get_events_for_days_tool,
    create_new_attio_task_tool
]

tool_names = [tool.name for tool in tools]

prompt = f'''You are an experienced partner at Norte, a Venture Capital firm in Brazil that has been asked a question.
At Norte, we speak both English and Portuguese.
Your name is Walter.
You have to answer the question as best you can. You have access to the following tools:

{tools}

If the answer isn't good enough, ask the user for info like what attio list they want to check.
You currently have access to the following attio lists:
companies
people
intros to funds
deals engaged
intros to funds

Today is {datetime.now()}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!'''


graph = create_react_agent(
    model=model,
    tools=tools,
    prompt=prompt,
    checkpointer=checkpoint
)

if __name__ == "__main__":
    _printed = set()
    while True:
        user_input = input("Digite sua pergunta (ou 'sair' para encerrar): ")
    
        if user_input.lower() == 'sair':
            break
            
        for step in graph.stream(
            {"messages": [("human", user_input)]}, stream_mode="values", config=config
        ):
            _print_event(step, _printed)

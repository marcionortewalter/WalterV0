import os
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from supabase import create_client
from langchain.tools import tool

def create_retriever():
    """
    Creates and returns a retriever connected to Supabase vectorstore
    
    Returns:
        Retriever: Configured retriever for document search
    """
    # Supabase credentials
    SUPABASE_URL = os.environ["SUPABASE_URL"]
    SUPABASE_KEY = os.environ["SUPABASE_KEY"]

    # Create Supabase client
    supabase_client = create_client(
        supabase_url=SUPABASE_URL,
        supabase_key=SUPABASE_KEY
    )

    # Initialize vectorstore
    vectorstore = SupabaseVectorStore(
        client=supabase_client,
        table_name="documents_large", 
        embedding=OpenAIEmbeddings(model="text-embedding-3-large", dimensions=3072),
        query_name="weighted_match_documents_large",
    )

    # Create and return retriever
    return vectorstore.as_retriever(search_kwargs={"k": 5})

@tool
def internal_retriever(input: str):
    """
    Retriever: Configured retriever for document search. 
    This tool can be used to search for information in the company's meeting notes, investment memos, and other documents.
    This can be used as a last resort to answer questions.

    Args:
        input (str): The query to search for
    
    Returns:
        List[Document]: The list of documents that match the query
    """
    return create_retriever().get_relevant_documents(input)

if __name__ == "__main__":
    print(internal_retriever("What is the company's profile?"))

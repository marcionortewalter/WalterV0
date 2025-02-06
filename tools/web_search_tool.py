### Search

from langchain_community.tools.tavily_search import TavilySearchResults

def create_web_search_tool(k=5):
    """
    Cria e retorna uma ferramenta de busca web.
    
    Returns:
        TavilySearchResults: Ferramenta de busca web
    """
    return TavilySearchResults(k=k)

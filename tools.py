"""
Custom tools for the AI News Agent.
"""
from langchain_tavily import TavilySearchResults
from config import Config


def create_search_tool():
    """
    Create and configure the web search tool using Tavily.
    
    Returns:
        TavilySearchResults: Configured search tool for the agent.
    """
    search_tool = TavilySearchResults(
        max_results=Config.MAX_SEARCH_RESULTS,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=False,
        include_images=False,
        api_key=Config.TAVILY_API_KEY,
        name="search_web",
        description=(
            "Search the web for current information about AI and automation news. "
            "Use this tool to find recent articles, developments, and trends in "
            "artificial intelligence and automation technology."
        )
    )
    
    return search_tool


def get_all_tools():
    """
    Get all tools available for the agent.
    
    Returns:
        list: List of tools for the agent.
    """
    return [create_search_tool()]

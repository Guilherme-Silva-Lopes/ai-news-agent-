"""
Custom tools for the AI News Agent.
"""
from langchain_community.tools.tavily_search import TavilySearchResults
from config import Config


def create_search_tool():
    """
    Create and configure the web search tool using Tavily.
    
    Returns:
        TavilySearchResults: Configured search tool for the agent.
    """
    search_tool = TavilySearchResults(
        max_results=10,  # More results for better selection
        search_depth="advanced",
        include_answer=True,
        include_raw_content=False,
        include_images=False,
        days=1,  # Filter to last 24 hours only
        api_key=Config.TAVILY_API_KEY,
        name="search_web",
        description=(
            "Search the web for RECENT AI and automation news from the last 24 hours. "
            "Use this tool to find the latest articles, developments, and trends in "
            "artificial intelligence and automation technology. Always prioritize recent news."
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

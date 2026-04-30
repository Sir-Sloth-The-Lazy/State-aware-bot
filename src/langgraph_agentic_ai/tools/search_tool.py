from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

def get_tools():
    """
    Return the list of tools to be used in the chatbot
    """
    
    tools = [TavilySearchResults(max_results=2)]
    return tools

def create_tool_nodes(tools):
    """
    Create ToolNode instances for each tool in tools.
    """
    return ToolNode(tools=tools)
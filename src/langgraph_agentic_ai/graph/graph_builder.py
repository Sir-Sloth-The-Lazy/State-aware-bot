from langgraph.graph import StateGraph, START , END
from src.langgraph_agentic_ai.state.state import State
from src.langgraph_agentic_ai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraph_agentic_ai.tools.search_tool import get_tools, create_tool_nodes

class GraphBuilder:
    def __init__(self, model):
        self.llm_model = model
        self.graph_builder = StateGraph(State)
        
    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph with a single message node.
        This method initializes the chatbot node using the 'BasicChatbotNode' class 
        and connects it to the start and end nodes of the graph.
        The chatbot node is set as both entrance and exit point for the graph, 
        allowing for a simple conversational flow.
        
        Returns:
            StateGraph: The constructed graph representing the chatbot's conversational flow.
        """
        
        self.basic_chatbot_node = BasicChatbotNode(self.llm_model)

        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)
    
    def chatbot_with_tools_build_graph(self):
        """
        Builds a chatbot graph that incorporates tools for enhanced functionality.
        This method initializes the chatbot node and integrates it with tool nodes created from the provided tools.
        The graph is structured to allow the chatbot to utilize the tools during conversations, 
        enabling more complex interactions and responses.

        Returns:
            StateGraph: The constructed graph representing the chatbot's conversational flow with tool integration.
        """
        
        

    def setup_graph(self, usecase):
        """
        Sets up the graph based on the selected use case.
        Currently, it supports a "Research Assistant" use case, which builds a basic chatbot graph.

        Args:
            usecase (str): The selected use case for which the graph needs to be set up.
        """
        if usecase == "Research Assistant":
            self.basic_chatbot_build_graph()
        else:
            raise ValueError("Unsupported use case")
        return self.graph_builder.compile()
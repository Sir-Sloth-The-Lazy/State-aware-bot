import streamlit as st
from src.langgraph_agentic_ai.ui.streamlit.loadUI import LoadStreamlitUI
from src.langgraph_agentic_ai.llms.groqllm import GroqLLM
from src.langgraph_agentic_ai.graph.graph_builder import GraphBuilder
from src.langgraph_agentic_ai.ui.streamlit.display_out import DisplayOutStreamlit

def load_langgraph_agenticai_app():
    """
    This function initializes and runs the LangGraph Agentic AI Streamlit application. 
    It loads the UI components, captures user input, and serves as the main entry point for the app.
    Returns:
        None
    """
    
    #Load UI
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()
    
    if not user_input : 
        st.error("Error : Failed to load user input from the UI")
        return

    user_message = st.chat_input("Enter your message : ")
    
    if user_message : 
        try: 
            # Configure the LLM
            obj_llm_config = GroqLLM(user_controls_input = user_input)
            model = obj_llm_config.get_llm_model()
            
            if not model : 
                st.error("Error : LLM model could not be initialized")
                return
            # initialize chatbot node on the usecase
            usecase = user_input.get("selected_usecase")
            
            if not usecase : 
                st.error("Error : No usecase selected")
                return
            
            #graph builder
            graph_builder = GraphBuilder(model)
            try :
                graph = graph_builder.setup_graph(usecase)
                DisplayOutStreamlit(usecase,graph,user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error setting up graph for usecase '{usecase}': {str(e)}")
                return
        except Exception as e:
                st.error(f"Error: {str(e)}")
                return

            
            
            
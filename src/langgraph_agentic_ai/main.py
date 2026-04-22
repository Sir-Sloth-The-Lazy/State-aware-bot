import streamlit as st
from src.langgraph_agentic_ai.ui.streamlit.loadUI import LoadStreamlitUI

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
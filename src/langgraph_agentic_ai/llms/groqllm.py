import os
import streamlit as st
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input
        
    def get_llm_model(self):
        try:
            groq_api_key = self.user_controls_input.get("GROQ_API_KEY", "")
            selected_groq_model = self.user_controls_input.get("selected_model")
            if not groq_api_key and not os.environ.get("GROQ_API_KEY"):
                st.error("Error: GROQ API key is not set. Please enter your API key in the sidebar.")
                return None
            llm_model = ChatGroq(model=selected_groq_model, api_key=groq_api_key or os.environ.get("GROQ_API_KEY"))
            return llm_model
        except Exception as e:
            st.error(f"Error initializing GROQ LLM: {str(e)}")
            return None
    
            
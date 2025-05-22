"""
Utilities for handling interactions with Google's Gemini models
"""

import google.generativeai as genai
import streamlit as st
from typing import Optional
import time
import re

def estimate_token_count(text: str) -> int:
    """
    Estimate the number of tokens in a text string
    A rough estimate based on words and punctuation
    """
    # Split on whitespace and punctuation
    tokens = re.findall(r'\w+|[^\w\s]', text)
    return len(tokens)

def truncate_text(text: str, max_chars: int = 15000) -> str:
    """
    Truncate text to fit within Gemini Flash model's context window
    Using character count as a conservative approach since Flash model
    is optimized for shorter inputs
    """
    return text[:max_chars]

def retry_with_backoff(func, max_retries=3, initial_delay=1):
    """
    Retry a function with exponential backoff
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            error_str = str(e).lower()
            if "safety" in error_str or "blocked" in error_str:
                st.error(f"Content blocked by safety filters: {str(e)}")
                return None
            elif "quota" in error_str:
                st.error("API quota exceeded. Please check your billing details or try again later.")
                return None
            else:
                if attempt == max_retries - 1:
                    st.error(f"Gemini API error: {str(e)}")
                    return None
                delay = initial_delay * (2 ** attempt)
                time.sleep(delay)

def generate_report(content: str, length_preference: str, gemini_api_key: str) -> Optional[str]:
    """
    Generate a report using Google's Gemini Pro model
    
    Args:
        content (str): Content to generate report from
        length_preference (str): Desired length of the report (Short/Medium/Detailed)
        gemini_api_key (str): Google API key
        
    Returns:
        Optional[str]: Generated report text or None if there's an error
    """
    # Configure the Gemini API
    genai.configure(api_key=gemini_api_key)
    
    # Initialize the model (using Flash model for faster response times)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    length_instructions = {
        "Short": "Create a concise summary in about 250 words.",
        "Medium": "Create a detailed summary in about 500 words.",
        "Detailed": "Create a comprehensive report in about 1000 words."
    }
    
    # Truncate content if needed (Gemini has a larger context window than GPT-3.5)
    truncated_content = truncate_text(content)
    
    prompt = f"""Based on the following content, {length_instructions[length_preference]}
    Focus on key information and insights. Structure the report with clear headings and sections.
    
    Content: {truncated_content}"""
    
    def make_api_call():
        chat = model.start_chat(history=[])
        response = chat.send_message(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                candidate_count=1,
                stop_sequences=None,
                top_p=0.95,
                top_k=40,
            )
        )
        return response.text

    response = retry_with_backoff(make_api_call)
    return response
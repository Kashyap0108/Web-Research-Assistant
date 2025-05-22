"""
Utilities for handling interactions with OpenAI's language models
"""

from openai import OpenAI, RateLimitError, APIError, BadRequestError, AuthenticationError
import streamlit as st
from typing import Optional, Dict
import tiktoken
import time

def count_tokens(text: str) -> int:
    """Count the number of tokens in a text string"""
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(text))

def truncate_content(content: str, max_tokens: int) -> str:
    """Truncate content to fit within token limit"""
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(content)
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
        content = encoding.decode(tokens)
    return content

def retry_with_backoff(func, max_retries=3, initial_delay=1):
    """
    Retry a function with exponential backoff
    """
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise e
            delay = initial_delay * (2 ** attempt)  # exponential backoff
            time.sleep(delay)
        except (BadRequestError, AuthenticationError) as e:
            if "insufficient_quota" in str(e).lower():
                st.error("OpenAI API quota exceeded. Please check your billing details or try again later.")
            else:
                st.error(f"OpenAI API error: {str(e)}")
            return None
        except APIError as e:
            st.error(f"OpenAI API error: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None

def generate_report(content: str, length_preference: str, openai_api_key: str) -> Optional[str]:
    """
    Generate a report using OpenAI's GPT model
    
    Args:
        content (str): Content to generate report from
        length_preference (str): Desired length of the report (Short/Medium/Detailed)
        openai_api_key (str): OpenAI API key
        
    Returns:
        Optional[str]: Generated report text or None if there's an error
    """
    client = OpenAI(api_key=openai_api_key)
    
    # Define token limits
    MAX_TOTAL_TOKENS = 4096  # GPT-3.5-turbo total token limit
    MAX_OUTPUT_TOKENS = 2000  # Maximum tokens for response
    SYSTEM_PROMPT_TOKENS = 50  # Approximate tokens for system prompt
    
    length_instructions = {
        "Short": "Create a concise summary in about 250 words.",
        "Medium": "Create a detailed summary in about 500 words.",
        "Detailed": "Create a comprehensive report in about 1000 words."
    }
    
    # Calculate available tokens for content
    instruction_tokens = count_tokens(length_instructions[length_preference])
    available_content_tokens = MAX_TOTAL_TOKENS - MAX_OUTPUT_TOKENS - SYSTEM_PROMPT_TOKENS - instruction_tokens - 100  # 100 tokens buffer
    
    # Truncate content if needed
    truncated_content = truncate_content(content, available_content_tokens)
    
    prompt = f"""Based on the following content, {length_instructions[length_preference]}
    Focus on key information and insights. Structure the report with clear headings and sections.
    
    Content: {truncated_content}"""
    
    def make_api_call():
        return client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional report writer. Create well-structured, informative reports based on provided content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=MAX_OUTPUT_TOKENS
        )

    response = retry_with_backoff(make_api_call)
    if response is not None:
        return response.choices[0].message.content
    return None
"""
Utilities for extracting content from web pages
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import streamlit as st

def extract_content(search_results: List[Dict[str, str]]) -> str:
    """
    Extract content from web pages found in search results
    
    Args:
        search_results (List[Dict[str, str]]): List of search results with URLs
        
    Returns:
        str: Concatenated extracted content from all pages
    """
    all_content = []
    
    for result in search_results:
        try:
            response = requests.get(
                result["link"],
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
                timeout=10
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Remove script and style elements
            for element in soup(["script", "style", "nav", "header", "footer"]):
                element.decompose()
            
            # Extract text from paragraphs and headers
            content = ""
            for tag in soup.find_all(["p", "h1", "h2", "h3", "h4", "article"]):
                text = tag.get_text(strip=True)
                if text and len(text) > 50:  # Filter out short snippets
                    content += text + "\n\n"
            
            if content:
                all_content.append(f"Source: {result['title']}\n{content}")
                
        except Exception as e:
            st.warning(f"Could not extract content from {result['link']}: {str(e)}")
            continue
    
    return "\n---\n".join(all_content) if all_content else "No content could be extracted from the search results."
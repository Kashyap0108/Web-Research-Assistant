"""
Utilities for performing web searches using SerpAPI
"""

import requests
from typing import List, Dict
import streamlit as st

def perform_web_search(query: str, api_key: str) -> List[Dict[str, str]]:
    """
    Perform a web search using SerpAPI
    
    Args:
        query (str): Search query
        api_key (str): SerpAPI key
        
    Returns:
        List[Dict[str, str]]: List of search results with 'title' and 'link' keys
    """
    base_url = "https://serpapi.com/search"
    
    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google",
        "num": 5  # Number of results to return
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "error" in data:
            st.error(f"Search API error: {data['error']}")
            return []
            
        organic_results = data.get("organic_results", [])
        
        return [
            {
                "title": result.get("title", ""),
                "link": result.get("link", ""),
                "snippet": result.get("snippet", "")
            }
            for result in organic_results
        ]
        
    except requests.RequestException as e:
        st.error(f"Error performing web search: {str(e)}")
        return []
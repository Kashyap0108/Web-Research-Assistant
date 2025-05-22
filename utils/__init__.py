"""
Web Research Assistant utility modules
"""

from .search_utils import perform_web_search
from .content_extractor import extract_content
from .llm_handler import generate_report
from .document_generator import generate_pdf, generate_docx

__all__ = [
    'perform_web_search',
    'extract_content',
    'generate_report',
    'generate_pdf',
    'generate_docx'
]
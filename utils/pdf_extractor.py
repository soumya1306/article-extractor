"""
PDF text extraction utilities for research articles
"""

from pypdf import PdfReader
from typing import Optional, Dict, Any
import io


def extract_text_from_pdf(pdf_file) -> Dict[str, Any]:
    """
    Extract text from a PDF file.
    
    Args:
        pdf_file: File-like object or path to PDF
        
    Returns:
        Dictionary containing extracted text and metadata
    """
    try:
        # Create PDF reader
        reader = PdfReader(pdf_file)
        
        # Extract metadata
        metadata = {
            'num_pages': len(reader.pages),
            'title': reader.metadata.title if reader.metadata and reader.metadata.title else 'Unknown',
            'author': reader.metadata.author if reader.metadata and reader.metadata.author else 'Unknown',
        }
        
        # Extract text from all pages
        full_text = ""
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text += f"\n--- Page {page_num + 1} ---\n{text}\n"
        
        # Check if extraction was successful
        if not full_text.strip():
            raise ValueError("No text could be extracted from the PDF. It might be a scanned image or encrypted.")
        
        return {
            'success': True,
            'text': full_text,
            'metadata': metadata,
            'error': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'text': None,
            'metadata': None,
            'error': str(e)
        }


def extract_text_from_abstract(abstract_text: str) -> Dict[str, Any]:
    """
    Process plain text abstract input.
    
    Args:
        abstract_text: Plain text abstract or paper excerpt
        
    Returns:
        Dictionary containing processed text
    """
    if not abstract_text.strip():
        return {
            'success': False,
            'text': None,
            'metadata': None,
            'error': 'Abstract text is empty'
        }
    
    return {
        'success': True,
        'text': abstract_text,
        'metadata': {
            'source': 'plain_text',
            'length': len(abstract_text)
        },
        'error': None
    }


def preprocess_text(text: str, max_length: Optional[int] = None) -> str:
    """
    Preprocess extracted text for better AI processing.
    
    Args:
        text: Raw extracted text
        max_length: Maximum character length (for token limit management)
        
    Returns:
        Preprocessed text
    """
    # Remove excessive whitespace
    lines = text.split('\n')
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    cleaned_text = '\n'.join(cleaned_lines)
    
    # Truncate if necessary
    if max_length and len(cleaned_text) > max_length:
        cleaned_text = cleaned_text[:max_length] + "\n\n[Text truncated due to length...]"
    
    return cleaned_text


def estimate_tokens(text: str) -> int:
    """
    Rough estimation of token count (approximately 4 characters per token).
    
    Args:
        text: Input text
        
    Returns:
        Estimated token count
    """
    return len(text) // 4

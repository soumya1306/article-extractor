"""
Text chunking utility with overlap support for processing large documents.
Provides flexible chunking strategies for text processing and retrieval tasks.
"""

import re
from typing import List, Dict, Tuple


class TextChunker:
    """Handles text chunking with configurable chunk size and overlap."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the TextChunker.
        
        Args:
            chunk_size: Target size of each chunk in characters.
            chunk_overlap: Number of characters to overlap between chunks.
        """
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size")
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_by_characters(self, text: str) -> List[str]:
        """
        Chunk text by character count with overlap.
        
        Args:
            text: The text to chunk.
            
        Returns:
            List of text chunks.
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk = text[start:end]
            chunks.append(chunk)
            
            # Move start position by (chunk_size - overlap)
            start += self.chunk_size - self.chunk_overlap
        
        return chunks
    
    def chunk_by_sentences(self, text: str) -> List[str]:
        """
        Chunk text by sentences with overlap.
        Attempts to keep sentences together to avoid splitting mid-sentence.
        
        Args:
            text: The text to chunk.
            
        Returns:
            List of text chunks.
        """
        # Split by common sentence endings
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = []
        current_length = 0
        overlap_buffer = []
        
        for sentence in sentences:
            sentence_length = len(sentence) + 1  # +1 for space
            
            if current_length + sentence_length > self.chunk_size and current_chunk:
                # Save current chunk
                chunk_text = ' '.join(current_chunk)
                chunks.append(chunk_text)
                
                # Prepare overlap for next chunk
                overlap_length = 0
                overlap_buffer = []
                for sent in reversed(current_chunk):
                    overlap_length += len(sent) + 1
                    overlap_buffer.insert(0, sent)
                    if overlap_length >= self.chunk_overlap:
                        break
                
                # Start new chunk with overlap
                current_chunk = overlap_buffer.copy()
                current_length = sum(len(s) + 1 for s in current_chunk)
            
            current_chunk.append(sentence)
            current_length += sentence_length
        
        # Add remaining text
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def chunk_by_paragraphs(self, text: str) -> List[str]:
        """
        Chunk text by paragraphs with overlap.
        Keeps paragraphs together for better semantic cohesion.
        
        Args:
            text: The text to chunk.
            
        Returns:
            List of text chunks.
        """
        # Split by double newline (paragraph breaks)
        paragraphs = re.split(r'\n\s*\n', text)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        chunks = []
        current_chunk = []
        current_length = 0
        overlap_buffer = []
        
        for paragraph in paragraphs:
            para_length = len(paragraph) + 2  # +2 for paragraph spacing
            
            if current_length + para_length > self.chunk_size and current_chunk:
                # Save current chunk
                chunk_text = '\n\n'.join(current_chunk)
                chunks.append(chunk_text)
                
                # Prepare overlap for next chunk
                overlap_length = 0
                overlap_buffer = []
                for para in reversed(current_chunk):
                    overlap_length += len(para) + 2
                    overlap_buffer.insert(0, para)
                    if overlap_length >= self.chunk_overlap:
                        break
                
                # Start new chunk with overlap
                current_chunk = overlap_buffer.copy()
                current_length = sum(len(p) + 2 for p in current_chunk)
            
            current_chunk.append(paragraph)
            current_length += para_length
        
        # Add remaining text
        if current_chunk:
            chunks.append('\n\n'.join(current_chunk))
        
        return chunks
    
    def chunk_with_metadata(self, text: str, method: str = "characters") -> List[Dict[str, any]]:
        """
        Chunk text and return metadata about each chunk.
        
        Args:
            text: The text to chunk.
            method: Chunking method - "characters", "sentences", or "paragraphs".
            
        Returns:
            List of dictionaries containing chunk text and metadata.
        """
        if method == "sentences":
            chunks = self.chunk_by_sentences(text)
        elif method == "paragraphs":
            chunks = self.chunk_by_paragraphs(text)
        else:
            chunks = self.chunk_by_characters(text)
        
        chunk_data = []
        char_position = 0
        
        for idx, chunk in enumerate(chunks):
            # Find actual position in original text
            char_position = text.find(chunk, char_position)
            
            chunk_data.append({
                "chunk_id": idx,
                "text": chunk,
                "length": len(chunk),
                "start_position": char_position,
                "end_position": char_position + len(chunk),
                "method": method
            })
            
            char_position += len(chunk)
        
        return chunk_data
    
    def estimate_tokens(self, text: str, tokens_per_char: float = 0.25) -> int:
        """
        Estimate the number of tokens in text.
        
        Args:
            text: The text to estimate tokens for.
            tokens_per_char: Approximate tokens per character (default ~0.25).
            
        Returns:
            Estimated token count.
        """
        return int(len(text) * tokens_per_char)
    
    def get_chunks_by_token_limit(self, text: str, max_tokens: int, method: str = "characters") -> List[str]:
        """
        Generate chunks that fit within a token limit.
        
        Args:
            text: The text to chunk.
            max_tokens: Maximum tokens per chunk.
            method: Chunking method - "characters", "sentences", or "paragraphs".
            
        Returns:
            List of text chunks.
        """
        # Estimate character limit based on token limit
        estimated_char_limit = int(max_tokens / 0.25)  # Assuming ~0.25 tokens per char
        
        original_size = self.chunk_size
        self.chunk_size = estimated_char_limit
        
        try:
            if method == "sentences":
                chunks = self.chunk_by_sentences(text)
            elif method == "paragraphs":
                chunks = self.chunk_by_paragraphs(text)
            else:
                chunks = self.chunk_by_characters(text)
        finally:
            self.chunk_size = original_size
        
        return chunks

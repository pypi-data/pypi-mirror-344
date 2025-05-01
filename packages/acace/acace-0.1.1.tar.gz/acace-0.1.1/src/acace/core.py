"""
Core ACACE implementation that integrates all components.
"""

from typing import Optional, Dict, Any, List

from acace_text_preprocessor import preprocess_text
from acace_tokenizer import tokenize_text
from acace_token_weightor import assign_weights
from acace_compression_engine import compress_text
from acace_context_storage import ContextStorage
from acace_llm_adapter import LLMAdapter

class ACACE:
    """
    Main ACACE class that orchestrates all components for context-aware content generation.
    """
    
    def __init__(self, 
                 llm_adapter: Optional[LLMAdapter] = None,
                 context_storage: Optional[ContextStorage] = None):
        """
        Initialize ACACE with optional custom components.
        
        Args:
            llm_adapter: Custom LLM adapter instance
            context_storage: Custom context storage instance
        """
        self.llm_adapter = llm_adapter or LLMAdapter()
        self.context_storage = context_storage or ContextStorage()
        
    def process_text(self, text: str, context_id: str = None) -> Dict[str, Any]:
        """
        Process text through the ACACE pipeline.
        
        Args:
            text: The input text to process
            context_id: Optional context ID for storing/retrieving context
            
        Returns:
            Dictionary containing processed results
        """
        # Preprocess text
        cleaned_text = preprocess_text(text)
        
        # Tokenize
        tokens = tokenize_text(cleaned_text)
        
        # Assign weights
        weighted_tokens = assign_weights(tokens)
        
        # Extract token strings for compression
        token_strings = [wt["token"] for wt in weighted_tokens]
        
        # Compress
        compressed = compress_text(token_strings)
        
        # Store context if ID provided
        if context_id:
            self.context_storage.store_context(context_id, compressed)
        
        return {
            "original_text": text,
            "cleaned_text": cleaned_text,
            "tokens": tokens,
            "weighted_tokens": weighted_tokens,
            "compressed_text": compressed
        }
        
    def generate_content(self, prompt: str, context_id: str = None) -> str:
        """
        Generate content using the LLM adapter.
        
        Args:
            prompt: The input prompt
            context_id: Optional context ID for retrieving context
            
        Returns:
            Generated content
        """
        context = None
        if context_id:
            context = self.context_storage.get_context(context_id)
        
        return self.llm_adapter.generate(prompt, context) 
"""
Core engine of the Adaptive Context-Aware Content Engine (ACACE).

This module provides the main ACACE class that orchestrates the entire pipeline,
from text preprocessing to context-aware content generation.
"""

import uuid
from enum import Enum
from typing import Dict, List, Any, Optional, Union, Tuple

# Import required modules
try:
    from acace_text_preprocessor import preprocess_text
    from acace_tokenizer import tokenize_text
    from acace_token_weightor import assign_weights
except ImportError:
    # For development
    import sys
    import os
    import importlib.util

    # Add project root to path
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, project_root)

    # Import modules dynamically
    def import_module_from_path(module_name, module_path):
        init_path = os.path.join(module_path, module_name, "__init__.py")
        spec = importlib.util.spec_from_file_location(module_name, init_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module

    # Import our modules
    acace_text_preprocessor = import_module_from_path(
        "acace_text_preprocessor", 
        os.path.join(project_root, "acace_text_preprocessor")
    )
    preprocess_text = acace_text_preprocessor.preprocess_text

    acace_tokenizer = import_module_from_path(
        "acace_tokenizer", 
        os.path.join(project_root, "acace_tokenizer")
    )
    tokenize_text = acace_tokenizer.tokenize_text

    acace_token_weightor = import_module_from_path(
        "acace_token_weightor", 
        os.path.join(project_root, "acace_token_weightor")
    )
    assign_weights = acace_token_weightor.assign_weights


class CompressionLevel(Enum):
    """Compression level options for token reduction."""
    LOW = "low"        # Minimal token reduction, preserves most information
    MEDIUM = "medium"  # Balanced token reduction and information preservation
    HIGH = "high"      # Maximum token reduction, may lose some information


class ContextStrategy(Enum):
    """Context management strategy options."""
    NONE = "none"           # No context persistence
    SESSION = "session"     # Context persists within a session
    PERSISTENT = "persistent"  # Context persists across sessions


class ACACE:
    """
    Adaptive Context-Aware Content Engine main class.
    
    This class orchestrates the entire ACACE pipeline, from text preprocessing
    to context-aware content generation, optimizing token usage while
    ensuring content coherence.
    """
    
    def __init__(self,
                 compression_level: CompressionLevel = CompressionLevel.MEDIUM,
                 context_strategy: ContextStrategy = ContextStrategy.SESSION,
                 use_grammar_correction: bool = False,
                 use_style_adjustment: bool = False,
                 max_context_items: int = 100,
                 llm_adapter: str = "auto",
                 **kwargs):
        """
        Initialize the ACACE engine with configuration options.
        
        Args:
            compression_level: Level of token reduction (LOW, MEDIUM, HIGH)
            context_strategy: How context is maintained (NONE, SESSION, PERSISTENT)
            use_grammar_correction: Whether to apply grammar correction to outputs
            use_style_adjustment: Whether to adjust output style based on guidance
            max_context_items: Maximum number of context items to store
            llm_adapter: LLM provider to use (auto, openai, anthropic, etc.)
            **kwargs: Additional configuration options
        """
        self.compression_level = compression_level
        self.context_strategy = context_strategy
        self.use_grammar_correction = use_grammar_correction
        self.use_style_adjustment = use_style_adjustment
        self.max_context_items = max_context_items
        self.llm_adapter = llm_adapter
        self.options = kwargs
        
        # Initialize context storage
        self.context_store = {}
        
        # Configure compression parameters based on level
        if compression_level == CompressionLevel.LOW:
            self.token_threshold = 0.2  # Only filter tokens with very low weight
            self.target_reduction = 0.1  # Target 10% token reduction
        elif compression_level == CompressionLevel.MEDIUM:
            self.token_threshold = 0.4  # Balanced token filtering
            self.target_reduction = 0.3  # Target 30% token reduction
        else:  # HIGH
            self.token_threshold = 0.6  # Aggressive token filtering
            self.target_reduction = 0.5  # Target 50% token reduction
    
    def compress(self, text: str) -> str:
        """
        Compress the input text to reduce token count while preserving meaning.
        
        Args:
            text: The text to compress
            
        Returns:
            Compressed text with reduced token count
        """
        # Step 1: Preprocess the text
        cleaned_text = preprocess_text(text)
        
        # Step 2: Tokenize the text
        tokens = tokenize_text(cleaned_text)
        
        # Step 3: Assign weights to tokens based on semantic importance
        weighted_tokens = assign_weights(tokens, context=cleaned_text)
        
        # Step 4: Filter tokens based on weight threshold
        # Note: In the full implementation, this would use acace_token_filter
        important_tokens = [item["token"] for item in weighted_tokens 
                           if item["weight"] >= self.token_threshold]
        
        # Step 5: Reconstruct text from important tokens
        # Note: In the full implementation, this would use acace_compression_engine
        compressed_text = " ".join(important_tokens)
        
        return compressed_text
    
    def get_compression_ratio(self, original_text: str, compressed_text: str) -> float:
        """
        Calculate the compression ratio achieved.
        
        Args:
            original_text: The original text
            compressed_text: The compressed text
            
        Returns:
            Compression ratio as a float (1.0 = no compression, 0.5 = 50% reduction)
        """
        original_tokens = tokenize_text(preprocess_text(original_text))
        compressed_tokens = tokenize_text(compressed_text)
        
        if not original_tokens:
            return 1.0
        
        return 1.0 - (len(compressed_tokens) / len(original_tokens))
    
    def store_context(self, context_id: str, metadata: Dict[str, Any]) -> None:
        """
        Store context for future use.
        
        Args:
            context_id: Unique identifier for the context
            metadata: Context metadata to store
        """
        if self.context_strategy == ContextStrategy.NONE:
            return
        
        if context_id not in self.context_store:
            self.context_store[context_id] = []
        
        # Add timestamp to metadata
        metadata["timestamp"] = uuid.uuid4().hex
        
        # Add to context store
        self.context_store[context_id].append(metadata)
        
        # Limit context size
        if len(self.context_store[context_id]) > self.max_context_items:
            self.context_store[context_id] = self.context_store[context_id][-self.max_context_items:]
    
    def retrieve_context(self, context_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve stored context.
        
        Args:
            context_id: Unique identifier for the context
            
        Returns:
            List of context metadata dictionaries
        """
        if self.context_strategy == ContextStrategy.NONE:
            return []
        
        return self.context_store.get(context_id, [])
    
    def generate(self, prompt: str, context_id: Optional[str] = None) -> str:
        """
        Generate content with context awareness.
        
        Args:
            prompt: The prompt for content generation
            context_id: Optional context ID for context persistence
            
        Returns:
            Generated content
        """
        # Note: This is a simplified implementation
        # In the full version, this would use:
        # - acace_context_matcher for context retrieval
        # - acace_prompt_formatter for prompt enhancement
        # - acace_llm_adapter for LLM integration
        # - acace_output_parser for result processing
        
        # Process the prompt
        cleaned_prompt = preprocess_text(prompt)
        
        # Retrieve context if available
        context = []
        if context_id:
            context = self.retrieve_context(context_id)
        
        # In a real implementation, this would call the LLM with the enriched prompt
        # For now, we'll return a placeholder
        response = f"Generated content based on prompt: {cleaned_prompt}"
        
        if context:
            response += f"\nWith {len(context)} context items."
        
        # In a real implementation, we would:
        # 1. Extract metadata from the response
        # 2. Store it in the context
        if context_id:
            self.store_context(context_id, {
                "prompt": prompt,
                "response_summary": "Summary of response",
                "key_elements": ["element1", "element2"]
            })
        
        return response
    
    def process_document(self, document_path: str, task: str, 
                         output_format: str = "text",
                         max_length: Optional[int] = None) -> str:
        """
        Process a document with specific requirements.
        
        Args:
            document_path: Path to the document
            task: Processing task (e.g., summarize, analyze)
            output_format: Desired output format
            max_length: Maximum length of output
            
        Returns:
            Processed document content
        """
        # Note: This is a placeholder implementation
        # In the full version, this would integrate with:
        # - Document parsing modules
        # - Multi-modal context integration
        # - Format-specific output generation
        
        return f"Processed document '{document_path}' with task '{task}' in format '{output_format}'"

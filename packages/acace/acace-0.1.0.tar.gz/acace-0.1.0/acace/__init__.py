"""
Adaptive Context-Aware Content Engine (ACACE): 
Optimizing token usage and ensuring content coherence in AI-driven writing.

This is the main package that integrates all ACACE modules into a cohesive pipeline.
"""

from .engine import ACACE, CompressionLevel, ContextStrategy

__all__ = ["ACACE", "CompressionLevel", "ContextStrategy"]
__version__ = "0.1.0"

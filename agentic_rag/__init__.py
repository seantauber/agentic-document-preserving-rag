"""
Agentic Document-Preserving RAG System
"""

from .system import create_rag_system, AgenticRAGSystem
from .core.document_manager import DocumentReference, DocumentMetadata

__version__ = "0.1.0"
__all__ = ['create_rag_system', 'AgenticRAGSystem', 'DocumentReference', 'DocumentMetadata']

"""
Main system interface for the Agentic RAG system.
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging
import asyncio

from .core.coordinator import AgentCoordinator, SystemMonitor, RAGException
from .core.document_manager import DocumentManager, DocumentReference
from .core.base import Response

class AgenticRAGSystem:
    """
    Main interface for the Agentic RAG system.
    
    This class provides a high-level API for:
    - Document management
    - Query processing
    - System monitoring
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize the system.
        
        Args:
            storage_path: Path for document storage. Defaults to './rag_storage'
        """
        # Setup logging
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
        
        # Initialize components
        self.storage_path = storage_path or "./rag_storage"
        self.doc_manager = DocumentManager(self.storage_path)
        self.coordinator = AgentCoordinator(doc_manager=self.doc_manager)
        self.monitor = SystemMonitor()
        
        self.logger.info("Agentic RAG System initialized")

    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)d)'
        )

    async def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a user query.
        
        Args:
            query: The user's query string
            
        Returns:
            Dict containing:
            - response: The system's response
            - confidence: Confidence score
            - sources: List of source documents
            - metadata: Additional processing metadata
        """
        try:
            self.logger.info(f"Processing query: {query}")
            
            # Process query through coordinator
            result = await self.coordinator.process_query(query)
            
            if isinstance(result.error, Exception):
                raise result.error
                
            # Handle metadata from both dict and object attributes
            metadata = result.metadata
            if not isinstance(metadata, dict):
                metadata = {
                    "confidence": getattr(metadata, "confidence", 0.0),
                    "sources": getattr(metadata, "sources", []),
                    "completion_time": result.completion_time.isoformat()
                }
                
            return {
                "response": result.data,
                "confidence": metadata.get("confidence", 0.0),
                "sources": metadata.get("sources", []),
                "metadata": metadata
            }
            
        except Exception as e:
            self.logger.error(f"Error processing query: {str(e)}")
            raise RAGException(f"Query processing failed: {str(e)}")

    async def add_document(
        self,
        content: bytes,
        filename: str,
        content_type: str,
        tags: List[str] = None,
        metadata: Dict[str, Any] = None
    ) -> DocumentReference:
        """
        Add a new document to the system.
        
        Args:
            content: Document content as bytes
            filename: Name of the document
            content_type: MIME type of the document
            tags: Optional list of tags
            metadata: Optional additional metadata
            
        Returns:
            DocumentReference for the stored document
        """
        try:
            self.logger.info(f"Adding document: {filename}")
            
            reference = await self.doc_manager.store_document(
                content=content,
                filename=filename,
                content_type=content_type,
                tags=tags,
                additional_metadata=metadata
            )
            
            return reference
            
        except Exception as e:
            self.logger.error(f"Error adding document: {str(e)}")
            raise RAGException(f"Document addition failed: {str(e)}")

    async def get_document(self, doc_id: str) -> Optional[bytes]:
        """
        Retrieve a document's content.
        
        Args:
            doc_id: ID of the document to retrieve
            
        Returns:
            Document content as bytes if found, None otherwise
        """
        try:
            return await self.doc_manager.retrieve_document(doc_id)
        except Exception as e:
            self.logger.error(f"Error retrieving document: {str(e)}")
            raise RAGException(f"Document retrieval failed: {str(e)}")

    async def search_documents(
        self,
        tags: List[str] = None,
        metadata_filters: Dict[str, Any] = None
    ) -> List[DocumentReference]:
        """
        Search for documents based on tags and metadata.
        
        Args:
            tags: Optional list of tags to filter by
            metadata_filters: Optional metadata filters
            
        Returns:
            List of matching DocumentReferences
        """
        try:
            return await self.doc_manager.search_documents(
                tags=tags,
                metadata_filters=metadata_filters
            )
        except Exception as e:
            self.logger.error(f"Error searching documents: {str(e)}")
            raise RAGException(f"Document search failed: {str(e)}")

    def get_system_metrics(self) -> Dict[str, Any]:
        """
        Get system performance metrics.
        
        Returns:
            Dict containing various system metrics
        """
        try:
            return self.monitor.get_metrics_summary()
        except Exception as e:
            self.logger.error(f"Error getting metrics: {str(e)}")
            raise RAGException(f"Metrics retrieval failed: {str(e)}")

async def create_rag_system(
    storage_path: Optional[str] = None
) -> AgenticRAGSystem:
    """
    Factory function to create and initialize a RAG system.
    
    Args:
        storage_path: Optional custom storage path
        
    Returns:
        Initialized AgenticRAGSystem instance
    """
    system = AgenticRAGSystem(storage_path)
    return system

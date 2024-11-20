"""
Tests for the Agentic RAG system.
"""
import pytest
import asyncio
from pathlib import Path
import tempfile
import shutil

from agentic_rag.system import create_rag_system
from agentic_rag.core.document_manager import DocumentReference

@pytest.fixture(scope="function")
@pytest.mark.asyncio
async def rag_system():
    """Fixture to create a test RAG system instance"""
    # Create temporary directory for test storage
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Create system instance with temporary storage
        system = await create_rag_system(storage_path=temp_dir)
        yield system
    finally:
        # Cleanup temporary directory after tests
        shutil.rmtree(temp_dir)

@pytest.mark.asyncio
async def test_document_management(rag_system):
    """Test document addition and retrieval"""
    # Test document content
    content = b"Test document content"
    filename = "test.txt"
    content_type = "text/plain"
    tags = ["test", "document"]  # Fixed: Added comma
    metadata = {"author": "Test Author"}
    
    # Add document
    doc_ref = await rag_system.add_document(
        content=content,  # Fixed: Added comma
        filename=filename,
        content_type=content_type,
        tags=tags,
        metadata=metadata
    )
    
    # Verify document reference
    assert isinstance(doc_ref, DocumentReference)
    assert doc_ref.metadata.filename == filename
    assert doc_ref.metadata.content_type == content_type
    assert doc_ref.metadata.tags == tags
    assert doc_ref.metadata.additional_metadata == metadata
    
    # Retrieve document
    retrieved_content = await rag_system.get_document(doc_ref.doc_id)
    assert retrieved_content == content

@pytest.mark.asyncio
async def test_query_processing(rag_system):
    """Test query processing"""
    # Add test document
    content = b"""
    The quick brown fox jumps over the lazy dog.
    This is a test document for query processing.
    It contains some sample text for testing.
    """
    await rag_system.add_document(
        content=content,  # Fixed: Added comma
        filename="test.txt",
        content_type="text/plain",
        tags=["test"]
    )
    
    # Process query
    query = "What animal jumps over the dog?"
    result = await rag_system.process_query(query)
    
    # Verify result structure
    assert "response" in result
    assert "confidence" in result
    assert "sources" in result
    assert "metadata" in result
    
    # Basic validation of confidence score
    assert 0 <= result["confidence"] <= 1.0

@pytest.mark.asyncio
async def test_document_search(rag_system):
    """Test document search functionality"""
    # Add multiple test documents
    docs = [
        {
            "content": b"Test document 1",  # Fixed: Added comma
            "filename": "test1.txt",
            "tags": ["test", "doc1"],  # Fixed: Added comma
            "metadata": {"category": "A"}
        },
        {
            "content": b"Test document 2",  # Fixed: Added comma
            "filename": "test2.txt",
            "tags": ["test", "doc2"],  # Fixed: Added comma
            "metadata": {"category": "B"}
        }
    ]
    
    for doc in docs:
        await rag_system.add_document(
            content=doc["content"],  # Fixed: Added comma
            filename=doc["filename"],
            content_type="text/plain",
            tags=doc["tags"],
            metadata=doc["metadata"]
        )
    
    # Search by tags
    results = await rag_system.search_documents(tags=["test"])
    assert len(results) == 2
    
    # Search by metadata
    results = await rag_system.search_documents(
        metadata_filters={"category": "A"}
    )
    assert len(results) == 1
    assert results[0].metadata.filename == "test1.txt"

@pytest.mark.asyncio
async def test_system_metrics(rag_system):
    """Test system metrics collection"""
    # Perform some operations to generate metrics
    await rag_system.add_document(
        content=b"Test content",  # Fixed: Added comma
        filename="test.txt",
        content_type="text/plain"
    )
    
    await rag_system.process_query("Test query")
    
    # Get metrics
    metrics = rag_system.get_system_metrics()
    
    # Verify metrics structure
    assert isinstance(metrics, dict)
    assert "avg_query_latency" in metrics

if __name__ == "__main__":
    pytest.main([__file__])

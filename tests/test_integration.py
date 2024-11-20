"""Integration tests for the Agentic RAG system using real documents and LLM."""
import pytest
import asyncio
from pathlib import Path
import tempfile
import shutil
import os
import inspect

from agentic_rag.system import create_rag_system, AgenticRAGSystem
from agentic_rag.core.document_manager import DocumentReference

# Test documents with meaningful content
DOCUMENTS = {
    "quantum_computing.txt": """
Quantum Computing Fundamentals

Quantum computing leverages quantum mechanical phenomena like superposition and entanglement 
to perform computations. Unlike classical bits that are either 0 or 1, quantum bits (qubits) 
can exist in multiple states simultaneously due to superposition.

Key concepts:
1. Superposition: Qubits can exist in multiple states at once
2. Entanglement: Quantum states of particles become correlated
3. Quantum Gates: Manipulate qubits to perform computations

Current challenges include maintaining qubit coherence and minimizing errors due to 
decoherence and noise. Companies like IBM, Google, and D-Wave are leading quantum 
computer development.
""".encode('ascii'),

    "climate_change.txt": """
Understanding Climate Change

Climate change refers to long-term shifts in global weather patterns and average temperatures. 
The primary driver of recent climate change is human activity, particularly the emission of 
greenhouse gases like CO2 and methane.

Key impacts include:
- Rising sea levels due to melting ice caps
- Increased frequency of extreme weather events
- Disruption of ecosystems and biodiversity loss
- Threats to food security and water resources

The Paris Agreement aims to limit global temperature rise to well below 2C above 
pre-industrial levels. This requires significant reduction in greenhouse gas emissions 
and transition to renewable energy sources.
""".encode('ascii'),

    "artificial_intelligence.txt": """
Modern Artificial Intelligence

AI systems use machine learning algorithms to analyze data and make predictions or decisions. 
Deep learning, a subset of machine learning, uses neural networks with multiple layers to 
process complex patterns.

Applications include:
- Natural Language Processing (NLP)
- Computer Vision
- Autonomous Systems
- Healthcare Diagnostics

Recent developments like large language models (LLMs) have shown remarkable capabilities in 
understanding and generating human-like text. However, challenges remain around bias, 
transparency, and ethical considerations.
""".encode('ascii')
}

def debug_object(obj, name="object"):
    """Helper function to debug object attributes and methods"""
    print(f"\n=== Debugging {name} ===")
    print(f"Type: {type(obj)}")
    print(f"Dir: {dir(obj)}")
    if hasattr(obj, '__class__'):
        print(f"Class methods: {inspect.getmembers(obj.__class__, predicate=inspect.isfunction)}")
    print(f"Is async generator? {inspect.isasyncgen(obj)}")
    print(f"Is coroutine? {inspect.iscoroutine(obj)}")
    print(f"Is async with attrs? {hasattr(obj, '__aenter__') and hasattr(obj, '__aexit__')}")
    print("=" * 50)

@pytest.fixture(scope="function")
async def test_system():
    """Create a test RAG system with temporary storage"""
    print("\n=== Starting test_system fixture ===")
    
    # Create temporary directory for test storage
    temp_dir = tempfile.mkdtemp()
    print(f"Created temp directory: {temp_dir}")
    
    # Create necessary subdirectories
    docs_dir = Path(temp_dir) / "documents"
    refs_dir = Path(temp_dir) / "references"
    docs_dir.mkdir(parents=True, exist_ok=True)
    refs_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created subdirectories: {docs_dir}, {refs_dir}")
    
    try:
        print("Creating RAG system...")
        system = await create_rag_system(storage_path=temp_dir)
        print("RAG system created")
        debug_object(system, "system in fixture before yield")
        
        yield system
        
    finally:
        print(f"Cleaning up temp directory: {temp_dir}")
        shutil.rmtree(temp_dir)

@pytest.mark.asyncio
async def test_quantum_computing_queries(test_system):
    """Test queries about quantum computing"""
    print("\n=== Starting quantum computing queries test ===")
    
    # Get the actual system instance by awaiting the fixture
    system = await test_system.__anext__()
    debug_object(system, "system after await in quantum test")
    
    # First load the test documents
    print("\nLoading quantum computing document...")
    doc_ref = await system.add_document(
        content=DOCUMENTS["quantum_computing.txt"],
        filename="quantum_computing.txt",
        content_type="text/plain",
        tags=["test", "quantum"],
        metadata={"domain": "quantum"}
    )
    print(f"Added document ref: {doc_ref}")
    
    queries = [
        "What is the difference between classical bits and qubits?",
        "What are the main challenges in quantum computing?"
    ]
    
    for query in queries:
        print(f"\nProcessing query: {query}")
        result = await system.process_query(query)
        print(f"Query result: {result}")
        
        assert "response" in result
        assert "confidence" in result
        assert "sources" in result
        assert any("quantum" in source for source in result["sources"])

@pytest.mark.asyncio
async def test_cross_domain_query(test_system):
    """Test queries that should combine information from multiple domains"""
    print("\n=== Starting cross domain query test ===")
    
    # Get the actual system instance
    system = await test_system.__anext__()
    debug_object(system, "system after await in cross domain test")
    
    # Load relevant documents
    for filename in ["quantum_computing.txt", "climate_change.txt"]:
        await system.add_document(
            content=DOCUMENTS[filename],
            filename=filename,
            content_type="text/plain",
            tags=["test", filename.split('_')[0]],
            metadata={"domain": filename.split('_')[0]}
        )
    
    query = "How might quantum computing help address climate change challenges?"
    result = await system.process_query(query)
    print(f"Query result: {result}")
    
    sources = [str(source) for source in result["sources"]]
    assert any("quantum" in source for source in sources)
    assert any("climate" in source for source in sources)

@pytest.mark.asyncio
async def test_specific_domain_search(test_system):
    """Test document search functionality with domain filtering"""
    print("\n=== Starting specific domain search test ===")
    
    # Get the actual system instance
    system = await test_system.__anext__()
    debug_object(system, "system after await in domain search test")
    
    # Load AI document
    await system.add_document(
        content=DOCUMENTS["artificial_intelligence.txt"],
        filename="artificial_intelligence.txt",
        content_type="text/plain",
        tags=["test", "artificial"],
        metadata={"domain": "artificial"}
    )
    
    ai_docs = await system.search_documents(
        tags=["artificial"],
        metadata_filters={"domain": "artificial"}
    )
    print(f"Search results: {ai_docs}")
    
    assert len(ai_docs) == 1
    assert "artificial_intelligence.txt" in ai_docs[0].metadata.filename

@pytest.mark.asyncio
async def test_complex_reasoning_query(test_system):
    """Test system's ability to handle complex reasoning tasks"""
    print("\n=== Starting complex reasoning query test ===")
    
    # Get the actual system instance
    system = await test_system.__anext__()
    debug_object(system, "system after await in complex reasoning test")
    
    # Load relevant documents
    for filename in ["quantum_computing.txt", "artificial_intelligence.txt"]:
        await system.add_document(
            content=DOCUMENTS[filename],
            filename=filename,
            content_type="text/plain",
            tags=["test", filename.split('_')[0]],
            metadata={"domain": filename.split('_')[0]}
        )
    
    query = """Compare and contrast the challenges faced in quantum computing 
and artificial intelligence development. What are some common themes?"""
    
    result = await system.process_query(query)
    print(f"Query result: {result}")
    
    sources = [str(source) for source in result["sources"]]
    assert any("quantum" in source for source in sources)
    assert any("artificial" in source for source in sources)
    assert result["confidence"] >= 0.6

if __name__ == "__main__":
    pytest.main([__file__])

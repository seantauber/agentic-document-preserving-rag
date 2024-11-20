# Agentic Document-Preserving RAG System

An advanced implementation of a Retrieval-Augmented Generation (RAG) system that combines autonomous agents with robust document preservation. Unlike traditional RAG systems that focus solely on retrieval and generation, this system introduces an agent-based architecture that maintains document integrity while enabling sophisticated information processing.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)

## System Architecture

### Core Components

#### 1. Agent Foundation
The system is built on a robust agent foundation that provides essential capabilities:

```python
class BaseAgent:
    def __init__(self):
        self.state = AgentState()
        self.knowledge = KnowledgeBase()
        self.capabilities = set()
```

- **State Management**: Tracks agent activity and current tasks
- **Knowledge Base**: Maintains agent-specific knowledge and learning
- **Task Planning**: Creates execution plans for given tasks
- **Communication**: Handles inter-agent messaging
- **Experience Tracking**: Records and learns from task execution

#### 2. Specialized Agents

**QueryAnalysisAgent**
- Analyzes and decomposes user queries
- Identifies intents and domains
- Creates subtasks
- Performs context analysis
- Calculates confidence scores

**DocumentAgent**
- Manages document access and analysis
- Preserves content integrity
- Identifies relationships
- Extracts context
- Handles metadata

**SynthesisAgent**
- Integrates information from multiple sources
- Generates coherent responses
- Maintains source attribution
- Ensures context awareness
- Provides confidence scoring

#### 3. Document Management

```python
class DocumentManager:
    async def store_document(
        self,
        content: bytes,
        filename: str,
        content_type: str,
        tags: List[str] = None,
        additional_metadata: Dict[str, Any] = None
    ) -> DocumentReference:
```

- Original document preservation
- Robust metadata tracking
- Efficient storage and retrieval
- Strong reference management
- Checksum verification

#### 4. Coordination System

```python
class AgentCoordinator:
    async def process_query(self, query: str) -> Result:
        # 1. Query Analysis
        query_analysis = await self.query_agent.analyze_query(query)
        # 2. Document Retrieval
        relevant_docs = await self._find_relevant_documents(query_analysis)
        # 3. Information Processing
        results = await self._execute_plan(plan, context)
        # 4. Response Generation
        return await self.synthesis_agent.synthesize(query_analysis, results)
```

- Task distribution
- Resource allocation
- Progress monitoring
- Error handling
- Performance optimization

### Comparison with Other RAG Systems

| Feature | This Implementation | Traditional RAG | LangChain RAG |
|---------|-------------------|----------------|---------------|
| Document Preservation | ✅ Complete | ❌ Limited | ⚠️ Partial |
| Agent Intelligence | ✅ Advanced | ❌ Basic | ⚠️ Framework-dependent |
| Architecture | ✅ Agent-based | ❌ Pipeline | ✅ Chain-based |
| Extensibility | ✅ High | ⚠️ Medium | ✅ High |
| Performance Monitoring | ✅ Built-in | ❌ Limited | ⚠️ External |

## Quick Start

### Installation

```bash
# Using Poetry (Recommended)
curl -sSL https://install.python-poetry.org | python3 -
git clone https://github.com/yourusername/agentic-rag.git
cd agentic-rag
poetry install
poetry shell

# Using Pip
git clone https://github.com/yourusername/agentic-rag.git
cd agentic-rag
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Basic Usage

```python
import asyncio
from agentic_rag.system import create_rag_system

async def main():
    # Create system instance
    system = await create_rag_system()
    
    # Add a document
    doc_ref = await system.add_document(
        content=content,
        filename="example.txt",
        content_type="text/plain",
        tags=["research"],
        metadata={"domain": "research"}
    )
    
    # Process a query
    result = await system.process_query(
        "What are the key findings in the research paper?"
    )
    
    print(f"Response: {result['response']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Sources: {result['sources']}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Advanced Usage

### Document Management

```python
# Add document with rich metadata
doc_ref = await system.add_document(
    content=content,
    filename="research_paper.pdf",
    content_type="application/pdf",
    tags=["research", "ai", "important"],
    metadata={
        "author": "John Doe",
        "date": "2024-01-01",
        "domain": "artificial-intelligence",
        "institution": "Research Lab"
    }
)

# Search documents
results = await system.search_documents(
    tags=["research", "important"],
    metadata_filters={
        "domain": "artificial-intelligence",
        "author": "John Doe"
    }
)
```

### System Monitoring

```python
# Get performance metrics
metrics = system.get_system_metrics()
print(f"Average query latency: {metrics['avg_query_latency']}s")
print(f"Document processing rate: {metrics['doc_processing_rate']}/s")
print(f"Memory usage: {metrics['memory_usage_mb']}MB")
```

## Cache Management

The system maintains a structured cache in the `rag_storage` directory:

```
rag_storage/
├── documents/     # Original documents
└── references/    # Metadata and references
```

Cache management commands:
```bash
# Clear cache (Unix)
rm -rf ./rag_storage

# Clear cache (Windows)
rmdir /s /q rag_storage
```

## Testing

```bash
# Run all tests
poetry run pytest tests/

# Run with coverage
poetry run pytest --cov=agentic_rag tests/

# Run specific test file
poetry run pytest tests/test_system.py
```

## Project Structure

```
agentic_rag/
├── core/
│   ├── base.py          # Base agent implementation
│   ├── agents.py        # Specialized agents
│   ├── coordinator.py   # Agent coordination
│   └── document_manager.py  # Document management
├── system.py            # Main system interface
└── __init__.py
examples/
└── basic_usage.py       # Usage examples
tests/
├── test_system.py       # System tests
└── test_integration.py  # Integration tests
```

## Dependencies

```toml
[tool.poetry.dependencies]
python = "^3.12"
asyncio = "^3.7.4"
typing = "^3.7.4"
dataclasses = "^0.6"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
pytest-asyncio = "^0.20.0"
pytest-cov = "^4.1.0"
```

## Extension Points

1. **Agent Capabilities**
   - Enhanced learning mechanisms
   - Specialized document analysis
   - Advanced query understanding
   - Dynamic resource allocation

2. **System Features**
   - Persistent storage backends
   - Advanced caching strategies
   - Real-time updates
   - Multi-user support

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

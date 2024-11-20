# Agentic Document-Preserving RAG System

An intelligent RAG (Retrieval-Augmented Generation) system where autonomous agents collaborate to analyze, retrieve, and synthesize information while preserving original document integrity.

## Features

- **Document Preservation**: Maintains complete access to original documents while enabling intelligent processing
- **Autonomous Agents**: Specialized agents for query analysis, document processing, and information synthesis
- **Intelligent Coordination**: Sophisticated agent coordination for complex information needs
- **Flexible Document Management**: Robust storage and retrieval system with metadata support
- **Performance Monitoring**: Built-in system monitoring and metrics collection

## Installation

### Using Poetry (Recommended)

The project uses Poetry for dependency management. To get started:

1. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Clone and set up the project:
```bash
# Clone the repository
git clone https://github.com/yourusername/agentic-rag.git
cd agentic-rag

# Install dependencies using Poetry
poetry install

# Activate the Poetry virtual environment
poetry shell
```

### Alternative: Pip Installation

If you prefer using pip:

```bash
# Clone the repository
git clone https://github.com/yourusername/agentic-rag.git
cd agentic-rag

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Cache Management

The system uses a `rag_storage` directory to cache documents and their references. This cache needs to be managed properly:

- **Location**: The cache is stored in the `./rag_storage` directory relative to your working directory
- **Structure**:
  ```
  rag_storage/
  ├── documents/     # Stores original documents
  └── references/    # Stores document metadata and references
  ```
- **Clearing the Cache**: 
  ```bash
  # Remove the entire cache directory
  rm -rf ./rag_storage
  
  # On Windows:
  rmdir /s /q rag_storage
  ```
- **When to Clear**: Clear the cache when:
  - Testing different document sets
  - Troubleshooting document processing
  - Starting fresh with new documents
  - After making changes to document processing logic

## Running Examples

### Basic Usage Example

The `examples/basic_usage.py` demonstrates core functionality:

```bash
# Clear cache and run with Poetry
rm -rf ./rag_storage && poetry run python examples/basic_usage.py

# Without Poetry (if using regular pip installation)
rm -rf ./rag_storage && python examples/basic_usage.py
```

This example:
1. Clears any existing cache
2. Creates a new RAG system instance
3. Adds a sample document
4. Processes various queries
5. Demonstrates document search
6. Shows system metrics

## Usage

### Basic Usage

```python
import asyncio
from agentic_rag.system import create_rag_system

async def main():
    # Create system instance
    system = await create_rag_system()
    
    # Add a document with domain metadata
    doc_ref = await system.add_document(
        content=content,
        filename="example.txt",
        content_type="text/plain",
        tags=["research", "paper"],
        metadata={
            "author": "John Doe",
            "date": "2024-01-01",
            "domain": "research"  # Important for domain attribution
        }
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

### Document Management

```python
# Add a document with metadata
doc_ref = await system.add_document(
    content=content,
    filename="example.txt",
    content_type="text/plain",
    tags=["category1", "important"],
    metadata={"author": "John Doe", "date": "2024-01-01"}
)

# Retrieve document content
content = await system.get_document(doc_ref.doc_id)

# Search documents
results = await system.search_documents(
    tags=["important"],
    metadata_filters={"author": "John Doe"}
)
```

### System Monitoring

```python
# Get system metrics
metrics = system.get_system_metrics()
print(f"Average query latency: {metrics['avg_query_latency']}s")
```

## Testing

The system includes a comprehensive test suite:

```bash
# Run all tests with Poetry
poetry run pytest tests/

# Run specific test file
poetry run pytest tests/test_system.py

# Run with coverage
poetry run pytest --cov=agentic_rag tests/

# Without Poetry:
pytest tests/
pytest tests/test_system.py
pytest --cov=agentic_rag tests/
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
└── basic_usage.py       # Basic usage example
tests/
├── test_system.py       # System tests
└── __init__.py
```

## Dependencies

The project uses the following main dependencies (managed by Poetry):

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
   - Learning from interactions
   - Specialized document analysis
   - Advanced query understanding
   - Dynamic resource allocation

2. **System Features**
   - Persistent storage
   - Advanced caching
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

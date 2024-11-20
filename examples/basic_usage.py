"""
Basic usage example of the Agentic RAG system.
"""
import asyncio
import logging
from pathlib import Path

from agentic_rag.system import create_rag_system

# Sample document content
SAMPLE_DOCUMENT = """
Title: Climate Change Impact on Marine Ecosystems

Abstract:
This research paper examines the effects of climate change on marine ecosystems 
between 2010 and 2023. Our findings indicate significant changes in ocean 
temperature, pH levels, and marine biodiversity.

Key Findings:
1. Ocean temperatures have increased by an average of 0.5C in the studied regions
2. Coral reef systems show 15% decline in biodiversity
3. Marine species migration patterns have shifted northward by 2-3 degrees latitude
4. Ocean acidification has increased by 0.1 pH units

Conclusions:
The study demonstrates clear evidence of climate change impacts on marine 
ecosystems, with particularly concerning effects on coral reefs and marine species 
distribution. Immediate action is needed to mitigate these effects.
""".encode('utf-8')

async def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Create system instance
        system = await create_rag_system()
        
        # Add sample document
        doc_ref = await system.add_document(
            content=SAMPLE_DOCUMENT,
            filename="climate_research.txt",
            content_type="text/plain",
            tags=["research", "climate", "marine"],
            metadata={
                "author": "Marine Research Team",
                "year": 2023,
                "type": "research paper",
                "domain": "climate"  # Added domain to metadata
            }
        )
        print(f"\nDocument added successfully: {doc_ref.doc_id}")
        
        # Example queries to demonstrate system capabilities
        queries = [
            "What are the main findings about ocean temperature changes?",
            "How has marine biodiversity been affected?",
            "What are the key conclusions of the study?",
            "What is the impact on coral reefs?"
        ]
        
        print("\nProcessing queries...")
        for query in queries:
            print(f"\nQuery: {query}")
            result = await system.process_query(query)
            
            print(f"Response: {result['response']}")
            print(f"Confidence: {result['confidence']:.2f}")
            print("Sources:", [str(s) for s in result['sources']])
            
        # Demonstrate document search
        print("\nSearching documents with tag 'climate'...")
        search_results = await system.search_documents(tags=["climate"])
        print(f"Found {len(search_results)} documents")
        
        # Get system metrics
        metrics = system.get_system_metrics()
        print("\nSystem Metrics:")
        for metric, value in metrics.items():
            print(f"{metric}: {value}")

    except Exception as e:
        logging.error(f"Error in example: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())

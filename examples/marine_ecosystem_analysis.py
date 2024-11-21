"""
Advanced usage example of the Agentic RAG system demonstrating cross-document analysis
of marine ecosystem documents with reference resolution and complex querying.
This example also highlights current limitations and areas for improvement in the RAG system.
"""
import asyncio
import logging
from pathlib import Path
import json
import shutil

from agentic_rag.system import create_rag_system

# Load the actual document contents from files
async def load_document(filepath: str) -> bytes:
    with open(filepath, 'rb') as f:
        return f.read()

async def main():
    # Configure logging with more detailed format
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('marine_ecosystem_analysis.log')
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Starting marine ecosystem analysis")
    
    # Clear existing storage
    storage_path = "rag_storage/marine_analysis"
    if Path(storage_path).exists():
        shutil.rmtree(storage_path)
        logger.info(f"Cleared existing storage at {storage_path}")
    
    try:
        # Create system instance with custom storage
        system = await create_rag_system(storage_path=storage_path)
        
        # Document metadata definitions
        documents = [
            {
                "filepath": "test_documents/coral_reef_study.txt",
                "filename": "coral_reef_study.txt",
                "tags": ["marine-biology", "climate-impact", "coral"],
                "metadata": {
                    "domain": "coral",
                    "reference": "CORAL_TEMP_REF_001"
                }
            },
            {
                "filepath": "test_documents/marine_biodiversity_assessment.txt",
                "filename": "marine_biodiversity_assessment.txt",
                "tags": ["marine-biology", "species-diversity", "biodiversity"],
                "metadata": {
                    "domain": "biodiversity",
                    "reference": "BIO_TEMP_REF_002"
                }
            },
            {
                "filepath": "test_documents/climate_impact_synthesis.txt",
                "filename": "climate_impact_synthesis.txt",
                "tags": ["climate-impact", "synthesis", "marine-ecosystems"],
                "metadata": {
                    "domain": "climate",
                    "references": ["CORAL_TEMP_REF_001", "BIO_TEMP_REF_002", "CLIMATE_REF_003"]
                }
            }
        ]
        
        # Load and add documents
        logger.info("Loading documents into the system")
        doc_refs = []
        for doc in documents:
            content = await load_document(doc["filepath"])
            doc_ref = await system.add_document(
                content=content,
                filename=doc["filename"],
                content_type="text/plain",
                tags=doc["tags"],
                metadata=doc["metadata"]
            )
            doc_refs.append(doc_ref)
            logger.info(f"Added document: {doc['filename']}")
        
        print("\n=== Document Analysis and Query Testing ===")
        print("Testing various query types to evaluate system capabilities and limitations")
        
        # 1. Basic Factual Queries
        print("\n1. Basic Factual Queries:")
        factual_queries = [
            "What are the main section headings in the coral reef study?",
            "What is the unique reference identifier for the coral reef study?",
            "What is the measured rate of ocean temperature increase?"
        ]
        
        for query in factual_queries:
            result = await system.process_query(query)
            print(f"\nQ: {query}")
            print(f"A: {result['response']}")
            print(f"Sources: {[str(s) for s in result['sources']]}")
        
        # 2. Cross-Document Data Integration
        print("\n2. Cross-Document Data Integration:")
        integration_query = """
        Compare the following across all documents:
        1. Temperature increase rate from coral study
        2. Species migration rate from biodiversity assessment
        3. How these rates are referenced in the synthesis
        Provide specific numbers and cross-references.
        """
        
        result = await system.process_query(integration_query)
        print(f"\nQ: {integration_query}")
        print(f"A: {result['response']}")
        print(f"Sources: {[str(s) for s in result['sources']]}")
        
        # 3. Analytical Reasoning
        print("\n3. Analytical Reasoning:")
        analysis_query = """
        Based on the temperature thresholds mentioned:
        - At what temperature does coral bleaching occur?
        - At what temperature does biodiversity loss accelerate?
        - What is the time gap between these thresholds being reached?
        Use specific data points to support the analysis.
        """
        
        result = await system.process_query(analysis_query)
        print(f"\nQ: {analysis_query}")
        print(f"A: {result['response']}")
        print(f"Sources: {[str(s) for s in result['sources']]}")
        
        # 4. Reference Resolution
        print("\n4. Reference Resolution:")
        ref_query = """
        For each reference to CORAL_TEMP_REF_001 in the synthesis document:
        1. What specific data point is being referenced?
        2. In what context is it used?
        3. How does it connect to other findings?
        """
        
        result = await system.process_query(ref_query)
        print(f"\nQ: {ref_query}")
        print(f"A: {result['response']}")
        print(f"Sources: {[str(s) for s in result['sources']]}")
        
        # 5. Document Search Verification
        print("\n5. Document Search Capabilities:")
        
        # Search by tags
        print("\nDocument tag search results:")
        for tag in ["marine-biology", "synthesis", "climate-impact"]:
            docs = await system.search_documents(tags=[tag])
            print(f"\nDocuments tagged with '{tag}':")
            for doc in docs:
                print(f"- {doc.metadata.filename}")
        
        # 6. System Performance Metrics
        print("\n6. System Metrics:")
        metrics = system.get_system_metrics()
        print(json.dumps(metrics, indent=2))

    except FileNotFoundError as e:
        logger.error(f"Document file not found: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error in analysis: {str(e)}")
        raise
    finally:
        logger.info("Analysis complete")

if __name__ == "__main__":
    asyncio.run(main())

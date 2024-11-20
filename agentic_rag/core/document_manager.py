"""
Document management system for storing and accessing documents.
"""
from dataclasses import dataclass
from typing import Dict, List, Any, Optional, BinaryIO
from datetime import datetime
import hashlib
import json
import os
import logging
from pathlib import Path

@dataclass
class DocumentMetadata:
    """Metadata for a stored document"""
    doc_id: str
    filename: str
    content_type: str
    size: int
    created_at: datetime
    updated_at: datetime
    checksum: str
    tags: List[str]
    additional_metadata: Dict[str, Any]

@dataclass
class DocumentReference:
    """Reference to a stored document"""
    doc_id: str
    location: str
    metadata: DocumentMetadata

class DocumentStore:
    """
    Handles physical storage of documents.
    """
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)

    async def store(self, content: bytes, filename: str) -> str:
        """Store document content and return document ID"""
        try:
            # Generate document ID
            doc_id = self._generate_doc_id(content)
            
            # Create document directory
            doc_dir = self.base_path / doc_id
            doc_dir.mkdir(exist_ok=True)
            
            # Store original content
            content_path = doc_dir / "original"
            with open(content_path, "wb") as f:
                f.write(content)
            
            return doc_id
                
        except Exception as e:
            self.logger.error(f"Error storing document: {str(e)}")
            raise

    async def retrieve(self, doc_id: str) -> Optional[bytes]:
        """Retrieve document content"""
        try:
            content_path = self.base_path / doc_id / "original"
            if not content_path.exists():
                return None
                
            with open(content_path, "rb") as f:
                return f.read()
                
        except Exception as e:
            self.logger.error(f"Error retrieving document: {str(e)}")
            raise

    def _generate_doc_id(self, content: bytes) -> str:
        """Generate unique document ID"""
        timestamp = datetime.now().isoformat()
        content_hash = hashlib.sha256(content).hexdigest()[:16]
        return f"{timestamp}_{content_hash}"

class ReferenceManager:
    """
    Manages document references and metadata.
    """
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        # Store the documents path for checksum calculation
        self.docs_path = Path(str(self.base_path).replace("/references", "/documents"))
        self.logger = logging.getLogger(__name__)

    async def create_reference(
        self,
        doc_id: str,
        filename: str,
        content_type: str,
        size: int,
        tags: List[str] = None,
        additional_metadata: Dict[str, Any] = None
    ) -> DocumentReference:
        """Create a new document reference"""
        try:
            metadata = DocumentMetadata(
                doc_id=doc_id,
                filename=filename,
                content_type=content_type,
                size=size,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                checksum=self._calculate_checksum(doc_id),
                tags=tags or [],
                additional_metadata=additional_metadata or {}
            )
            
            # Store metadata
            await self._store_metadata(metadata)
            
            return DocumentReference(
                doc_id=doc_id,
                location=str(self.base_path / doc_id),
                metadata=metadata
            )
                
        except Exception as e:
            self.logger.error(f"Error creating reference: {str(e)}")
            raise

    async def get_reference(self, doc_id: str) -> Optional[DocumentReference]:
        """Retrieve document reference"""
        try:
            metadata = await self._load_metadata(doc_id)
            if not metadata:
                return None
                
            return DocumentReference(
                doc_id=doc_id,
                location=str(self.base_path / doc_id),
                metadata=metadata
            )
                
        except Exception as e:
            self.logger.error(f"Error retrieving reference: {str(e)}")
            raise

    async def _store_metadata(self, metadata: DocumentMetadata) -> None:
        """Store document metadata"""
        # Create metadata directory if it doesn't exist
        metadata_dir = self.base_path / metadata.doc_id
        metadata_dir.mkdir(parents=True, exist_ok=True)
        
        metadata_path = metadata_dir / "metadata.json"
        metadata_dict = {
            "doc_id": metadata.doc_id,
            "filename": metadata.filename,
            "content_type": metadata.content_type,
            "size": metadata.size,
            "created_at": metadata.created_at.isoformat(),
            "updated_at": metadata.updated_at.isoformat(),
            "checksum": metadata.checksum,
            "tags": metadata.tags,
            "additional_metadata": metadata.additional_metadata
        }
        
        with open(metadata_path, "w") as f:
            json.dump(metadata_dict, f, indent=2)

    async def _load_metadata(self, doc_id: str) -> Optional[DocumentMetadata]:
        """Load document metadata"""
        metadata_path = self.base_path / doc_id / "metadata.json"
        if not metadata_path.exists():
            return None
                
        with open(metadata_path, "r") as f:
            metadata_dict = json.load(f)
                
        return DocumentMetadata(
            doc_id=metadata_dict["doc_id"],
            filename=metadata_dict["filename"],
            content_type=metadata_dict["content_type"],
            size=metadata_dict["size"],
            created_at=datetime.fromisoformat(metadata_dict["created_at"]),
            updated_at=datetime.fromisoformat(metadata_dict["updated_at"]),
            checksum=metadata_dict["checksum"],
            tags=metadata_dict["tags"],
            additional_metadata=metadata_dict["additional_metadata"]
        )

    def _calculate_checksum(self, doc_id: str) -> str:
        """Calculate document checksum"""
        # Look for the original file in the documents directory
        content_path = self.docs_path / doc_id / "original"
        if not content_path.exists():
            raise FileNotFoundError(f"Document content not found at {content_path}")
                
        with open(content_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

class DocumentManager:
    """
    Main interface for document management.
    """
    def __init__(self, storage_path: str):
        self.storage_path = Path(storage_path)
        self.doc_store = DocumentStore(str(self.storage_path / "documents"))
        self.ref_manager = ReferenceManager(str(self.storage_path / "references"))
        self.logger = logging.getLogger(__name__)

    async def store_document(
        self,
        content: bytes,
        filename: str,
        content_type: str,
        tags: List[str] = None,
        additional_metadata: Dict[str, Any] = None
    ) -> DocumentReference:
        """Store a document and create its reference"""
        try:
            # Store document content
            doc_id = await self.doc_store.store(content, filename)
                
            # Create document reference
            reference = await self.ref_manager.create_reference(
                doc_id=doc_id,
                filename=filename,
                content_type=content_type,
                size=len(content),
                tags=tags,
                additional_metadata=additional_metadata
            )
                
            return reference
                
        except Exception as e:
            self.logger.error(f"Error storing document: {str(e)}")
            raise

    async def retrieve_document(self, doc_id: str) -> Optional[bytes]:
        """Retrieve document content"""
        return await self.doc_store.retrieve(doc_id)

    async def get_document_reference(self, doc_id: str) -> Optional[DocumentReference]:
        """Get document reference"""
        return await self.ref_manager.get_reference(doc_id)

    async def search_documents(
        self,
        tags: List[str] = None,
        metadata_filters: Dict[str, Any] = None
    ) -> List[DocumentReference]:
        """Search for documents based on tags and metadata"""
        matching_refs = []

        for reference_dir in self.ref_manager.base_path.iterdir():
            if not reference_dir.is_dir():
                continue

            metadata_path = reference_dir / "metadata.json"
            if not metadata_path.exists():
                continue

            with open(metadata_path, "r") as f:
                metadata_dict = json.load(f)

            # Check tags
            if tags:
                if not set(tags).issubset(set(metadata_dict.get("tags", []))):
                    continue

            # Check metadata_filters against additional_metadata
            if metadata_filters:
                additional_metadata = metadata_dict.get("additional_metadata", {})
                if not all(additional_metadata.get(k) == v for k, v in metadata_filters.items()):
                    continue

            # Create DocumentMetadata instance
            metadata = DocumentMetadata(
                doc_id=metadata_dict["doc_id"],
                filename=metadata_dict["filename"],
                content_type=metadata_dict["content_type"],
                size=metadata_dict["size"],
                created_at=datetime.fromisoformat(metadata_dict["created_at"]),
                updated_at=datetime.fromisoformat(metadata_dict["updated_at"]),
                checksum=metadata_dict["checksum"],
                tags=metadata_dict["tags"],
                additional_metadata=metadata_dict["additional_metadata"]
            )

            # Create DocumentReference
            doc_ref = DocumentReference(
                doc_id=metadata_dict["doc_id"],
                location=str(reference_dir),
                metadata=metadata
            )
            matching_refs.append(doc_ref)

        return matching_refs

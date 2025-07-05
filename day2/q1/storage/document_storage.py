"""
Document Storage Service

This handles saving and loading documents to/from JSON files.
Think of it as a digital filing cabinet that can:
- Store documents
- Retrieve documents  
- Search through documents
- List all documents

Why use JSON?
- Human readable (you can open the file and read it)
- Easy to work with in Python
- Standard format for data exchange
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime

from models.document import Document
from config import STORAGE_DIR, DOCUMENTS_FILE

class DocumentStorage:
    """
    Document Storage Service
    
    This class handles all document storage operations.
    Think of it as a librarian who manages all the books (documents).
    """
    
    def __init__(self):
        """Initialize the storage service"""
        self.storage_dir = Path(STORAGE_DIR)
        self.documents_file = Path(DOCUMENTS_FILE)
        
        # Create storage directory if it doesn't exist
        self.storage_dir.mkdir(exist_ok=True)
        
        # Create documents file if it doesn't exist
        if not self.documents_file.exists():
            self._create_empty_storage()
    
    def _create_empty_storage(self):
        """Create an empty documents storage file"""
        empty_storage = {
            "documents": [],
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "total_documents": 0
            }
        }
        self._save_storage(empty_storage)
        print(f"📁 Created empty storage file: {self.documents_file}")
    
    def _load_storage(self) -> Dict[str, Any]:
        """Load the entire storage file"""
        try:
            with open(self.documents_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Storage file not found, creating new one")
            self._create_empty_storage()
            return self._load_storage()
        except json.JSONDecodeError as e:
            print(f"❌ Error reading storage file: {e}")
            # Backup corrupted file and create new one
            backup_file = self.documents_file.with_suffix('.backup')
            self.documents_file.rename(backup_file)
            print(f"📋 Backed up corrupted file to: {backup_file}")
            self._create_empty_storage()
            return self._load_storage()
    
    def _save_storage(self, storage_data: Dict[str, Any]):
        """Save the entire storage file"""
        try:
            # Update metadata
            storage_data["metadata"]["last_updated"] = datetime.now().isoformat()
            storage_data["metadata"]["total_documents"] = len(storage_data["documents"])
            
            with open(self.documents_file, 'w', encoding='utf-8') as f:
                json.dump(storage_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving storage file: {e}")
            raise
    
    def add_document(self, document: Document) -> bool:
        """
        Add a new document to storage
        
        Args:
            document: Document to add
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            storage_data = self._load_storage()
            
            # Check if document with same ID already exists
            existing_ids = [doc["id"] for doc in storage_data["documents"]]
            if document.id in existing_ids:
                print(f"⚠️ Document with ID {document.id} already exists")
                return False
            
            # Add document
            storage_data["documents"].append(document.to_dict())
            self._save_storage(storage_data)
            
            print(f"✅ Added document: {document.title}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding document: {e}")
            return False
    
    def get_document(self, document_id: str) -> Optional[Document]:
        """
        Retrieve a document by ID
        
        Args:
            document_id: ID of the document to retrieve
            
        Returns:
            Document if found, None otherwise
        """
        try:
            storage_data = self._load_storage()
            
            for doc_data in storage_data["documents"]:
                if doc_data["id"] == document_id:
                    return Document.from_dict(doc_data)
            
            print(f"⚠️ Document with ID {document_id} not found")
            return None
            
        except Exception as e:
            print(f"❌ Error retrieving document: {e}")
            return None
    
    def update_document(self, document: Document) -> bool:
        """
        Update an existing document
        
        Args:
            document: Document to update
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            storage_data = self._load_storage()
            
            # Find and update the document
            for i, doc_data in enumerate(storage_data["documents"]):
                if doc_data["id"] == document.id:
                    storage_data["documents"][i] = document.to_dict()
                    self._save_storage(storage_data)
                    print(f"✅ Updated document: {document.title}")
                    return True
            
            print(f"⚠️ Document with ID {document.id} not found for update")
            return False
            
        except Exception as e:
            print(f"❌ Error updating document: {e}")
            return False
    
    def delete_document(self, document_id: str) -> bool:
        """
        Delete a document by ID
        
        Args:
            document_id: ID of the document to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            storage_data = self._load_storage()
            
            # Find and remove the document
            for i, doc_data in enumerate(storage_data["documents"]):
                if doc_data["id"] == document_id:
                    deleted_doc = storage_data["documents"].pop(i)
                    self._save_storage(storage_data)
                    print(f"✅ Deleted document: {deleted_doc['title']}")
                    return True
            
            print(f"⚠️ Document with ID {document_id} not found for deletion")
            return False
            
        except Exception as e:
            print(f"❌ Error deleting document: {e}")
            return False
    
    def list_documents(self, limit: Optional[int] = None) -> List[Document]:
        """
        List all documents
        
        Args:
            limit: Maximum number of documents to return
            
        Returns:
            List of documents
        """
        try:
            storage_data = self._load_storage()
            documents = []
            
            doc_list = storage_data["documents"]
            if limit:
                doc_list = doc_list[:limit]
            
            for doc_data in doc_list:
                documents.append(Document.from_dict(doc_data))
            
            return documents
            
        except Exception as e:
            print(f"❌ Error listing documents: {e}")
            return []
    
    def search_documents(self, query: str, limit: Optional[int] = None) -> List[Document]:
        """
        Search documents by title or content
        
        Args:
            query: Search query
            limit: Maximum number of results to return
            
        Returns:
            List of matching documents
        """
        try:
            storage_data = self._load_storage()
            matching_docs = []
            
            query_lower = query.lower()
            
            for doc_data in storage_data["documents"]:
                # Search in title and content
                title_match = query_lower in doc_data["title"].lower()
                content_match = query_lower in doc_data["content"].lower()
                
                if title_match or content_match:
                    matching_docs.append(Document.from_dict(doc_data))
            
            # Sort by relevance (title matches first)
            matching_docs.sort(key=lambda doc: (
                query_lower not in doc.title.lower(),  # Title matches first
                -doc.stats.word_count  # Longer documents last
            ))
            
            if limit:
                matching_docs = matching_docs[:limit]
            
            return matching_docs
            
        except Exception as e:
            print(f"❌ Error searching documents: {e}")
            return []
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """
        Get storage statistics
        
        Returns:
            Dictionary with storage statistics
        """
        try:
            storage_data = self._load_storage()
            
            total_docs = len(storage_data["documents"])
            total_words = sum(doc["stats"]["word_count"] for doc in storage_data["documents"])
            
            # Count documents by category
            categories = {}
            for doc in storage_data["documents"]:
                category = doc["metadata"]["category"]
                categories[category] = categories.get(category, 0) + 1
            
            return {
                "total_documents": total_docs,
                "total_words": total_words,
                "categories": categories,
                "storage_file": str(self.documents_file),
                "last_updated": storage_data["metadata"]["last_updated"]
            }
            
        except Exception as e:
            print(f"❌ Error getting storage stats: {e}")
            return {}

# Example usage and testing
if __name__ == "__main__":
    # Test the storage service
    storage = DocumentStorage()
    
    # Create a test document
    from models.document import Document, DocumentMetadata
    
    test_doc = Document(
        title="Test Document",
        content="This is a test document for our storage system. It contains some sample text to verify everything works correctly!",
        metadata=DocumentMetadata(
            author="Test Author",
            category="test",
            tags=["test", "storage", "sample"]
        )
    )
    
    print("🧪 Testing Document Storage")
    print("=" * 50)
    
    # Test adding document
    if storage.add_document(test_doc):
        print("✅ Document added successfully")
    
    # Test retrieving document
    retrieved_doc = storage.get_document(test_doc.id)
    if retrieved_doc:
        print(f"✅ Document retrieved: {retrieved_doc.title}")
    
    # Test listing documents
    all_docs = storage.list_documents()
    print(f"✅ Found {len(all_docs)} documents in storage")
    
    # Test searching
    search_results = storage.search_documents("test")
    print(f"✅ Search found {len(search_results)} documents")
    
    # Test storage stats
    stats = storage.get_storage_stats()
    print(f"✅ Storage stats: {stats['total_documents']} documents, {stats['total_words']} words")
    
    print("=" * 50)
    print("🎉 Document storage working correctly!") 
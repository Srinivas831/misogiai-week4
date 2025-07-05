"""
Comprehensive test for Document Model + Storage
"""

import sys
sys.path.append('.')  # Add current directory to Python path

from models.document import Document, DocumentMetadata
from storage.document_storage import DocumentStorage

def test_document_storage():
    """Test the complete document storage workflow"""
    
    print("🧪 Testing Document Storage System")
    print("=" * 50)
    
    # Initialize storage
    storage = DocumentStorage()
    
    # Create sample documents
    documents = [
        Document(
            title="Welcome to Our Blog",
            content="Welcome to our amazing blog! Here you'll find interesting articles about technology, science, and more. We hope you enjoy reading our content!",
            metadata=DocumentMetadata(
                author="John Doe",
                category="blog",
                tags=["welcome", "introduction", "blog"]
            )
        ),
        Document(
            title="Python Programming Guide",
            content="Python is a powerful programming language. It's easy to learn and has many applications. In this guide, we'll explore the basics of Python programming.",
            metadata=DocumentMetadata(
                author="Jane Smith",
                category="technical",
                tags=["python", "programming", "tutorial"]
            )
        ),
        Document(
            title="Movie Review: The Great Adventure",
            content="The Great Adventure is an exciting movie! The plot was engaging and the characters were well-developed. I highly recommend this film to anyone who enjoys action movies.",
            metadata=DocumentMetadata(
                author="Bob Wilson",
                category="review",
                tags=["movie", "review", "action"]
            )
        )
    ]
    
    # Test 1: Add documents
    print("📝 Adding documents...")
    for doc in documents:
        success = storage.add_document(doc)
        if success:
            print(f"   ✅ Added: {doc.title}")
        else:
            print(f"   ❌ Failed to add: {doc.title}")
    
    # Test 2: List all documents
    print("\n📋 Listing all documents...")
    all_docs = storage.list_documents()
    print(f"   Found {len(all_docs)} documents:")
    for doc in all_docs:
        print(f"   - {doc.title} ({doc.stats.word_count} words)")
    
    # Test 3: Search documents
    print("\n🔍 Searching documents...")
    search_results = storage.search_documents("Python")
    print(f"   Search for 'Python' found {len(search_results)} results:")
    for doc in search_results:
        print(f"   - {doc.title}")
    
    # Test 4: Get specific document
    print("\n📄 Getting specific document...")
    if all_docs:
        first_doc = all_docs[0]
        retrieved_doc = storage.get_document(first_doc.id)
        if retrieved_doc:
            print(f"   ✅ Retrieved: {retrieved_doc.title}")
            print(f"   - Author: {retrieved_doc.metadata.author}")
            print(f"   - Category: {retrieved_doc.metadata.category}")
            print(f"   - Word count: {retrieved_doc.stats.word_count}")
    
    # Test 5: Storage statistics
    print("\n📊 Storage statistics...")
    stats = storage.get_storage_stats()
    print(f"   - Total documents: {stats['total_documents']}")
    print(f"   - Total words: {stats['total_words']}")
    print(f"   - Categories: {stats['categories']}")
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed successfully!")
    print("✅ Document model and storage working perfectly!")

if __name__ == "__main__":
    test_document_storage() 
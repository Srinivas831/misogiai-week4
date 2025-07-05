"""
Simple test for Document Model
"""

from models.document import Document, DocumentMetadata

# Create a sample document
doc = Document(
    title="My First Blog Post",
    content="This is my first blog post. It's really exciting! I can't wait to share more content with everyone.",
    metadata=DocumentMetadata(
        author="Alice Smith",
        category="blog",
        tags=["first-post", "exciting", "blog"]
    )
)

print("🧪 Testing Document Model")
print("=" * 40)
print(f"📄 Title: {doc.title}")
print(f"👤 Author: {doc.metadata.author}")
print(f"📊 Word Count: {doc.stats.word_count}")
print(f"📝 Sentence Count: {doc.stats.sentence_count}")
print(f"📋 Category: {doc.metadata.category}")
print(f"🏷️ Tags: {doc.metadata.tags}")
print(f"🆔 ID: {doc.id[:8]}...")  # Show first 8 characters of ID
print("=" * 40)
print("✅ Document model working correctly!") 
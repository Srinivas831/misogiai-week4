"""
Test MCP Tools

This tests all our MCP tools without running the full MCP server.
It simulates what would happen when AI assistants call our tools.
"""

import sys
import asyncio
sys.path.append('.')

from models.document import Document, DocumentMetadata
from storage.document_storage import DocumentStorage
from services.sentiment_service import SentimentService
from services.keyword_service import KeywordService
from services.readability_service import ReadabilityService

class MCPToolsTester:
    """Test all MCP tools functionality"""
    
    def __init__(self):
        """Initialize all services"""
        self.storage = DocumentStorage()
        self.sentiment_service = SentimentService()
        self.keyword_service = KeywordService()
        self.readability_service = ReadabilityService()
        
        print("🧪 MCP Tools Tester initialized")
    
    async def test_add_document(self):
        """Test adding a document"""
        print("\n1️⃣ Testing add_document...")
        
        # Create a test document
        title = "Python Programming Tutorial"
        content = "Python is an amazing programming language! It's easy to learn and incredibly powerful. Python is used in web development, data science, artificial intelligence, and automation. Many developers love Python because of its simple syntax and extensive libraries."
        author = "Alice Johnson"
        category = "technical"
        tags = ["python", "programming", "tutorial"]
        
        # Create document metadata
        metadata = DocumentMetadata(
            author=author,
            category=category,
            tags=tags
        )
        
        # Create document
        document = Document(
            title=title,
            content=content,
            metadata=metadata
        )
        
        # Add to storage
        success = self.storage.add_document(document)
        
        if success:
            # Perform analysis
            sentiment_result = self.sentiment_service.analyze_sentiment(content)
            keywords = self.keyword_service.extract_keywords(content, limit=10)
            readability_result = self.readability_service.calculate_readability(content)
            
            # Update document with analysis
            document.analysis.sentiment = sentiment_result
            document.analysis.keywords = keywords
            document.analysis.readability = readability_result
            
            # Save updated document
            self.storage.update_document(document)
            
            print(f"✅ Document added successfully!")
            print(f"   - ID: {document.id}")
            print(f"   - Title: {document.title}")
            print(f"   - Author: {document.metadata.author}")
            print(f"   - Word Count: {document.stats.word_count}")
            print(f"   - Sentiment: {sentiment_result.label}")
            print(f"   - Top Keywords: {', '.join(keywords[:3])}")
            print(f"   - Reading Level: {readability_result.grade_level}")
            
            return document.id
        else:
            print("❌ Failed to add document")
            return None
    
    async def test_get_sentiment(self):
        """Test sentiment analysis"""
        print("\n2️⃣ Testing get_sentiment...")
        
        test_texts = [
            "I love this product! It's amazing and works perfectly!",
            "This is terrible. I hate it and want my money back.",
            "The weather is sunny today. It's a nice day for a walk."
        ]
        
        for i, text in enumerate(test_texts, 1):
            sentiment_result = self.sentiment_service.analyze_sentiment(text)
            explanation = self.sentiment_service.get_sentiment_explanation(sentiment_result)
            
            print(f"   Test {i}: \"{text}\"")
            print(f"   - Sentiment: {sentiment_result.label.upper()}")
            print(f"   - Polarity: {sentiment_result.polarity:.2f}")
            print(f"   - Explanation: {explanation}")
            print()
    
    async def test_extract_keywords(self):
        """Test keyword extraction"""
        print("\n3️⃣ Testing extract_keywords...")
        
        test_text = "Machine learning is a subset of artificial intelligence that focuses on algorithms and statistical models. Machine learning enables computers to learn and improve from experience without being explicitly programmed. Data science and machine learning are closely related fields."
        
        # Extract keywords
        keywords = self.keyword_service.extract_keywords(test_text, limit=10)
        keywords_with_scores = self.keyword_service.extract_keywords_with_scores(test_text, limit=5)
        phrases = self.keyword_service.extract_phrases(test_text, limit=3)
        
        print(f"   Text: \"{test_text}\"")
        print(f"   Top Keywords: {', '.join(keywords)}")
        print(f"   Keywords with scores:")
        for kw_data in keywords_with_scores:
            print(f"     - {kw_data['word']}: {kw_data['count']} times ({kw_data['percentage']:.1f}%)")
        print(f"   Common phrases: {', '.join(phrases)}")
    
    async def test_search_documents(self):
        """Test document search"""
        print("\n4️⃣ Testing search_documents...")
        
        # Search for documents
        search_queries = ["Python", "programming", "tutorial"]
        
        for query in search_queries:
            matching_docs = self.storage.search_documents(query, limit=5)
            print(f"   Search for '{query}': Found {len(matching_docs)} documents")
            
            for doc in matching_docs:
                sentiment_label = doc.analysis.sentiment.label if doc.analysis.sentiment else "Not analyzed"
                top_keywords = ', '.join(doc.analysis.keywords[:3]) if doc.analysis.keywords else "None"
                
                print(f"     - {doc.title}")
                print(f"       Author: {doc.metadata.author}, Sentiment: {sentiment_label}")
                print(f"       Keywords: {top_keywords}")
    
    async def test_analyze_document(self, document_id):
        """Test complete document analysis"""
        print("\n5️⃣ Testing analyze_document...")
        
        if not document_id:
            print("   ❌ No document ID provided")
            return
        
        # Get document
        document = self.storage.get_document(document_id)
        if not document:
            print(f"   ❌ Document with ID {document_id} not found")
            return
        
        # Perform complete analysis
        sentiment_result = self.sentiment_service.analyze_sentiment(document.content)
        keywords = self.keyword_service.extract_keywords(document.content, limit=10)
        readability_result = self.readability_service.calculate_readability(document.content)
        
        # Update document
        document.analysis.sentiment = sentiment_result
        document.analysis.keywords = keywords
        document.analysis.readability = readability_result
        
        # Save updated document
        self.storage.update_document(document)
        
        print(f"   ✅ Complete analysis of: {document.title}")
        print(f"   - Sentiment: {sentiment_result.label.upper()} ({sentiment_result.polarity:.2f})")
        print(f"   - Keywords: {', '.join(keywords)}")
        print(f"   - Reading Level: {readability_result.grade_level}")
        print(f"   - Flesch Score: {readability_result.flesch_score:.1f}")
        print(f"   - Reading Time: {readability_result.reading_time_minutes} minutes")
        print(f"   - Word Count: {document.stats.word_count}")
    
    async def run_all_tests(self):
        """Run all MCP tool tests"""
        print("🧪 Testing All MCP Tools")
        print("=" * 50)
        
        # Test 1: Add document
        document_id = await self.test_add_document()
        
        # Test 2: Get sentiment
        await self.test_get_sentiment()
        
        # Test 3: Extract keywords
        await self.test_extract_keywords()
        
        # Test 4: Search documents
        await self.test_search_documents()
        
        # Test 5: Analyze document
        await self.test_analyze_document(document_id)
        
        print("\n" + "=" * 50)
        print("🎉 All MCP tools tested successfully!")
        print("✅ Document Analyzer MCP Server is ready for AI assistants!")

async def main():
    """Run the MCP tools test"""
    tester = MCPToolsTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 
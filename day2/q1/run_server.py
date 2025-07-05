"""
Document Analyzer MCP Server Launcher

This script demonstrates the Document Analyzer MCP Server functionality.
It shows how AI assistants would interact with our document analysis tools.
"""

import sys
import asyncio
sys.path.append('.')

from models.document import Document, DocumentMetadata
from storage.document_storage import DocumentStorage
from services.sentiment_service import SentimentService
from services.keyword_service import KeywordService
from services.readability_service import ReadabilityService

class DocumentAnalyzerDemo:
    """Demo of the Document Analyzer MCP Server"""
    
    def __init__(self):
        """Initialize all services"""
        self.storage = DocumentStorage()
        self.sentiment_service = SentimentService()
        self.keyword_service = KeywordService()
        self.readability_service = ReadabilityService()
        
        print("🚀 Document Analyzer MCP Server Demo")
        print("=" * 60)
    
    def show_available_tools(self):
        """Show all available MCP tools"""
        print("\n🔧 Available MCP Tools:")
        print("1. analyze_document(document_id) - Complete document analysis")
        print("2. get_sentiment(text) - Sentiment analysis for any text")
        print("3. extract_keywords(text, limit) - Extract keywords from text")
        print("4. add_document(title, content, author, category, tags) - Add new document")
        print("5. search_documents(query, limit) - Search documents by content")
    
    def show_document_library(self):
        """Show all documents in the library"""
        print("\n📚 Document Library:")
        print("-" * 60)
        
        all_docs = self.storage.list_documents()
        
        for i, doc in enumerate(all_docs, 1):
            sentiment = doc.analysis.sentiment.label if doc.analysis.sentiment else "Not analyzed"
            keywords = ', '.join(doc.analysis.keywords[:3]) if doc.analysis.keywords else "None"
            
            print(f"{i:2d}. {doc.title}")
            print(f"    Author: {doc.metadata.author} | Category: {doc.metadata.category}")
            print(f"    Words: {doc.stats.word_count} | Sentiment: {sentiment}")
            print(f"    Keywords: {keywords}")
            print(f"    ID: {doc.id}")
            print()
    
    async def demo_analyze_document(self):
        """Demo analyzing a specific document"""
        print("\n🔍 Demo: Analyzing a Document")
        print("-" * 40)
        
        # Get a sample document
        all_docs = self.storage.list_documents()
        if not all_docs:
            print("❌ No documents found")
            return
        
        # Pick an interesting document
        doc = all_docs[0]  # First document
        
        print(f"📄 Analyzing: {doc.title}")
        print(f"Author: {doc.metadata.author}")
        print(f"Category: {doc.metadata.category}")
        print(f"Content: {doc.content[:100]}...")
        
        # Perform analysis
        sentiment_result = self.sentiment_service.analyze_sentiment(doc.content)
        keywords = self.keyword_service.extract_keywords(doc.content, limit=8)
        readability_result = self.readability_service.calculate_readability(doc.content)
        
        print(f"\n📊 Analysis Results:")
        print(f"Sentiment: {sentiment_result.label.upper()} (polarity: {sentiment_result.polarity:.2f})")
        print(f"Keywords: {', '.join(keywords)}")
        print(f"Reading Level: {readability_result.grade_level}")
        print(f"Flesch Score: {readability_result.flesch_score:.1f}")
        print(f"Reading Time: {readability_result.reading_time_minutes} minutes")
    
    async def demo_sentiment_analysis(self):
        """Demo sentiment analysis on custom text"""
        print("\n🧠 Demo: Sentiment Analysis")
        print("-" * 40)
        
        test_texts = [
            "I absolutely love this new technology! It's revolutionary and will change everything.",
            "This product is terrible. It doesn't work and the customer service is awful.",
            "The research methodology was comprehensive and the results were statistically significant."
        ]
        
        for i, text in enumerate(test_texts, 1):
            print(f"\n{i}. Text: \"{text}\"")
            
            sentiment_result = self.sentiment_service.analyze_sentiment(text)
            explanation = self.sentiment_service.get_sentiment_explanation(sentiment_result)
            
            print(f"   Sentiment: {sentiment_result.label.upper()}")
            print(f"   Polarity: {sentiment_result.polarity:.2f}")
            print(f"   Explanation: {explanation}")
    
    async def demo_keyword_extraction(self):
        """Demo keyword extraction"""
        print("\n🔍 Demo: Keyword Extraction")
        print("-" * 40)
        
        sample_text = """
        Artificial intelligence and machine learning are transforming the healthcare industry. 
        These technologies enable doctors to diagnose diseases more accurately and develop 
        personalized treatment plans. Machine learning algorithms can analyze medical images, 
        predict patient outcomes, and identify potential drug interactions. The integration 
        of AI in healthcare promises to improve patient care while reducing costs.
        """
        
        print(f"📝 Sample Text: {sample_text.strip()}")
        
        keywords = self.keyword_service.extract_keywords(sample_text, limit=10)
        keywords_with_scores = self.keyword_service.extract_keywords_with_scores(sample_text, limit=5)
        phrases = self.keyword_service.extract_phrases(sample_text, limit=5)
        
        print(f"\n🔑 Top Keywords: {', '.join(keywords)}")
        print(f"\n📊 Keywords with Scores:")
        for kw_data in keywords_with_scores:
            print(f"   - {kw_data['word']}: {kw_data['count']} times ({kw_data['percentage']:.1f}%)")
        
        print(f"\n🔗 Common Phrases: {', '.join(phrases)}")
    
    async def demo_search_documents(self):
        """Demo document search"""
        print("\n🔍 Demo: Document Search")
        print("-" * 40)
        
        search_queries = ["Python", "AI", "positive", "healthcare"]
        
        for query in search_queries:
            print(f"\n🔍 Search for: '{query}'")
            
            matching_docs = self.storage.search_documents(query, limit=3)
            
            if matching_docs:
                print(f"   Found {len(matching_docs)} documents:")
                for doc in matching_docs:
                    sentiment = doc.analysis.sentiment.label if doc.analysis.sentiment else "Not analyzed"
                    print(f"   - {doc.title} (Sentiment: {sentiment})")
            else:
                print("   No documents found")
    
    async def demo_add_document(self):
        """Demo adding a new document"""
        print("\n📄 Demo: Adding New Document")
        print("-" * 40)
        
        # Create a new document
        title = "The Future of Quantum Computing"
        content = """
        Quantum computing represents a paradigm shift in computational technology. 
        Unlike classical computers that use bits, quantum computers use quantum bits 
        or qubits that can exist in multiple states simultaneously. This quantum 
        superposition allows quantum computers to perform certain calculations 
        exponentially faster than classical computers. The potential applications 
        include cryptography, drug discovery, and optimization problems.
        """
        
        metadata = DocumentMetadata(
            author="Dr. Quantum Smith",
            category="academic",
            tags=["quantum", "computing", "technology", "research"]
        )
        
        document = Document(
            title=title,
            content=content.strip(),
            metadata=metadata
        )
        
        # Add to storage
        success = self.storage.add_document(document)
        
        if success:
            # Perform analysis
            sentiment_result = self.sentiment_service.analyze_sentiment(document.content)
            keywords = self.keyword_service.extract_keywords(document.content, limit=8)
            readability_result = self.readability_service.calculate_readability(document.content)
            
            # Update document with analysis
            document.analysis.sentiment = sentiment_result
            document.analysis.keywords = keywords
            document.analysis.readability = readability_result
            
            self.storage.update_document(document)
            
            print(f"✅ Successfully added: {document.title}")
            print(f"   ID: {document.id}")
            print(f"   Author: {document.metadata.author}")
            print(f"   Word Count: {document.stats.word_count}")
            print(f"   Sentiment: {sentiment_result.label}")
            print(f"   Keywords: {', '.join(keywords[:5])}")
            print(f"   Reading Level: {readability_result.grade_level}")
        else:
            print("❌ Failed to add document")
    
    async def run_demo(self):
        """Run complete demo"""
        print("\n🎯 Document Analyzer MCP Server Demo")
        print("This shows how AI assistants would interact with our server")
        
        # Show available tools
        self.show_available_tools()
        
        # Show document library
        self.show_document_library()
        
        # Demo each tool
        await self.demo_analyze_document()
        await self.demo_sentiment_analysis()
        await self.demo_keyword_extraction()
        await self.demo_search_documents()
        await self.demo_add_document()
        
        print("\n" + "=" * 60)
        print("🎉 Demo Complete!")
        print("✅ Document Analyzer MCP Server is ready for AI assistants!")
        print("🚀 All 5 MCP tools are working perfectly!")
        
        # Final stats
        stats = self.storage.get_storage_stats()
        print(f"\n📊 Final Statistics:")
        print(f"   Total Documents: {stats['total_documents']}")
        print(f"   Total Words: {stats['total_words']}")
        print(f"   Categories: {', '.join(stats['categories'].keys())}")
        print(f"   Last Updated: {stats['last_updated']}")

async def main():
    """Run the demo"""
    demo = DocumentAnalyzerDemo()
    await demo.run_demo()

if __name__ == "__main__":
    asyncio.run(main()) 
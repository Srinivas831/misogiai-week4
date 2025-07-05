"""
Document Analyzer MCP Server

This is the main MCP server that provides document analysis tools to AI assistants.
It's like a waiter in a restaurant - it takes requests from AI assistants and 
delivers the results from our analysis services.

MCP Tools provided:
1. analyze_document(document_id) - Complete analysis of a stored document
2. get_sentiment(text) - Sentiment analysis for any text
3. extract_keywords(text, limit) - Extract keywords from any text
4. add_document(document_data) - Add new documents
5. search_documents(query) - Search through documents
"""

import asyncio
import json
import sys
from typing import Any, Dict, List, Optional
from pathlib import Path

sys.path.append('.')

# Import MCP components
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
import mcp.types as types

# Import our services
from models.document import Document, DocumentMetadata
from storage.document_storage import DocumentStorage
from services.sentiment_service import SentimentService
from services.keyword_service import KeywordService
from services.readability_service import ReadabilityService
from config import MCP_SERVER_CONFIG

class DocumentAnalyzerMCPServer:
    """
    Document Analyzer MCP Server
    
    This server provides AI assistants with document analysis capabilities.
    Think of it as a smart assistant that can analyze documents for:
    - Sentiment (positive/negative/neutral)
    - Keywords (important words)
    - Readability (how easy to read)
    - Document management (store, search, retrieve)
    """
    
    def __init__(self):
        """Initialize the MCP server and all services"""
        print("🚀 Initializing Document Analyzer MCP Server...")
        
        # Initialize MCP server
        self.server = Server(MCP_SERVER_CONFIG["name"])
        
        # Initialize our services
        self.storage = DocumentStorage()
        self.sentiment_service = SentimentService()
        self.keyword_service = KeywordService()
        self.readability_service = ReadabilityService()
        
        # Register our tools
        self._register_tools()
        
        print("✅ Document Analyzer MCP Server initialized successfully!")
    
    def _register_tools(self):
        """Register all MCP tools with the server"""
        
        # Tool 1: Analyze Document
        @self.server.tool()
        async def analyze_document(document_id: str) -> List[types.TextContent]:
            """
            Complete analysis of a stored document
            
            Args:
                document_id: ID of the document to analyze
                
            Returns:
                Complete analysis results including sentiment, keywords, and readability
            """
            try:
                # Get document from storage
                document = self.storage.get_document(document_id)
                if not document:
                    return [types.TextContent(
                        type="text",
                        text=f"❌ Document with ID {document_id} not found"
                    )]
                
                # Perform comprehensive analysis
                # 1. Sentiment Analysis
                sentiment_result = self.sentiment_service.analyze_sentiment(document.content)
                
                # 2. Keyword Extraction
                keywords = self.keyword_service.extract_keywords(document.content, limit=10)
                
                # 3. Readability Analysis
                readability_result = self.readability_service.calculate_readability(document.content)
                
                # Update document with analysis results
                document.analysis.sentiment = sentiment_result
                document.analysis.keywords = keywords
                document.analysis.readability = readability_result
                
                # Save updated document
                self.storage.update_document(document)
                
                # Format results
                analysis_text = f"""
📄 **Document Analysis Results**

**Document Information:**
- Title: {document.title}
- Author: {document.metadata.author}
- Category: {document.metadata.category}
- Word Count: {document.stats.word_count}
- Reading Time: {readability_result.reading_time_minutes} minutes

**Sentiment Analysis:**
- Overall Sentiment: {sentiment_result.label.upper()}
- Polarity Score: {sentiment_result.polarity:.2f} (-1 to 1)
- Subjectivity: {sentiment_result.subjectivity:.2f} (0 to 1)
- Confidence: {sentiment_result.confidence:.2f}

**Keywords:**
- Top Keywords: {', '.join(keywords[:5])}
- All Keywords: {', '.join(keywords)}

**Readability Analysis:**
- Flesch Reading Ease: {readability_result.flesch_score:.1f}
- Grade Level: {readability_result.grade_level}
- Flesch-Kincaid Grade: {readability_result.flesch_kincaid_grade:.1f}

**Document Statistics:**
- Words: {document.stats.word_count}
- Sentences: {document.stats.sentence_count}
- Paragraphs: {document.stats.paragraph_count}
- Average words per sentence: {document.stats.avg_words_per_sentence:.1f}
"""
                
                return [types.TextContent(type="text", text=analysis_text)]
                
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Error analyzing document: {str(e)}"
                )]
        
        # Tool 2: Get Sentiment
        @self.server.tool()
        async def get_sentiment(text: str) -> List[types.TextContent]:
            """
            Analyze sentiment of any text
            
            Args:
                text: Text to analyze for sentiment
                
            Returns:
                Sentiment analysis results
            """
            try:
                if not text or not text.strip():
                    return [types.TextContent(
                        type="text",
                        text="❌ Please provide text to analyze"
                    )]
                
                # Analyze sentiment
                sentiment_result = self.sentiment_service.analyze_sentiment(text)
                explanation = self.sentiment_service.get_sentiment_explanation(sentiment_result)
                
                # Format results
                sentiment_text = f"""
🧠 **Sentiment Analysis Results**

**Text:** "{text}"

**Results:**
- Sentiment: {sentiment_result.label.upper()}
- Polarity: {sentiment_result.polarity:.2f} (-1 = very negative, 1 = very positive)
- Subjectivity: {sentiment_result.subjectivity:.2f} (0 = objective, 1 = subjective)
- Confidence: {sentiment_result.confidence:.2f}

**Explanation:** {explanation}
"""
                
                return [types.TextContent(type="text", text=sentiment_text)]
                
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Error analyzing sentiment: {str(e)}"
                )]
        
        # Tool 3: Extract Keywords
        @self.server.tool()
        async def extract_keywords(text: str, limit: int = 10) -> List[types.TextContent]:
            """
            Extract keywords from text
            
            Args:
                text: Text to extract keywords from
                limit: Maximum number of keywords to return (default: 10)
                
            Returns:
                List of extracted keywords
            """
            try:
                if not text or not text.strip():
                    return [types.TextContent(
                        type="text",
                        text="❌ Please provide text to extract keywords from"
                    )]
                
                # Extract keywords
                keywords = self.keyword_service.extract_keywords(text, limit=limit)
                keywords_with_scores = self.keyword_service.extract_keywords_with_scores(text, limit=limit)
                
                # Format results
                if not keywords:
                    return [types.TextContent(
                        type="text",
                        text="⚠️ No keywords found in the provided text"
                    )]
                
                keywords_text = f"""
🔍 **Keyword Extraction Results**

**Text:** "{text}"

**Top {len(keywords)} Keywords:**
"""
                
                for i, (keyword, keyword_data) in enumerate(zip(keywords, keywords_with_scores), 1):
                    keywords_text += f"   {i}. {keyword} (appears {keyword_data['count']} times, {keyword_data['percentage']:.1f}%)\n"
                
                # Add phrases if available
                phrases = self.keyword_service.extract_phrases(text, limit=5)
                if phrases:
                    keywords_text += f"\n**Common Phrases:**\n"
                    for i, phrase in enumerate(phrases, 1):
                        keywords_text += f"   {i}. {phrase}\n"
                
                return [types.TextContent(type="text", text=keywords_text)]
                
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Error extracting keywords: {str(e)}"
                )]
        
        # Tool 4: Add Document
        @self.server.tool()
        async def add_document(title: str, content: str, author: str = "Unknown", 
                             category: str = "general", tags: Optional[List[str]] = None) -> List[types.TextContent]:
            """
            Add a new document to the storage
            
            Args:
                title: Document title
                content: Document content
                author: Document author (default: "Unknown")
                category: Document category (default: "general")
                tags: List of tags for the document
                
            Returns:
                Success message with document ID
            """
            try:
                if not title or not content:
                    return [types.TextContent(
                        type="text",
                        text="❌ Please provide both title and content for the document"
                    )]
                
                # Create document metadata
                metadata = DocumentMetadata(
                    author=author,
                    category=category,
                    tags=tags or []
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
                    # Perform initial analysis
                    sentiment_result = self.sentiment_service.analyze_sentiment(content)
                    keywords = self.keyword_service.extract_keywords(content, limit=10)
                    readability_result = self.readability_service.calculate_readability(content)
                    
                    # Update document with analysis
                    document.analysis.sentiment = sentiment_result
                    document.analysis.keywords = keywords
                    document.analysis.readability = readability_result
                    
                    # Save updated document
                    self.storage.update_document(document)
                    
                    result_text = f"""
✅ **Document Added Successfully**

**Document Information:**
- ID: {document.id}
- Title: {document.title}
- Author: {document.metadata.author}
- Category: {document.metadata.category}
- Word Count: {document.stats.word_count}
- Tags: {', '.join(document.metadata.tags) if document.metadata.tags else 'None'}

**Initial Analysis:**
- Sentiment: {sentiment_result.label.upper()}
- Top Keywords: {', '.join(keywords[:5])}
- Reading Level: {readability_result.grade_level}
- Reading Time: {readability_result.reading_time_minutes} minutes
"""
                    
                    return [types.TextContent(type="text", text=result_text)]
                else:
                    return [types.TextContent(
                        type="text",
                        text="❌ Failed to add document to storage"
                    )]
                
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Error adding document: {str(e)}"
                )]
        
        # Tool 5: Search Documents
        @self.server.tool()
        async def search_documents(query: str, limit: int = 10) -> List[types.TextContent]:
            """
            Search documents by content or title
            
            Args:
                query: Search query
                limit: Maximum number of results to return (default: 10)
                
            Returns:
                List of matching documents with analysis
            """
            try:
                if not query or not query.strip():
                    return [types.TextContent(
                        type="text",
                        text="❌ Please provide a search query"
                    )]
                
                # Search documents
                matching_docs = self.storage.search_documents(query, limit=limit)
                
                if not matching_docs:
                    return [types.TextContent(
                        type="text",
                        text=f"⚠️ No documents found matching query: '{query}'"
                    )]
                
                # Format results
                search_text = f"""
🔍 **Search Results**

**Query:** "{query}"
**Found {len(matching_docs)} matching documents:**

"""
                
                for i, doc in enumerate(matching_docs, 1):
                    # Get sentiment label
                    sentiment_label = doc.analysis.sentiment.label if doc.analysis.sentiment else "Not analyzed"
                    
                    # Get top keywords
                    top_keywords = ', '.join(doc.analysis.keywords[:3]) if doc.analysis.keywords else "None"
                    
                    search_text += f"""
**{i}. {doc.title}**
- ID: {doc.id}
- Author: {doc.metadata.author}
- Category: {doc.metadata.category}
- Word Count: {doc.stats.word_count}
- Sentiment: {sentiment_label}
- Keywords: {top_keywords}
- Content Preview: {doc.content[:100]}{'...' if len(doc.content) > 100 else ''}

"""
                
                return [types.TextContent(type="text", text=search_text)]
                
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Error searching documents: {str(e)}"
                )]

    async def run(self):
        """Run the MCP server"""
        print("🌐 Starting Document Analyzer MCP Server...")
        print("🔧 Available tools:")
        print("   1. analyze_document(document_id)")
        print("   2. get_sentiment(text)")
        print("   3. extract_keywords(text, limit)")
        print("   4. add_document(title, content, author, category, tags)")
        print("   5. search_documents(query, limit)")
        print("✅ MCP Server is ready to receive requests!")
        
        # For now, we'll just keep the server running
        # In a real implementation, this would handle MCP protocol communication
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n⏹️ MCP Server stopped by user")

# Example usage and testing
if __name__ == "__main__":
    async def main():
        # Create and run the MCP server
        server = DocumentAnalyzerMCPServer()
        await server.run()
    
    # Run the server
    asyncio.run(main()) 
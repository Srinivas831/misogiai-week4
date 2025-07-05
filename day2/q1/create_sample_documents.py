"""
Create Sample Documents

This script creates 15+ diverse sample documents to demonstrate
the Document Analyzer MCP Server capabilities.

Categories:
- News articles
- Blog posts
- Technical documentation
- Creative writing
- Academic papers
- Product reviews
- Social media posts
"""

import sys
import asyncio
sys.path.append('.')

from models.document import Document, DocumentMetadata
from storage.document_storage import DocumentStorage
from services.sentiment_service import SentimentService
from services.keyword_service import KeywordService
from services.readability_service import ReadabilityService

class SampleDocumentCreator:
    """Creates diverse sample documents for testing"""
    
    def __init__(self):
        """Initialize services"""
        self.storage = DocumentStorage()
        self.sentiment_service = SentimentService()
        self.keyword_service = KeywordService()
        self.readability_service = ReadabilityService()
        
        print("📄 Sample Document Creator initialized")
    
    def create_sample_documents(self):
        """Create all sample documents"""
        
        # News Articles
        news_articles = [
            {
                "title": "New AI Breakthrough Announced",
                "content": "Scientists at MIT have announced a major breakthrough in artificial intelligence research. The new algorithm can process natural language with unprecedented accuracy, potentially revolutionizing how we interact with computers. The research team spent three years developing this technology, which could have applications in healthcare, education, and customer service.",
                "author": "Sarah Chen",
                "category": "news",
                "tags": ["AI", "technology", "research", "MIT"]
            },
            {
                "title": "Climate Change Summit Reaches Agreement",
                "content": "World leaders have reached a historic agreement on climate change action. The summit concluded with commitments to reduce carbon emissions by 50% within the next decade. Environmental groups are cautiously optimistic about the agreement, though some critics argue the measures don't go far enough.",
                "author": "Michael Rodriguez",
                "category": "news",
                "tags": ["climate", "environment", "politics", "international"]
            },
            {
                "title": "Stock Market Hits Record High",
                "content": "The stock market closed at a record high today, driven by strong earnings reports from major technology companies. Investors are optimistic about the economic outlook, with many analysts predicting continued growth in the coming months. However, some experts warn that the market may be overvalued.",
                "author": "Jennifer Park",
                "category": "news",
                "tags": ["finance", "stocks", "economy", "technology"]
            }
        ]
        
        # Blog Posts
        blog_posts = [
            {
                "title": "My Journey Learning Python",
                "content": "I started learning Python six months ago, and it's been an amazing journey! At first, I was intimidated by programming, but Python's simple syntax made it much more approachable. I've built several projects, including a web scraper and a simple game. The Python community is incredibly supportive and welcoming to beginners.",
                "author": "Alex Thompson",
                "category": "blog",
                "tags": ["python", "programming", "learning", "personal"]
            },
            {
                "title": "The Best Coffee Shops in Seattle",
                "content": "Seattle is famous for its coffee culture, and after living here for five years, I've discovered some hidden gems. My favorite is Victrola Coffee on Capitol Hill - their espresso is incredible and the atmosphere is perfect for working. Another great spot is Analog Coffee, which has the best pastries in the city.",
                "author": "Emma Wilson",
                "category": "blog",
                "tags": ["coffee", "Seattle", "food", "lifestyle"]
            },
            {
                "title": "Tips for Remote Work Success",
                "content": "Working from home can be challenging, but with the right strategies, it can be incredibly productive. I've learned to create a dedicated workspace, establish clear boundaries between work and personal time, and maintain regular communication with my team. The key is finding what works best for your personality and work style.",
                "author": "David Lee",
                "category": "blog",
                "tags": ["remote work", "productivity", "tips", "career"]
            }
        ]
        
        # Technical Documentation
        technical_docs = [
            {
                "title": "REST API Documentation",
                "content": "This API provides access to user data and authentication services. All endpoints require authentication via API key. The base URL is https://api.example.com/v1/. Rate limiting is enforced at 1000 requests per hour per API key. All responses are returned in JSON format with standard HTTP status codes.",
                "author": "Dev Team",
                "category": "technical",
                "tags": ["API", "documentation", "REST", "development"]
            },
            {
                "title": "Database Schema Design",
                "content": "The database schema consists of five main tables: users, products, orders, order_items, and categories. Foreign key relationships maintain data integrity. Indexes are implemented on frequently queried columns to optimize performance. The schema supports both MySQL and PostgreSQL databases.",
                "author": "Database Team",
                "category": "technical",
                "tags": ["database", "schema", "design", "SQL"]
            }
        ]
        
        # Creative Writing
        creative_writing = [
            {
                "title": "The Last Library",
                "content": "In a world where books had become obsolete, Maria discovered the last library hidden beneath the city. Dust motes danced in the filtered sunlight as she walked between towering shelves filled with forgotten stories. Each book held memories of a time when words on paper could transport readers to other worlds. She picked up a worn novel and began to read, feeling the magic that technology had almost erased.",
                "author": "Rachel Green",
                "category": "creative",
                "tags": ["fiction", "short story", "library", "books"]
            },
            {
                "title": "Morning Coffee Haiku",
                "content": "Steam rises gently / From my morning coffee cup / Peace before the day",
                "author": "James Kim",
                "category": "creative",
                "tags": ["poetry", "haiku", "coffee", "morning"]
            }
        ]
        
        # Academic Papers
        academic_papers = [
            {
                "title": "Machine Learning Applications in Healthcare",
                "content": "This paper examines the implementation of machine learning algorithms in medical diagnosis and treatment planning. We analyze three case studies where ML models achieved diagnostic accuracy comparable to human specialists. The methodology involved training convolutional neural networks on medical imaging data from 10,000 patients. Results indicate significant potential for improving healthcare outcomes while reducing costs.",
                "author": "Dr. Lisa Anderson",
                "category": "academic",
                "tags": ["machine learning", "healthcare", "research", "diagnosis"]
            },
            {
                "title": "Sustainable Energy Solutions",
                "content": "This research investigates renewable energy technologies and their potential for widespread adoption. We conducted a comprehensive analysis of solar, wind, and hydroelectric power systems across different geographical regions. Our findings suggest that a combination of these technologies could meet 80% of global energy demands within the next two decades.",
                "author": "Dr. Robert Martinez",
                "category": "academic",
                "tags": ["renewable energy", "sustainability", "research", "environment"]
            }
        ]
        
        # Product Reviews
        product_reviews = [
            {
                "title": "Amazing Wireless Headphones",
                "content": "These headphones exceeded all my expectations! The sound quality is crystal clear, and the noise cancellation is fantastic. I can wear them for hours without any discomfort. The battery life is incredible - I only need to charge them once a week. Highly recommend to anyone looking for premium audio experience.",
                "author": "Mark Johnson",
                "category": "review",
                "tags": ["headphones", "audio", "technology", "positive"]
            },
            {
                "title": "Disappointing Restaurant Experience",
                "content": "Unfortunately, my experience at this restaurant was quite disappointing. The service was slow, and the food arrived cold. The staff seemed overwhelmed and inattentive. The prices were high for the quality offered. I've had much better experiences at other restaurants in the area and won't be returning.",
                "author": "Susan Davis",
                "category": "review",
                "tags": ["restaurant", "food", "service", "negative"]
            }
        ]
        
        # Social Media Posts
        social_media = [
            {
                "title": "Beautiful Sunset Today",
                "content": "Just witnessed the most incredible sunset! The sky was painted in shades of orange, pink, and purple. Sometimes nature reminds us to pause and appreciate the simple beauty around us. #sunset #nature #grateful",
                "author": "Instagram User",
                "category": "social_media",
                "tags": ["sunset", "nature", "photography", "gratitude"]
            },
            {
                "title": "New Recipe Success",
                "content": "Finally nailed that chocolate cake recipe I've been working on! Third time's the charm. The secret ingredient was a pinch of sea salt. Can't wait to share it with friends this weekend. #baking #chocolate #success",
                "author": "Food Blogger",
                "category": "social_media",
                "tags": ["baking", "recipe", "chocolate", "cooking"]
            }
        ]
        
        # Combine all documents
        all_documents = news_articles + blog_posts + technical_docs + creative_writing + academic_papers + product_reviews + social_media
        
        print(f"📄 Creating {len(all_documents)} sample documents...")
        
        # Add each document
        for doc_data in all_documents:
            metadata = DocumentMetadata(
                author=doc_data["author"],
                category=doc_data["category"],
                tags=doc_data["tags"]
            )
            
            document = Document(
                title=doc_data["title"],
                content=doc_data["content"],
                metadata=metadata
            )
            
            # Add to storage
            success = self.storage.add_document(document)
            
            if success:
                # Perform analysis
                sentiment_result = self.sentiment_service.analyze_sentiment(document.content)
                keywords = self.keyword_service.extract_keywords(document.content, limit=10)
                readability_result = self.readability_service.calculate_readability(document.content)
                
                # Update document with analysis
                document.analysis.sentiment = sentiment_result
                document.analysis.keywords = keywords
                document.analysis.readability = readability_result
                
                # Save updated document
                self.storage.update_document(document)
                
                print(f"   ✅ Added: {document.title}")
            else:
                print(f"   ❌ Failed to add: {doc_data['title']}")
        
        print(f"\n🎉 Successfully created {len(all_documents)} sample documents!")
        
        # Show summary
        self.show_summary()
    
    def show_summary(self):
        """Show summary of all documents"""
        print("\n📊 Document Summary:")
        print("=" * 50)
        
        # Get all documents
        all_docs = self.storage.list_documents()
        
        # Count by category
        categories = {}
        sentiments = {"positive": 0, "negative": 0, "neutral": 0}
        total_words = 0
        
        for doc in all_docs:
            # Count categories
            category = doc.metadata.category
            categories[category] = categories.get(category, 0) + 1
            
            # Count sentiments
            if doc.analysis.sentiment:
                sentiment = doc.analysis.sentiment.label
                sentiments[sentiment] = sentiments.get(sentiment, 0) + 1
            
            # Count words
            total_words += doc.stats.word_count
        
        print(f"📄 Total Documents: {len(all_docs)}")
        print(f"📝 Total Words: {total_words}")
        print(f"⏱️ Estimated Reading Time: {total_words / 200:.1f} minutes")
        
        print(f"\n📂 Documents by Category:")
        for category, count in categories.items():
            print(f"   {category}: {count} documents")
        
        print(f"\n😊 Sentiment Distribution:")
        for sentiment, count in sentiments.items():
            percentage = (count / len(all_docs)) * 100
            print(f"   {sentiment}: {count} documents ({percentage:.1f}%)")
        
        print("=" * 50)
        print("✅ Sample documents created successfully!")
        print("🚀 Document Analyzer MCP Server is ready with real data!")

def main():
    """Create sample documents"""
    creator = SampleDocumentCreator()
    creator.create_sample_documents()

if __name__ == "__main__":
    main() 
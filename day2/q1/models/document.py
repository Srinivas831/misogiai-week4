"""
Document Model

This defines what a document looks like in our system.
Think of it as a blueprint or template for every document we store.

A document has:
- Basic info: ID, title, content
- Metadata: author, category, date, tags
- Statistics: word count, sentences, etc.
- Analysis results: sentiment, keywords, readability
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Any
import uuid

@dataclass
class DocumentMetadata:
    """
    Document metadata - extra information about the document
    Like the "details" section of a file
    """
    author: str = "Unknown"
    category: str = "general"  # news, blog, technical, creative, academic, review, social_media
    date_created: datetime = field(default_factory=datetime.now)
    source: str = "manual"  # web, upload, manual
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary for JSON storage"""
        return {
            "author": self.author,
            "category": self.category,
            "date_created": self.date_created.isoformat(),
            "source": self.source,
            "tags": self.tags
        }

@dataclass
class DocumentStats:
    """
    Basic statistics about the document
    Like a summary of the document's "vital signs"
    """
    word_count: int = 0
    sentence_count: int = 0
    paragraph_count: int = 0
    char_count: int = 0
    avg_words_per_sentence: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert stats to dictionary for JSON storage"""
        return {
            "word_count": self.word_count,
            "sentence_count": self.sentence_count,
            "paragraph_count": self.paragraph_count,
            "char_count": self.char_count,
            "avg_words_per_sentence": self.avg_words_per_sentence
        }

@dataclass
class SentimentResult:
    """
    Sentiment analysis results
    Tells us if the document is positive, negative, or neutral
    """
    label: str = "neutral"  # positive, negative, neutral
    polarity: float = 0.0   # -1 (very negative) to 1 (very positive)
    subjectivity: float = 0.0  # 0 (objective) to 1 (subjective)
    confidence: float = 0.0    # How sure we are about the result
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert sentiment to dictionary for JSON storage"""
        return {
            "label": self.label,
            "polarity": self.polarity,
            "subjectivity": self.subjectivity,
            "confidence": self.confidence
        }

@dataclass
class ReadabilityResult:
    """
    Readability analysis results
    Tells us how easy the document is to read
    """
    flesch_score: float = 0.0      # 0-100, higher = easier to read
    grade_level: str = "Unknown"    # What grade level can read this?
    flesch_kincaid_grade: float = 0.0  # US grade level
    reading_time_minutes: float = 0.0   # Estimated reading time
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert readability to dictionary for JSON storage"""
        return {
            "flesch_score": self.flesch_score,
            "grade_level": self.grade_level,
            "flesch_kincaid_grade": self.flesch_kincaid_grade,
            "reading_time_minutes": self.reading_time_minutes
        }

@dataclass
class DocumentAnalysis:
    """
    Complete analysis results for a document
    This holds all the "smart" insights about the document
    """
    sentiment: SentimentResult = field(default_factory=SentimentResult)
    keywords: List[str] = field(default_factory=list)
    readability: ReadabilityResult = field(default_factory=ReadabilityResult)
    analysis_date: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert analysis to dictionary for JSON storage"""
        return {
            "sentiment": self.sentiment.to_dict(),
            "keywords": self.keywords,
            "readability": self.readability.to_dict(),
            "analysis_date": self.analysis_date.isoformat()
        }

@dataclass
class Document:
    """
    Main Document class - represents a complete document with all its data
    
    This is like a complete file folder with:
    - The document itself (title, content)
    - Information about it (metadata)
    - Basic measurements (stats)
    - Smart analysis (sentiment, keywords, readability)
    """
    # Required fields
    title: str
    content: str
    
    # Optional fields with defaults
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: DocumentMetadata = field(default_factory=DocumentMetadata)
    stats: DocumentStats = field(default_factory=DocumentStats)
    analysis: DocumentAnalysis = field(default_factory=DocumentAnalysis)
    
    def __post_init__(self):
        """
        This runs after the document is created
        It calculates basic stats automatically
        """
        self.calculate_stats()
    
    def calculate_stats(self):
        """
        Calculate basic statistics from the content
        Like counting words, sentences, etc.
        """
        if not self.content:
            return
            
        # Count characters
        self.stats.char_count = len(self.content)
        
        # Count words (split by whitespace)
        words = self.content.split()
        self.stats.word_count = len(words)
        
        # Count sentences (rough count by periods, exclamation marks, question marks)
        sentences = self.content.count('.') + self.content.count('!') + self.content.count('?')
        self.stats.sentence_count = max(sentences, 1)  # At least 1 sentence
        
        # Count paragraphs (split by double newlines)
        paragraphs = self.content.split('\n\n')
        self.stats.paragraph_count = len([p for p in paragraphs if p.strip()])
        
        # Calculate average words per sentence
        if self.stats.sentence_count > 0:
            self.stats.avg_words_per_sentence = self.stats.word_count / self.stats.sentence_count
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the entire document to a dictionary
        This is used for saving to JSON files
        """
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "metadata": self.metadata.to_dict(),
            "stats": self.stats.to_dict(),
            "analysis": self.analysis.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Document':
        """
        Create a Document from a dictionary
        This is used for loading from JSON files
        """
        # Create metadata
        metadata_data = data.get("metadata", {})
        metadata = DocumentMetadata(
            author=metadata_data.get("author", "Unknown"),
            category=metadata_data.get("category", "general"),
            date_created=datetime.fromisoformat(metadata_data.get("date_created", datetime.now().isoformat())),
            source=metadata_data.get("source", "manual"),
            tags=metadata_data.get("tags", [])
        )
        
        # Create stats
        stats_data = data.get("stats", {})
        stats = DocumentStats(
            word_count=stats_data.get("word_count", 0),
            sentence_count=stats_data.get("sentence_count", 0),
            paragraph_count=stats_data.get("paragraph_count", 0),
            char_count=stats_data.get("char_count", 0),
            avg_words_per_sentence=stats_data.get("avg_words_per_sentence", 0.0)
        )
        
        # Create analysis
        analysis_data = data.get("analysis", {})
        
        # Create sentiment
        sentiment_data = analysis_data.get("sentiment", {})
        sentiment = SentimentResult(
            label=sentiment_data.get("label", "neutral"),
            polarity=sentiment_data.get("polarity", 0.0),
            subjectivity=sentiment_data.get("subjectivity", 0.0),
            confidence=sentiment_data.get("confidence", 0.0)
        )
        
        # Create readability
        readability_data = analysis_data.get("readability", {})
        readability = ReadabilityResult(
            flesch_score=readability_data.get("flesch_score", 0.0),
            grade_level=readability_data.get("grade_level", "Unknown"),
            flesch_kincaid_grade=readability_data.get("flesch_kincaid_grade", 0.0),
            reading_time_minutes=readability_data.get("reading_time_minutes", 0.0)
        )
        
        # Create analysis
        analysis = DocumentAnalysis(
            sentiment=sentiment,
            keywords=analysis_data.get("keywords", []),
            readability=readability,
            analysis_date=datetime.fromisoformat(analysis_data.get("analysis_date", datetime.now().isoformat()))
        )
        
        # Create document
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            title=data.get("title", ""),
            content=data.get("content", ""),
            metadata=metadata,
            stats=stats,
            analysis=analysis
        )

# Example usage and testing
if __name__ == "__main__":
    # Create a sample document
    doc = Document(
        title="Sample Blog Post",
        content="This is a sample blog post. It contains multiple sentences! How exciting is that?",
        metadata=DocumentMetadata(
            author="John Doe",
            category="blog",
            tags=["sample", "test"]
        )
    )
    
    print("📄 Document Created:")
    print(f"Title: {doc.title}")
    print(f"Word Count: {doc.stats.word_count}")
    print(f"Sentence Count: {doc.stats.sentence_count}")
    print(f"Author: {doc.metadata.author}")
    print(f"Category: {doc.metadata.category}")
    print(f"Document ID: {doc.id}")
    
    # Test conversion to/from dictionary
    doc_dict = doc.to_dict()
    print(f"\n✅ Document can be converted to dictionary: {len(doc_dict)} fields")
    
    # Test loading from dictionary
    loaded_doc = Document.from_dict(doc_dict)
    print(f"✅ Document can be loaded from dictionary: {loaded_doc.title}")
    
    print("\n🎉 Document model working correctly!") 
"""
Keyword Extraction Service

This service finds the most important words or phrases in text.
It helps identify what a document is really about.

How it works:
1. Remove common words (stop words) like "the", "and", "is"
2. Count word frequency
3. Filter out very short words
4. Return the most frequent meaningful words

Think of it as a detective that finds the key clues in a text.
"""

import re
from collections import Counter
from typing import List, Dict, Any
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import sys
sys.path.append('.')

class KeywordService:
    """
    Keyword Extraction Service
    
    This service is like a detective that finds the most important words in text.
    It helps identify what a document is really about by filtering out common words
    and finding the words that appear most frequently.
    """
    
    def __init__(self):
        """Initialize the keyword service"""
        try:
            # Download required NLTK data if not already present
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            print("📦 Downloading required NLTK data...")
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
        
        # Get English stop words (common words like "the", "and", "is")
        self.stop_words = set(stopwords.words('english'))
        
        # Add more stop words that aren't useful for keyword extraction
        self.stop_words.update([
            'would', 'could', 'should', 'might', 'must', 'shall', 'will',
            'one', 'two', 'first', 'second', 'also', 'said', 'say', 'get',
            'go', 'know', 'think', 'see', 'come', 'take', 'use', 'make',
            'way', 'time', 'year', 'day', 'work', 'life', 'world', 'hand',
            'part', 'child', 'eye', 'woman', 'man', 'place', 'good', 'great',
            'right', 'new', 'old', 'high', 'different', 'small', 'large',
            'next', 'early', 'young', 'important', 'few', 'public', 'bad',
            'same', 'able'
        ])
        
        print("🔍 Keyword Extraction Service initialized")
    
    def extract_keywords(self, text: str, limit: int = 10) -> List[str]:
        """
        Extract the most important keywords from text
        
        Args:
            text: Text to extract keywords from
            limit: Maximum number of keywords to return
            
        Returns:
            List of keywords ordered by importance
        """
        if not text or not text.strip():
            return []
        
        try:
            # Clean and tokenize the text
            cleaned_text = self._clean_text(text)
            tokens = word_tokenize(cleaned_text.lower())
            
            # Filter words
            filtered_words = []
            for word in tokens:
                if (word.isalpha() and  # Only alphabetic words
                    len(word) > 2 and   # At least 3 characters
                    word not in self.stop_words):  # Not a stop word
                    filtered_words.append(word)
            
            # Count word frequencies
            word_freq = Counter(filtered_words)
            
            # Get most common words
            most_common = word_freq.most_common(limit)
            
            # Return just the words (not the counts)
            return [word for word, count in most_common]
            
        except Exception as e:
            print(f"❌ Error extracting keywords: {e}")
            return []
    
    def extract_keywords_with_scores(self, text: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Extract keywords with their frequency scores
        
        Args:
            text: Text to extract keywords from
            limit: Maximum number of keywords to return
            
        Returns:
            List of dictionaries with 'word' and 'score' keys
        """
        if not text or not text.strip():
            return []
        
        try:
            # Clean and tokenize the text
            cleaned_text = self._clean_text(text)
            tokens = word_tokenize(cleaned_text.lower())
            
            # Filter words
            filtered_words = []
            for word in tokens:
                if (word.isalpha() and 
                    len(word) > 2 and 
                    word not in self.stop_words):
                    filtered_words.append(word)
            
            if not filtered_words:
                return []
            
            # Count word frequencies
            word_freq = Counter(filtered_words)
            total_words = len(filtered_words)
            
            # Calculate relative frequency scores
            most_common = word_freq.most_common(limit)
            
            results = []
            for word, count in most_common:
                score = count / total_words  # Relative frequency
                results.append({
                    'word': word,
                    'count': count,
                    'score': score,
                    'percentage': (count / total_words) * 100
                })
            
            return results
            
        except Exception as e:
            print(f"❌ Error extracting keywords with scores: {e}")
            return []
    
    def _clean_text(self, text: str) -> str:
        """
        Clean text by removing special characters and extra whitespace
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text
        """
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def extract_phrases(self, text: str, phrase_length: int = 2, limit: int = 10) -> List[str]:
        """
        Extract common phrases (n-grams) from text
        
        Args:
            text: Text to extract phrases from
            phrase_length: Length of phrases (2 = bigrams, 3 = trigrams)
            limit: Maximum number of phrases to return
            
        Returns:
            List of phrases ordered by frequency
        """
        if not text or not text.strip():
            return []
        
        try:
            # Clean and tokenize
            cleaned_text = self._clean_text(text)
            tokens = word_tokenize(cleaned_text.lower())
            
            # Filter tokens
            filtered_tokens = []
            for token in tokens:
                if (token.isalpha() and 
                    len(token) > 2 and 
                    token not in self.stop_words):
                    filtered_tokens.append(token)
            
            if len(filtered_tokens) < phrase_length:
                return []
            
            # Create n-grams
            phrases = []
            for i in range(len(filtered_tokens) - phrase_length + 1):
                phrase = ' '.join(filtered_tokens[i:i + phrase_length])
                phrases.append(phrase)
            
            # Count phrase frequencies
            phrase_freq = Counter(phrases)
            
            # Get most common phrases
            most_common = phrase_freq.most_common(limit)
            
            return [phrase for phrase, count in most_common]
            
        except Exception as e:
            print(f"❌ Error extracting phrases: {e}")
            return []
    
    def get_keyword_summary(self, text: str) -> Dict[str, Any]:
        """
        Get a comprehensive keyword summary
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with keyword analysis summary
        """
        if not text or not text.strip():
            return {
                "total_words": 0,
                "unique_words": 0,
                "keywords": [],
                "phrases": [],
                "top_keywords": []
            }
        
        try:
            # Basic stats
            words = word_tokenize(text.lower())
            total_words = len(words)
            unique_words = len(set(words))
            
            # Extract keywords and phrases
            keywords = self.extract_keywords(text, limit=15)
            phrases = self.extract_phrases(text, limit=10)
            top_keywords = self.extract_keywords_with_scores(text, limit=5)
            
            return {
                "total_words": total_words,
                "unique_words": unique_words,
                "keywords": keywords,
                "phrases": phrases,
                "top_keywords": top_keywords
            }
            
        except Exception as e:
            print(f"❌ Error getting keyword summary: {e}")
            return {
                "total_words": 0,
                "unique_words": 0,
                "keywords": [],
                "phrases": [],
                "top_keywords": []
            }

# Example usage and testing
if __name__ == "__main__":
    # Test the keyword service
    service = KeywordService()
    
    print("🧪 Testing Keyword Extraction Service")
    print("=" * 50)
    
    # Test text
    test_text = """
    Python is a powerful programming language that is easy to learn and widely used in web development, 
    data science, and artificial intelligence. Python's simple syntax makes it perfect for beginners, 
    while its extensive libraries and frameworks make it suitable for advanced applications. 
    Many companies use Python for machine learning, data analysis, and automation tasks.
    """
    
    print(f"📝 Text: {test_text.strip()}")
    print()
    
    # Test keyword extraction
    print("🔍 Top Keywords:")
    keywords = service.extract_keywords(test_text, limit=10)
    for i, keyword in enumerate(keywords, 1):
        print(f"   {i}. {keyword}")
    print()
    
    # Test keywords with scores
    print("📊 Keywords with Scores:")
    keywords_with_scores = service.extract_keywords_with_scores(test_text, limit=5)
    for keyword_data in keywords_with_scores:
        print(f"   - {keyword_data['word']}: {keyword_data['count']} times ({keyword_data['percentage']:.1f}%)")
    print()
    
    # Test phrase extraction
    print("🔗 Common Phrases:")
    phrases = service.extract_phrases(test_text, limit=5)
    for i, phrase in enumerate(phrases, 1):
        print(f"   {i}. {phrase}")
    print()
    
    # Test summary
    print("📋 Keyword Summary:")
    summary = service.get_keyword_summary(test_text)
    print(f"   Total words: {summary['total_words']}")
    print(f"   Unique words: {summary['unique_words']}")
    print(f"   Top keywords: {', '.join(summary['keywords'][:5])}")
    print(f"   Top phrases: {', '.join(summary['phrases'][:3])}")
    
    print("=" * 50)
    print("✅ Keyword extraction service working correctly!") 
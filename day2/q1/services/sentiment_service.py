"""
Sentiment Analysis Service

This service analyzes the emotional tone of text to determine if it's:
- Positive (happy, excited, good)
- Negative (sad, angry, bad)  
- Neutral (factual, objective)

We use TextBlob library which is simple and effective for basic sentiment analysis.

How it works:
1. TextBlob analyzes the text
2. Returns polarity (-1 to 1) and subjectivity (0 to 1)
3. We classify based on polarity: negative < 0, positive > 0, neutral = 0
"""

from textblob import TextBlob
from typing import Dict, Any
import sys
sys.path.append('.')

from models.document import SentimentResult

class SentimentService:
    """
    Sentiment Analysis Service
    
    This service is like a psychologist that can read emotions in text.
    It tells us whether a piece of text has a positive, negative, or neutral tone.
    """
    
    def __init__(self):
        """Initialize the sentiment service"""
        self.threshold = 0.1  # Minimum polarity to be considered positive/negative
        print("🧠 Sentiment Analysis Service initialized")
    
    def analyze_sentiment(self, text: str) -> SentimentResult:
        """
        Analyze sentiment of text
        
        Args:
            text: Text to analyze
            
        Returns:
            SentimentResult with label, polarity, subjectivity, and confidence
        """
        if not text or not text.strip():
            return SentimentResult(
                label="neutral",
                polarity=0.0,
                subjectivity=0.0,
                confidence=0.0
            )
        
        try:
            # Use TextBlob to analyze the text
            blob = TextBlob(text)
            
            # Get polarity (-1 to 1) and subjectivity (0 to 1)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Determine sentiment label
            if polarity > self.threshold:
                label = "positive"
            elif polarity < -self.threshold:
                label = "negative"
            else:
                label = "neutral"
            
            # Calculate confidence based on how far from neutral
            confidence = abs(polarity)
            
            return SentimentResult(
                label=label,
                polarity=polarity,
                subjectivity=subjectivity,
                confidence=confidence
            )
            
        except Exception as e:
            print(f"❌ Error analyzing sentiment: {e}")
            return SentimentResult(
                label="neutral",
                polarity=0.0,
                subjectivity=0.0,
                confidence=0.0
            )
    
    def get_sentiment_explanation(self, sentiment_result: SentimentResult) -> str:
        """
        Get a human-readable explanation of the sentiment result
        
        Args:
            sentiment_result: SentimentResult to explain
            
        Returns:
            Human-readable explanation
        """
        label = sentiment_result.label
        polarity = sentiment_result.polarity
        subjectivity = sentiment_result.subjectivity
        confidence = sentiment_result.confidence
        
        explanation = f"The text is {label}"
        
        # Add intensity description
        if label == "positive":
            if polarity > 0.5:
                explanation += " (very positive)"
            elif polarity > 0.2:
                explanation += " (moderately positive)"
            else:
                explanation += " (slightly positive)"
        elif label == "negative":
            if polarity < -0.5:
                explanation += " (very negative)"
            elif polarity < -0.2:
                explanation += " (moderately negative)"
            else:
                explanation += " (slightly negative)"
        
        # Add subjectivity description
        if subjectivity > 0.7:
            explanation += " and highly subjective (opinion-based)"
        elif subjectivity > 0.3:
            explanation += " and moderately subjective"
        else:
            explanation += " and objective (fact-based)"
        
        # Add confidence description
        if confidence > 0.7:
            explanation += " with high confidence"
        elif confidence > 0.3:
            explanation += " with moderate confidence"
        else:
            explanation += " with low confidence"
        
        return explanation
    
    def batch_analyze(self, texts: list) -> list:
        """
        Analyze sentiment for multiple texts
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            List of SentimentResult objects
        """
        results = []
        for text in texts:
            result = self.analyze_sentiment(text)
            results.append(result)
        return results
    
    def get_sentiment_summary(self, texts: list) -> Dict[str, Any]:
        """
        Get a summary of sentiment for multiple texts
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            Dictionary with sentiment summary statistics
        """
        if not texts:
            return {
                "total_texts": 0,
                "positive": 0,
                "negative": 0,
                "neutral": 0,
                "avg_polarity": 0.0,
                "avg_subjectivity": 0.0
            }
        
        results = self.batch_analyze(texts)
        
        # Count sentiment labels
        positive_count = sum(1 for r in results if r.label == "positive")
        negative_count = sum(1 for r in results if r.label == "negative")
        neutral_count = sum(1 for r in results if r.label == "neutral")
        
        # Calculate averages
        avg_polarity = sum(r.polarity for r in results) / len(results)
        avg_subjectivity = sum(r.subjectivity for r in results) / len(results)
        
        return {
            "total_texts": len(texts),
            "positive": positive_count,
            "negative": negative_count,
            "neutral": neutral_count,
            "avg_polarity": avg_polarity,
            "avg_subjectivity": avg_subjectivity,
            "positive_percentage": (positive_count / len(texts)) * 100,
            "negative_percentage": (negative_count / len(texts)) * 100,
            "neutral_percentage": (neutral_count / len(texts)) * 100
        }

# Example usage and testing
if __name__ == "__main__":
    # Test the sentiment service
    service = SentimentService()
    
    print("🧪 Testing Sentiment Analysis Service")
    print("=" * 50)
    
    # Test different types of text
    test_texts = [
        "I love this product! It's amazing and works perfectly!",
        "This is terrible. I hate it and want my money back.",
        "The weather is sunny today.",
        "This is a technical document about machine learning algorithms.",
        "I'm so excited about this new opportunity!",
        "The service was disappointing and slow."
    ]
    
    for i, text in enumerate(test_texts, 1):
        result = service.analyze_sentiment(text)
        explanation = service.get_sentiment_explanation(result)
        
        print(f"{i}. Text: \"{text}\"")
        print(f"   Result: {result.label} (polarity: {result.polarity:.2f})")
        print(f"   Explanation: {explanation}")
        print()
    
    # Test batch analysis
    print("📊 Batch Analysis Summary:")
    summary = service.get_sentiment_summary(test_texts)
    print(f"   Total texts: {summary['total_texts']}")
    print(f"   Positive: {summary['positive']} ({summary['positive_percentage']:.1f}%)")
    print(f"   Negative: {summary['negative']} ({summary['negative_percentage']:.1f}%)")
    print(f"   Neutral: {summary['neutral']} ({summary['neutral_percentage']:.1f}%)")
    print(f"   Average polarity: {summary['avg_polarity']:.2f}")
    print(f"   Average subjectivity: {summary['avg_subjectivity']:.2f}")
    
    print("=" * 50)
    print("✅ Sentiment analysis service working correctly!") 
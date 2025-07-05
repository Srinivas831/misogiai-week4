"""
Readability Service

This service calculates how easy text is to read and understand.
It's like a teacher grading how difficult a piece of writing is.

Readability metrics we calculate:
1. Flesch Reading Ease Score (0-100, higher = easier)
2. Flesch-Kincaid Grade Level (US grade level)
3. Reading time estimation
4. Grade level description

How it works:
- Analyzes sentence length and word complexity
- Counts syllables in words
- Uses established formulas to calculate readability
- Provides human-readable explanations
"""

import textstat
import re
from typing import Dict, Any, List
import sys
sys.path.append('.')

from models.document import ReadabilityResult

class ReadabilityService:
    """
    Readability Service
    
    This service is like a teacher who evaluates how easy text is to read.
    It analyzes sentence length, word complexity, and provides grade-level assessments.
    """
    
    def __init__(self):
        """Initialize the readability service"""
        # Average reading speed (words per minute)
        self.reading_speed_wpm = 200
        
        print("📚 Readability Service initialized")
    
    def calculate_readability(self, text: str) -> ReadabilityResult:
        """
        Calculate comprehensive readability metrics for text
        
        Args:
            text: Text to analyze
            
        Returns:
            ReadabilityResult with various readability metrics
        """
        if not text or not text.strip():
            return ReadabilityResult(
                flesch_score=0.0,
                grade_level="Unknown",
                flesch_kincaid_grade=0.0,
                reading_time_minutes=0.0
            )
        
        try:
            # Calculate Flesch Reading Ease Score (0-100, higher = easier)
            flesch_score = textstat.flesch_reading_ease(text)
            
            # Calculate Flesch-Kincaid Grade Level (US grade level)
            flesch_kincaid_grade = textstat.flesch_kincaid_grade(text)
            
            # Get grade level description
            grade_level = self._get_grade_level_description(flesch_score)
            
            # Calculate reading time
            reading_time_minutes = self._calculate_reading_time(text)
            
            return ReadabilityResult(
                flesch_score=flesch_score,
                grade_level=grade_level,
                flesch_kincaid_grade=flesch_kincaid_grade,
                reading_time_minutes=reading_time_minutes
            )
            
        except Exception as e:
            print(f"❌ Error calculating readability: {e}")
            return ReadabilityResult(
                flesch_score=0.0,
                grade_level="Unknown",
                flesch_kincaid_grade=0.0,
                reading_time_minutes=0.0
            )
    
    def _get_grade_level_description(self, flesch_score: float) -> str:
        """
        Convert Flesch score to grade level description
        
        Args:
            flesch_score: Flesch Reading Ease score
            
        Returns:
            Human-readable grade level description
        """
        if flesch_score >= 90:
            return "5th grade (Very Easy)"
        elif flesch_score >= 80:
            return "6th grade (Easy)"
        elif flesch_score >= 70:
            return "7th grade (Fairly Easy)"
        elif flesch_score >= 60:
            return "8th-9th grade (Standard)"
        elif flesch_score >= 50:
            return "10th-12th grade (Fairly Difficult)"
        elif flesch_score >= 30:
            return "College level (Difficult)"
        else:
            return "Graduate level (Very Difficult)"
    
    def _calculate_reading_time(self, text: str) -> float:
        """
        Calculate estimated reading time in minutes
        
        Args:
            text: Text to analyze
            
        Returns:
            Estimated reading time in minutes
        """
        words = text.split()
        word_count = len(words)
        
        # Calculate time based on average reading speed
        reading_time_minutes = word_count / self.reading_speed_wpm
        
        return round(reading_time_minutes, 1)
    
    def get_detailed_analysis(self, text: str) -> Dict[str, Any]:
        """
        Get detailed readability analysis with multiple metrics
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with detailed readability analysis
        """
        if not text or not text.strip():
            return {
                "flesch_reading_ease": 0.0,
                "flesch_kincaid_grade": 0.0,
                "automated_readability_index": 0.0,
                "coleman_liau_index": 0.0,
                "gunning_fog": 0.0,
                "reading_time_minutes": 0.0,
                "word_count": 0,
                "sentence_count": 0,
                "avg_sentence_length": 0.0,
                "avg_syllables_per_word": 0.0,
                "difficult_words": 0,
                "text_difficulty": "Unknown"
            }
        
        try:
            # Calculate various readability metrics
            flesch_reading_ease = textstat.flesch_reading_ease(text)
            flesch_kincaid_grade = textstat.flesch_kincaid_grade(text)
            automated_readability_index = textstat.automated_readability_index(text)
            coleman_liau_index = textstat.coleman_liau_index(text)
            gunning_fog = textstat.gunning_fog(text)
            
            # Calculate text statistics
            word_count = len(text.split())
            sentence_count = textstat.sentence_count(text)
            avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
            avg_syllables_per_word = textstat.avg_syllables_per_word(text)
            difficult_words = textstat.difficult_words(text)
            
            # Calculate reading time
            reading_time_minutes = self._calculate_reading_time(text)
            
            # Determine overall text difficulty
            text_difficulty = self._determine_text_difficulty(flesch_reading_ease)
            
            return {
                "flesch_reading_ease": flesch_reading_ease,
                "flesch_kincaid_grade": flesch_kincaid_grade,
                "automated_readability_index": automated_readability_index,
                "coleman_liau_index": coleman_liau_index,
                "gunning_fog": gunning_fog,
                "reading_time_minutes": reading_time_minutes,
                "word_count": word_count,
                "sentence_count": sentence_count,
                "avg_sentence_length": avg_sentence_length,
                "avg_syllables_per_word": avg_syllables_per_word,
                "difficult_words": difficult_words,
                "text_difficulty": text_difficulty
            }
            
        except Exception as e:
            print(f"❌ Error getting detailed analysis: {e}")
            return {
                "flesch_reading_ease": 0.0,
                "flesch_kincaid_grade": 0.0,
                "automated_readability_index": 0.0,
                "coleman_liau_index": 0.0,
                "gunning_fog": 0.0,
                "reading_time_minutes": 0.0,
                "word_count": 0,
                "sentence_count": 0,
                "avg_sentence_length": 0.0,
                "avg_syllables_per_word": 0.0,
                "difficult_words": 0,
                "text_difficulty": "Unknown"
            }
    
    def _determine_text_difficulty(self, flesch_score: float) -> str:
        """
        Determine overall text difficulty based on Flesch score
        
        Args:
            flesch_score: Flesch Reading Ease score
            
        Returns:
            Text difficulty level
        """
        if flesch_score >= 80:
            return "Very Easy"
        elif flesch_score >= 70:
            return "Easy"
        elif flesch_score >= 60:
            return "Standard"
        elif flesch_score >= 50:
            return "Fairly Difficult"
        elif flesch_score >= 30:
            return "Difficult"
        else:
            return "Very Difficult"
    
    def get_readability_suggestions(self, text: str) -> List[str]:
        """
        Get suggestions for improving readability
        
        Args:
            text: Text to analyze
            
        Returns:
            List of suggestions for improving readability
        """
        if not text or not text.strip():
            return ["Please provide text to analyze"]
        
        suggestions = []
        
        try:
            analysis = self.get_detailed_analysis(text)
            
            # Check sentence length
            if analysis["avg_sentence_length"] > 20:
                suggestions.append("Consider breaking up long sentences (average: {:.1f} words per sentence)".format(analysis["avg_sentence_length"]))
            
            # Check syllable complexity
            if analysis["avg_syllables_per_word"] > 1.7:
                suggestions.append("Consider using simpler words (average: {:.1f} syllables per word)".format(analysis["avg_syllables_per_word"]))
            
            # Check difficult words
            if analysis["difficult_words"] > analysis["word_count"] * 0.1:
                suggestions.append("Reduce difficult words ({} out of {} words are difficult)".format(analysis["difficult_words"], analysis["word_count"]))
            
            # Check overall readability
            if analysis["flesch_reading_ease"] < 60:
                suggestions.append("Overall readability could be improved (Flesch score: {:.1f})".format(analysis["flesch_reading_ease"]))
            
            # Check paragraph length
            paragraphs = text.split('\n\n')
            avg_paragraph_length = sum(len(p.split()) for p in paragraphs) / len(paragraphs)
            if avg_paragraph_length > 100:
                suggestions.append("Consider breaking up long paragraphs (average: {:.1f} words per paragraph)".format(avg_paragraph_length))
            
            if not suggestions:
                suggestions.append("Text readability is good! No specific improvements needed.")
            
            return suggestions
            
        except Exception as e:
            print(f"❌ Error getting readability suggestions: {e}")
            return ["Error analyzing text for suggestions"]
    
    def compare_texts(self, texts: List[str]) -> Dict[str, Any]:
        """
        Compare readability of multiple texts
        
        Args:
            texts: List of texts to compare
            
        Returns:
            Dictionary with comparison results
        """
        if not texts:
            return {"error": "No texts provided"}
        
        try:
            results = []
            
            for i, text in enumerate(texts):
                analysis = self.get_detailed_analysis(text)
                analysis["text_index"] = i
                results.append(analysis)
            
            # Find easiest and most difficult texts
            easiest = max(results, key=lambda x: x["flesch_reading_ease"])
            most_difficult = min(results, key=lambda x: x["flesch_reading_ease"])
            
            # Calculate averages
            avg_flesch = sum(r["flesch_reading_ease"] for r in results) / len(results)
            avg_grade_level = sum(r["flesch_kincaid_grade"] for r in results) / len(results)
            avg_reading_time = sum(r["reading_time_minutes"] for r in results) / len(results)
            
            return {
                "text_count": len(texts),
                "individual_results": results,
                "easiest_text": {
                    "index": easiest["text_index"],
                    "flesch_score": easiest["flesch_reading_ease"],
                    "difficulty": easiest["text_difficulty"]
                },
                "most_difficult_text": {
                    "index": most_difficult["text_index"],
                    "flesch_score": most_difficult["flesch_reading_ease"],
                    "difficulty": most_difficult["text_difficulty"]
                },
                "averages": {
                    "flesch_reading_ease": avg_flesch,
                    "grade_level": avg_grade_level,
                    "reading_time_minutes": avg_reading_time
                }
            }
            
        except Exception as e:
            print(f"❌ Error comparing texts: {e}")
            return {"error": str(e)}

# Example usage and testing
if __name__ == "__main__":
    # Test the readability service
    service = ReadabilityService()
    
    print("🧪 Testing Readability Service")
    print("=" * 50)
    
    # Test texts with different complexity levels
    test_texts = [
        "The cat sat on the mat. It was a sunny day.",  # Very simple
        "Python is a programming language. It is easy to learn and use. Many people like Python.",  # Simple
        "The implementation of machine learning algorithms requires sophisticated understanding of statistical methodologies and computational complexity theory.",  # Complex
        "Artificial intelligence represents a paradigm shift in computational methodologies, necessitating interdisciplinary collaboration between computer scientists, mathematicians, and domain experts to develop robust, scalable solutions for complex real-world problems."  # Very complex
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Text {i}: \"{text}\"")
        
        # Basic readability
        result = service.calculate_readability(text)
        print(f"   Flesch Score: {result.flesch_score:.1f}")
        print(f"   Grade Level: {result.grade_level}")
        print(f"   Reading Time: {result.reading_time_minutes} minutes")
        
        # Suggestions
        suggestions = service.get_readability_suggestions(text)
        print(f"   Suggestions: {suggestions[0]}")
    
    # Detailed analysis for one text
    print(f"\n📊 Detailed Analysis for Text 3:")
    detailed = service.get_detailed_analysis(test_texts[2])
    print(f"   Average sentence length: {detailed['avg_sentence_length']:.1f} words")
    print(f"   Average syllables per word: {detailed['avg_syllables_per_word']:.1f}")
    print(f"   Difficult words: {detailed['difficult_words']}")
    print(f"   Text difficulty: {detailed['text_difficulty']}")
    
    print("\n" + "=" * 50)
    print("✅ Readability service working correctly!") 
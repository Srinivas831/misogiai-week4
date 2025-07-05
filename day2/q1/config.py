"""
Configuration File

This file stores settings for our Document Analyzer.
Think of it like the settings menu in a video game - you can adjust how things work.

Why do we use a config file?
- Easy to change settings without editing code
- Different settings for development vs production
- All settings in one place
"""

import os
from pathlib import Path

# Base directory - where our project files are located
BASE_DIR = Path(__file__).parent

# Storage settings - where we save our documents
STORAGE_DIR = BASE_DIR / "storage"
DOCUMENTS_FILE = STORAGE_DIR / "documents.json"

# Analysis settings - how our text analysis works
ANALYSIS_SETTINGS = {
    "default_keyword_limit": 10,        # How many keywords to extract by default
    "min_word_count": 10,              # Minimum words needed for analysis
    "sentiment_threshold": 0.1,         # How sensitive sentiment detection is
}

# MCP Server settings
MCP_SERVER_CONFIG = {
    "name": "document-analyzer",
    "version": "1.0.0",
    "description": "Analyzes documents for sentiment, keywords, and readability"
}

# Sample document categories - types of documents we'll create
DOCUMENT_CATEGORIES = [
    "news",
    "blog", 
    "technical",
    "creative",
    "academic",
    "review",
    "social_media"
]

print(f"Configuration loaded from: {BASE_DIR}")
print(f"Documents will be stored in: {DOCUMENTS_FILE}") 
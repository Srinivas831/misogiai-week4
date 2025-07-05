"""
Simple Storage Viewer
"""

import json
import sys
sys.path.append('.')

def view_storage():
    """View the contents of the storage file"""
    
    try:
        with open('storage/documents.json', 'r') as f:
            data = json.load(f)
        
        print("📁 Storage File Contents")
        print("=" * 40)
        
        metadata = data.get("metadata", {})
        print(f"📊 Total Documents: {metadata.get('total_documents', 0)}")
        print(f"📅 Last Updated: {metadata.get('last_updated', 'Unknown')}")
        print()
        
        print("📋 Documents:")
        for i, doc in enumerate(data.get("documents", []), 1):
            print(f"{i}. {doc['title']}")
            print(f"   Author: {doc['metadata']['author']}")
            print(f"   Category: {doc['metadata']['category']}")
            print(f"   Words: {doc['stats']['word_count']}")
            print(f"   ID: {doc['id'][:8]}...")
            print()
        
        print("=" * 40)
        print("✅ Storage file loaded successfully!")
        
    except FileNotFoundError:
        print("❌ Storage file not found")
    except json.JSONDecodeError:
        print("❌ Invalid JSON in storage file")

if __name__ == "__main__":
    view_storage() 
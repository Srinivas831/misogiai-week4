"""
Test Setup Script

This script tests if our basic setup is working.
We'll run this to make sure everything is properly configured.
"""

import sys
import os
from pathlib import Path

def test_basic_setup():
    """Test if our basic project structure is working"""
    
    print("🧪 Testing Document Analyzer Setup...")
    print("=" * 50)
    
    # Test 1: Check if we can import our config
    try:
        import config
        print("✅ Config file imported successfully")
        print(f"   - Base directory: {config.BASE_DIR}")
        print(f"   - Storage directory: {config.STORAGE_DIR}")
    except ImportError as e:
        print(f"❌ Could not import config: {e}")
        return False
    
    # Test 2: Check if directories exist
    try:
        models_dir = Path("models")
        services_dir = Path("services")
        storage_dir = Path("storage")
        
        print(f"✅ Project structure:")
        print(f"   - models/ exists: {models_dir.exists()}")
        print(f"   - services/ exists: {services_dir.exists()}")
        print(f"   - storage/ exists: {storage_dir.exists()}")
    except Exception as e:
        print(f"❌ Error checking directories: {e}")
        return False
    
    # Test 3: Check Python version
    python_version = sys.version_info
    print(f"✅ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("⚠️  Warning: Python 3.8+ is recommended")
    
    print("=" * 50)
    print("🎉 Basic setup test completed!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Create the document models")
    print("3. Build the analysis services")
    
    return True

if __name__ == "__main__":
    test_basic_setup() 
# Document Analyzer MCP Server

## What is this?

This is a **Document Analyzer** that uses **MCP (Model Context Protocol)** to let AI assistants analyze text documents.

### Simple Explanation:
- **MCP** = A way for AI assistants to use external tools
- **Our tool** = Analyzes documents for sentiment, keywords, and readability
- **AI assistants** = Can call our tool to analyze any document

Think of it like a smart assistant that can:
- Tell you if a document is positive, negative, or neutral
- Find the most important words in a document
- Tell you how easy or hard a document is to read

## What We've Built So Far

### Project Structure:
```
day2/q1/
├── main.py              # Main server file (the waiter)
├── config.py            # Settings and configuration
├── requirements.txt     # List of Python packages we need
├── README.md           # This file!
├── models/             # Data blueprints
│   └── __init__.py
├── services/           # Business logic (the kitchen)
│   └── __init__.py
└── storage/            # Data storage (the filing cabinet)
    └── __init__.py
```

## Next Steps

1. **Install Dependencies** - Get the Python packages we need
2. **Create Models** - Define what documents and analysis results look like
3. **Build Services** - Create the actual analysis functions
4. **Create MCP Tools** - Make the tools that AI assistants can call
5. **Add Sample Documents** - Create 15+ test documents
6. **Test Everything** - Make sure it all works!

## How to Run (Once Complete)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

## Learning Notes

- **MCP** = Model Context Protocol (how AI assistants talk to external tools)
- **NLP** = Natural Language Processing (how computers understand human language)
- **Sentiment Analysis** = Determining if text is positive, negative, or neutral
- **Keywords** = The most important words in a document
- **Readability** = How easy text is to read and understand 
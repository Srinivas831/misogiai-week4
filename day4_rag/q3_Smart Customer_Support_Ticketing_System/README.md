# Smart Customer Support Ticketing System with RAG

A Retrieval-Augmented Generation (RAG) system that provides intelligent customer support responses by combining web scraping, vector search, and Large Language Models (LLMs).

## 🚀 Features

- **Intelligent Query Classification**: Automatically categorizes customer queries into support categories
- **Web Content Scraping**: Extracts support information from company websites
- **Vector Search**: Uses FAISS for efficient similarity search across support documents
- **Context-Aware Responses**: Generates accurate answers using retrieved relevant documents
- **Category-Based Filtering**: Searches within specific support categories for better relevance

## 📋 System Architecture

```
User Query → Query Classification → Document Retrieval → Answer Generation
     ↓              ↓                      ↓                    ↓
  Input Text    LLM Classifier      FAISS Vector DB      LLM with Context
```

### Components:

1. **Web Scraper**: Extracts support content from websites
2. **Document Database**: SQLite database for storing scraped content
3. **Vector Store**: FAISS for efficient similarity search
4. **Query Classifier**: LLM-based category classification
5. **Answer Generator**: Context-aware response generation

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- OpenAI API key

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd day4_rag/q3_Smart Customer_Support_Ticketing_System
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the backend directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 📁 Project Structure

```
backend/
├── db/
│   ├── document_db.py          # Database models and operations
│   ├── insert_document.py      # Document insertion utilities
│   └── fetch_unvectorized.py   # Fetch unprocessed documents
├── loaders/
│   └── web_loader.py           # Web scraping functionality
├── vectorstore/
│   └── vectorizer.py           # Document vectorization logic
├── data/
│   └── documents.db            # SQLite database
├── faiss_vectorstore/          # FAISS vector database files
├── test_web_scrape.py          # Web scraping script
├── test_vectorize.py           # Vectorization script
├── test_query.py               # Main query processing script
└── .env                        # Environment variables
```

## 🚀 Usage

### 1. Scrape Support Content

First, scrape support content from websites:

```bash
python test_web_scrape.py
```

This will:
- Scrape content from predefined support URLs
- Store documents in SQLite database
- Categorize content (Returns, Shipping, Warranty, Payments)

### 2. Vectorize Documents

Convert documents to vector embeddings:

```bash
python test_vectorize.py
```

This will:
- Process unvectorized documents from the database
- Split documents into chunks
- Create embeddings using OpenAI
- Store in FAISS vector database

### 3. Query the System

Run the main query interface:

```bash
python test_query.py
```

Example interaction:
```
Enter your query: What happens if I have received a defective item?
Predicted category: Warranty

Top 3 matching chunks:
1. [Category: Warranty]
The Apple Limited Warranty covers manufacturing defects...

============================================================
FINAL ANSWER:
============================================================
If you've received a defective item, you're covered under the Apple Limited 
Warranty for manufacturing defects. You can get service including replacement 
parts for 90 days or the remaining warranty term, whichever is longer...
============================================================
```

## 🔧 Configuration

### Support Categories

The system supports these categories:
- **FAQ**: General frequently asked questions
- **Returns**: Product return and refund policies
- **Shipping**: Delivery and shipping information
- **Warranty**: Product warranty and repair services
- **Payments**: Payment and billing issues

### Web Sources

Default sources (can be modified in `test_web_scrape.py`):
- Apple iPhone Support: https://support.apple.com/en-in/iphone
- Returns & Refunds: https://www.apple.com/in/shop/help/returns_refund
- Shipping: https://www.apple.com/in/shop/help/shipping_delivery
- Warranty: https://support.apple.com/en-in/iphone/repair/service
- Payments: https://support.apple.com/en-in/billing

## 🧪 Testing

### Test Individual Components

1. **Test Database Connection**
   ```bash
   python -c "from db.document_db import SessionLocal; print('Database connected successfully')"
   ```

2. **Test Web Scraping**
   ```bash
   python test_web_scrape.py
   ```

3. **Test Vectorization**
   ```bash
   python test_vectorize.py
   ```

4. **Test Query Processing**
   ```bash
   python test_query.py
   ```

## 📊 Database Schema

### Document Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| source | String | Source URL of the document |
| content | Text | Full text content |
| category | String | Support category (Returns, Shipping, etc.) |
| is_vectorized | Boolean | Whether document is processed for vector search |

## 🔍 How It Works

### 1. Data Ingestion
- Web scraper extracts content from support websites
- Content is cleaned and stored in SQLite database
- Each document is tagged with a category

### 2. Vectorization
- Documents are split into chunks (500 characters with 50 overlap)
- Each chunk is converted to embeddings using OpenAI's text-embedding-3-small
- Embeddings are stored in FAISS vector database with metadata

### 3. Query Processing
- User query is classified into a support category using GPT-4
- Relevant chunks are retrieved using semantic similarity search
- Results are filtered by predicted category for better relevance

### 4. Answer Generation
- Retrieved chunks are combined as context
- GPT-4 generates a comprehensive answer using the context
- Response maintains professional customer support tone

## 🛡️ Error Handling

The system includes error handling for:
- Database connection issues
- Web scraping failures
- Vector store loading errors
- API rate limits and failures
- Invalid user inputs

## 🔮 Future Enhancements

- [ ] Add support for multiple languages
- [ ] Implement conversation history
- [ ] Add confidence scoring for answers
- [ ] Create web interface
- [ ] Add support for file uploads (PDFs, docs)
- [ ] Implement feedback loop for answer quality
- [ ] Add analytics and usage tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section below
2. Create an issue on GitHub
3. Contact the development team

## 🔧 Troubleshooting

### Common Issues

**1. "No documents found in vectorstore"**
- Run `python test_vectorize.py` to create/update the vector store
- Ensure documents exist in the database

**2. "OpenAI API key not found"**
- Check your `.env` file contains `OPENAI_API_KEY=`
- Ensure the `.env` file is in the backend directory

**3. "No matching chunks found"**
- Try broader search terms
- Check if documents are properly categorized
- Verify vector store contains relevant content

**4. "Database connection error"**
- Ensure the `data/` directory exists
- Check file permissions for SQLite database

### Performance Tips

- Use specific queries for better results
- Categories help narrow down search scope
- Regularly update and refresh scraped content
- Monitor OpenAI API usage and costs

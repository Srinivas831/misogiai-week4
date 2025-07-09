# 🤖 HR Onboarding Knowledge Assistant (Manual RAG)

This project replaces time-consuming HR onboarding calls with an AI assistant that can instantly answer employee questions about policies, leave, benefits, and more — directly from uploaded HR documents.

We manually implemented the entire Retrieval-Augmented Generation (RAG) pipeline using:
- Flask for backend API
- OpenAI for embeddings and GPT responses
- FAISS for vector storage
- No LangChain — full control and clarity

---

## 📦 Features

- Upload HR documents (PDF, DOCX, TXT)
- Extract text and chunk it intelligently
- Convert chunks to vector embeddings
- Store vectors in FAISS (in-memory vector DB)
- Accept natural language questions from users
- Retrieve relevant chunks based on query similarity
- Send context + question to GPT model for accurate answers
- Return the AI-generated response

---

## 📂 Project Structure

```
hr_rag_manual/
├── app.py                  # Main Flask backend
├── documents/              # Uploaded documents (PDFs, DOCX)
├── .env                    # Environment variables (API key)
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🧪 Dependencies

Install all required packages:

```bash
pip install flask openai faiss-cpu python-dotenv python-docx PyMuPDF
```

---

## 🔐 .env File

Create a `.env` file in the root directory:

```
OPENAI_API_KEY=""
```

---

## 🚀 Manual RAG Pipeline Flow

### 🔹 Step 1: Upload HR Document

- Endpoint: `POST /upload`
- Use Postman → form-data → key=`files`, value=`(select file)`
- Accepted file formats: `.pdf`, `.docx`, `.txt`
- The file is saved into `/documents`

### 🔹 Step 2: Extract Text

- PDF: Extracted with PyMuPDF (`fitz`)
- DOCX: Extracted with `python-docx`
- TXT: Read using basic `open()` call

### 🔹 Step 3: Chunk the Text

Text is split into overlapping chunks:

```python
def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks
```

### 🔹 Step 4: Generate Embeddings

Each chunk is converted to a 1536D embedding using OpenAI API:

```python
response = openai.embeddings.create(input=chunk, model="text-embedding-3-small")
embedding = response.data[0].embedding
```

These embeddings are stored in a list.

### 🔹 Step 5: Store in FAISS

```python
dimension = len(embeddings[0])  # 1536
index = faiss.IndexFlatL2(dimension)
vectors = np.array(embeddings).astype("float32")
index.add(vectors)
```

FAISS holds the embeddings in memory, allowing fast similarity search.

We also store `chunk_metadata = chunks` for later retrieval.

---

## ❓ Querying the Assistant

### Endpoint: `POST /query`

**JSON Body:**

```json
{
  "question": "What is the process for applying for parental leave?"
}
```

### Backend Steps:

1. Embed the question using OpenAI
2. Perform vector similarity search in FAISS
3. Retrieve top-k relevant chunks
4. Build a prompt with context + question
5. Send to OpenAI Chat model
6. Return the answer to the user

### Example Prompt Sent to GPT:

```
You are an HR assistant. Use the following company policy context to answer the employee's question.

Context:
<retrieved_chunk_1>
---
<retrieved_chunk_2>
---
<retrieved_chunk_3>

Question: What is the process for applying for parental leave?

Answer:
```

---

## ✅ Current Limitations

- FAISS index is not persisted to disk (restarts lose data)
- Chunking is fixed-length, not semantic
- No metadata filtering
- GPT may hallucinate if retrieved chunks are irrelevant

---

## 🚧 Future Improvements

- Save/load FAISS index using `faiss.write_index()` / `read_index()`
- Add document metadata (filename, section) per chunk
- Use semantic or recursive chunking (NLTK, spaCy)
- Add LangChain/LangGraph later for orchestration
- Frontend dashboard for HR to upload/query docs
- Auth roles for HR/admin vs employees

---

## 🏁 Conclusion

You now have a fully working Retrieval-Augmented Generation (RAG) system built completely from scratch:

- ✅ No LangChain
- ✅ End-to-end pipeline
- ✅ Local testing with OpenAI and FAISS

This is how real-world knowledge assistants are built — by understanding every layer. You’re ready to scale it up, productionize it, or plug it into any frontend or chatbot.

---

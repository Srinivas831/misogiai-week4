from flask import Flask, request, jsonify
import os
import uuid

import fitz  # PyMuPDF for PDFs
import docx  # python-docx for Word files

import openai
import faiss
import numpy as np
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


app= Flask(__name__)

# Set the folder where uploaded files will be saved
UPLOAD_FOLDER = "documents"
ALLOWED_EXTENSIONS= {"pdf", "docx"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Check file extension
def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(filepath):
    text = ""
    with fitz.open(filepath) as pdf:
        print("Number of pages:", len(pdf))
        for page in pdf:
            text += page.get_text()
            print("Page", page.number, "extracted")
    return text

def extract_text_from_docx(filepath):
    doc = docx.Document(filepath)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text


def extract_text_from_file(filepath):
    ext = filepath.rsplit('.', 1)[1].lower()
    print("File extension:", ext)
    if ext == 'pdf':
        return extract_text_from_pdf(filepath)
    elif ext == 'docx':
        return extract_text_from_docx(filepath)
    elif ext == 'txt':
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return ""

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    print("Chunking text...",len(text))
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap  # slide forward with overlap
    return chunks

def get_embeddings_for_chunks(chunks):
    embeddings = []

    for i, chunk in enumerate(chunks):
        response = openai.embeddings.create(
            input=chunk,
            model="text-embedding-3-small"
        )

        # if i == 0:
        #     print("First embedding response:", response)
        
        # ✅ FIXED HERE
        embedding = response.data[0].embedding

        embeddings.append(embedding)

    return embeddings


def store_in_faiss(embeddings, chunks):
    dimension = len(embeddings[0])  # should be 1536
    index = faiss.IndexFlatL2(dimension)

    # Convert to numpy array
    vectors = np.array(embeddings).astype('float32')

    # Add vectors to FAISS index
    index.add(vectors)

    # Store chunks as metadata
    return index, chunks


faiss_index = None
chunk_metadata = []


@app.route("/upload", methods=["POST"])
def upload_file():
    print("Upload route hit", request)
    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400
    
    file = request.files["file"] 
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and is_allowed_file(file.filename):
        # Create a unique filename to avoid collisions
        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_name = f"{uuid.uuid4()}.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_name)

        # Save the file
        file.save(filepath)
        print("File saved to:", filepath)
        text = extract_text_from_file(filepath)
        print("Extracted text length:", len(text))

        chunks = chunk_text(text)
        print(f"Total Chunks: {len(chunks)}")
        # print(f" ///////Full chunk:////////",  chunks[0])

        embeddings = get_embeddings_for_chunks(chunks)
        # print("Embeddings created", embeddings)

        global faiss_index, chunk_metadata
        faiss_index, chunk_metadata = store_in_faiss(embeddings, chunks)

        print("Stored in FAISS", faiss_index)
        # print("Chunk metadata", chunk_metadata)

        return jsonify({"message": "File uploaded successfully", "filename": unique_name, "text": text, "chunks": chunks}), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400




@app.route("/query", methods=["POST"])
def query_knowledge_base():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    # 1. Embed the question
    question_embedding_response = openai.embeddings.create(
        input=question,
        model="text-embedding-3-small"
    )
    query_vector = np.array([question_embedding_response.data[0].embedding]).astype("float32")

    # 2. Search FAISS for top-k
    k = 3
    D, I = faiss_index.search(query_vector, k)
    print("FAISS search results:", D, "//////I", I)
    retrieved_chunks = [chunk_metadata[i] for i in I[0]]

    # 3. Build prompt
    context = "\n---\n".join(retrieved_chunks)
    prompt = f"""
You are an assistant. Use the following context to answer the question.

Context:{context}

Question: {question}

Answer:"""

    # 4. Send to OpenAI
    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    answer = completion.choices[0].message.content.strip()

    # 5. Return result
    return jsonify({
        "question": question,
        "answer": answer,
        "context_chunks": retrieved_chunks
    })


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

    
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils.laoder import load_documents
from utils.splitter import split_documents
from utils.rag_pipeline import embed_and_store, query_with_context


app= Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "documents"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=['POST'])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error":"No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error":"No selected files"}), 400
    
    ext = file.filename.split(".")[-1].lower()
    print("ext",ext)
    if ext not in ["pdf", "docx", "txt"]:
        return jsonify({"error":"Unsupported file type"}), 400
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    print("filepath",filepath)
    file.save(filepath)

    try:
        doc = load_documents(filepath)
        chunks = split_documents(doc)

        vectorStore = embed_and_store(chunks)
        print("vectorStore",vectorStore)

      
    except Exception as e:
        return jsonify({"error":str(e)}), 500

    return jsonify({
            "message": "File uploaded, loaded, and chunked successfully",
            "total_chunks": len(chunks),
            "sample_chunk": chunks[0].page_content[:300]  # Show preview
        }), 200


@app.route('/query', methods=['POST'])
def query_rag():
    data = request.json
    question = data.get('question')
    print("question",question)

    if not question:
        return jsonify({"error":"Question is required"}), 400
    
    try:
        answer =query_with_context(question) 
        (question)
        return jsonify({"answer": answer}), 200
        
    except Exception as e:
        return jsonify({"error":str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
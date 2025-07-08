from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils.pdf_loader import extract_text_from_pdf
from chunking.fixed import fixed_chunking
from chunking.recursive import recursive_chunking
from chunking.document_based import document_chunking
from chunking.semantic import semantic_chunking

app = Flask(__name__)
CORS(app)

@app.route('/api/upload', methods=['POST'])
def upload_pdf():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    filepath = os.path.join('uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(filepath)

    text = extract_text_from_pdf(filepath)
    return jsonify({'text': text})

@app.route('/api/chunk', methods=['POST'])
def chunk_text():
    data = request.get_json()
    text = data.get('text')
    strategy = data.get('strategy')

    if not text or not strategy:
        return jsonify({'error': 'Missing text or strategy'}), 400

    if strategy == 'fixed':
        chunks = fixed_chunking(text)
    elif strategy == 'recursive':
        chunks = recursive_chunking(text)
    elif strategy == 'document':
        chunks = document_chunking(text)
    elif strategy == 'semantic':
        chunks = semantic_chunking(text)
    else:
        return jsonify({'error': 'Invalid strategy'}), 400

    return jsonify({'chunks': chunks})

if __name__ == '__main__':
    app.run(debug=True)

# loader.py

import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_community.document_loaders.word_document import Docx2txtLoader

def load_documents(file_path: str) -> List[Document]:
    """
    Load a document based on its file type (.pdf, .docx, .txt)
    and return a list of LangChain Document objects.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        loader = PyMuPDFLoader(file_path)
    elif ext == ".docx":
        loader = Docx2txtLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

    documents = loader.load()
    return documents

# Temporary test block to run this directly (you can delete later)
# if __name__ == "__main__":
#     file_path = "../documents/VisualTutorAI.pdf"  
#     docs = load_documents(file_path)

#     print(f"Loaded {len(docs)} document pages")
#     print("Sample content:\n", docs[0].page_content[:500])

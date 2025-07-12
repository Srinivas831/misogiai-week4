# backend/db/fetch_unvectorized.py

from document_db import Document, SessionLocal

def get_unvectorized_documents():
    session = SessionLocal()
    docs = session.query(Document).filter(Document.is_vectorized == False).all()
    session.close()
    return docs

# backend/db/insert_document.py

from document_db import Document, SessionLocal

def add_document(source, content, category):
    session = SessionLocal()
    new_doc = Document(
        source=source,
        content=content,
        category=category,
        is_vectorized=False
    )
    session.add(new_doc)
    session.commit()
    session.close()

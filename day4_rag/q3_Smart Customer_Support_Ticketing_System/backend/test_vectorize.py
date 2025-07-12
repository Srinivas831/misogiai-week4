from vectorstore.vectorizer import get_unvectorized_documents, vectorize_documents
from db.document_db import SessionLocal, Document
from sqlalchemy.orm import Session

def delete_all_documents():
    session: Session = SessionLocal()
    try:
        deleted = session.query(Document).delete()
        session.commit()
        print(f"🗑️ Deleted {deleted} documents from the database.")
    except Exception as e:
        print("❌ Error deleting documents:", e)
        session.rollback()
    finally:
        session.close()

# delete_all_documents()

# docs = get_unvectorized_documents()
docs = vectorize_documents()
# for doc in docs:
#     print(f"{doc.id} | {doc.category} | {doc.source[:40]}...")



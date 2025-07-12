from db.document_db import Document, SessionLocal
from typing import List
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document as LCDocument
# from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
load_dotenv()

def get_unvectorized_documents() -> List[Document]:
    session: Session = SessionLocal()
    try:
        documents = session.query(Document).filter(Document.is_vectorized == False).all()
        print(f"Found {len(documents)} unvectorized documents")
        return documents
    finally:
        session.close()


# 2. Embedding model
embedding_model = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

# 3. Chroma vector DB path
# CHROMA_PATH = "chroma_db"
# if not os.path.exists(CHROMA_PATH):
#     os.makedirs(CHROMA_PATH)

# 3. FAISS vector DB path
FAISS_PATH = "faiss_vectorstore"
if not os.path.exists(FAISS_PATH):
    os.makedirs(FAISS_PATH)

# 1. Text splitter setup
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 100
)
    

# 4. Main vectorization function
def vectorize_documents():
    raw_docs = get_unvectorized_documents()
    print(f"Found {len(raw_docs)} unvectorized documents")
    if not raw_docs:
        print("No unvectorized documents found")
        return
    
    # print("raw_docs: ", raw_docs)
    # print("length of raw_docs: ", len(raw_docs))

    session: Session = SessionLocal()
    try:
        all_chunks = []
        for doc in raw_docs:
            # Split into smaller chunks
            chunks = text_splitter.split_text(doc.content)
            print(f"Splitted {doc.source} into {len(chunks)} chunks")

            # Convert each chunk into a LangChain Document with metadata
            for i, chunk in enumerate(chunks):
                metadata = {
                    "doc_id": str(doc.id),
                    "category": doc.category,
                    "source": doc.source,
                    "chunk_id": f"{doc.id}_{i}"
                }
                
                all_chunks.append(LCDocument(
                    page_content = chunk,
                    metadata = metadata
                ))

                if i==0 :
                    # print(f"first chunk of {doc.source}:",all_chunks)
                    print(f"first chunk of {doc.source}: {all_chunks[0]}")


        # print(" Starting Chroma.from_documents...")
        # Create vectorstore from chunks
        # vectorstore = Chroma.from_documents(documents = all_chunks, embedding = embedding_model, persist_directory = CHROMA_PATH)
        # vectorstore.persist()

        vectorstore = FAISS.from_documents(documents = all_chunks, embedding = embedding_model)
        print("Vectorstore created successfully")
        vectorstore.save_local(FAISS_PATH)
        print("Vectorstore saved successfully")
        vs_check = FAISS.load_local(FAISS_PATH, OpenAIEmbeddings(),allow_dangerous_deserialization=True)
        print(f"📌 {len(vs_check.docstore._dict)} chunks stored in FAISS.")

        # Update document status in DB
        for doc in raw_docs:
            print(f"Updating document {doc.id} to vectorized")
            doc.is_vectorized = True
            session.commit()

    except Exception as e:
        print("❌ Error during vectorization:", e)
        session.rollback()
    finally:
        session.close()

            



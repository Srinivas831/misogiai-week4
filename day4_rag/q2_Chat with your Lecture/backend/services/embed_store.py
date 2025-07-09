import os
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def embed_transcript(transcript_path: str, collection_name: str = "lecture_chunks") -> str:
    """
    Loads transcript text, splits into chunks, embeds, and stores in ChromaDB.
    """
    print("transcript_path",transcript_path)
    try:
        # 1. Load transcript text
        with open(transcript_path, "r", encoding="utf-8") as f:
            full_text = f.read()

        # 2. Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_text(full_text)

        print(f"[📚] Split into {len(chunks)} chunks.")

        # 3. Create embeddings
        embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

        # 4. Store in Chroma
        vector_store = Chroma.from_texts(
            texts=chunks,
            embedding=embedding_model,
            persist_directory=f"vectorstores/{collection_name}"
        )

        vector_store.persist()  # save to disk
        print(f"[✅] Stored {len(chunks)} chunks in ChromaDB at vectorstores/{collection_name}")

        return f"vectorstores/{collection_name}"

    except Exception as e:
        print(f"[❌] Error embedding transcript: {e}")
        return ""

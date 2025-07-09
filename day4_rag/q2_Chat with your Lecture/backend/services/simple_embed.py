import os
import json
import time
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def simple_embed_transcript(transcript_path: str, collection_name: str = "lecture_chunks") -> str:
    """
    Simple embedding that saves to JSON files instead of ChromaDB.
    """
    print(f"[🔄] Simple embedding for: {transcript_path}")
    
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

        # 3. Create embeddings model
        print("[🔄] Creating OpenAI embeddings model...")
        embedding_model = OpenAIEmbeddings()
        print("[✅] OpenAI embeddings model created.")

        # 4. Process chunks one by one and save to JSON
        output_dir = f"vectorstores/{collection_name}"
        os.makedirs(output_dir, exist_ok=True)
        
        embeddings_data = []
        
        for i, chunk in enumerate(chunks):
            print(f"[🔄] Processing chunk {i+1}/{len(chunks)}...")
            
            try:
                # Create embedding for this chunk
                embedding = embedding_model.embed_query(chunk)
                
                chunk_data = {
                    "id": f"chunk_{i}",
                    "text": chunk,
                    "embedding": embedding,
                    "metadata": {"chunk_index": i}
                }
                
                embeddings_data.append(chunk_data)
                print(f"[✅] Chunk {i+1} embedded successfully!")
                
                # Small delay to avoid rate limiting
                if i < len(chunks) - 1:
                    time.sleep(0.5)
                    
            except Exception as chunk_error:
                print(f"[❌] Error processing chunk {i+1}: {chunk_error}")
                continue

        # 5. Save to JSON file
        output_file = os.path.join(output_dir, "embeddings.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(embeddings_data, f, indent=2)
        
        print(f"[✅] Saved {len(embeddings_data)} embeddings to {output_file}")
        return output_file

    except Exception as e:
        print(f"[❌] Error in simple embedding: {e}")
        return "" 
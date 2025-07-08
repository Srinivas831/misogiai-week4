def fixed_chunking(text, chunk_size=500):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append({
            'text': chunk,
            'start': i,
            'end': i + chunk_size,
            'length': len(chunk)
        })
    return chunks

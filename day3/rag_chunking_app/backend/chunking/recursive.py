import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

def recursive_chunking(text, max_tokens=500):
    sentences = sent_tokenize(text)
    chunks, chunk = [], ''
    for sent in sentences:
        if len(chunk) + len(sent) <= max_tokens:
            chunk += ' ' + sent
        else:
            chunks.append({
                'text': chunk.strip(),
                'length': len(chunk)
            })
            chunk = sent
    if chunk:
        chunks.append({
            'text': chunk.strip(),
            'length': len(chunk)
        })
    return chunks

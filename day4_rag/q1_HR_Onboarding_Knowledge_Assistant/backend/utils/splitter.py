
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(document):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50,separators=["\n\n", "\n", " ", ""])
    # print("text_splitter",text_splitter.split_documents(document))
    
    return text_splitter.split_documents(document)
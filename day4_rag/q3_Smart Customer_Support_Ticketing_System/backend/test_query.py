import os
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
load_dotenv()

# 1. FAISS vector store path
FAISS_PATH = "faiss_vectorstore"

# Step 1: Take user query
user_query = input("Enter your query: ")

# Step 2: Classify query category
def classify_query_category(query: str) -> str:
     categories = ['FAQ', 'Returns', 'Shipping', 'Warranty', 'Payments']
     prompt = f"""  
     You are a helpful assistant that classifies user queries into one of the following categories:
     {categories}
     User query: {query}
     
     Return ONLY the category name that best matches the user query.
     Do not provide any explanation or additional text.
     If the query does not belong to any of the categories, return "Other".
     
     Examples:
     - For "My order is damaged" return "Shipping"
     - For "I want to return my product" return "Returns"
     - For "Payment failed" return "Payments"
     
     Category:
     """
     llm = ChatOpenAI(
         temperature=0.2,
         model_name="gpt-4o",
         openai_api_key=os.getenv("OPENAI_API_KEY")
     )
     response = llm.invoke(prompt)
     return response.content.strip()


# Step 4: Load FAISS vector store
def load_vectorstore():
    return FAISS.load_local(FAISS_PATH, OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY")), allow_dangerous_deserialization=True)


# Step 5: Search vectorstore with category filter
def search_documents(user_query, category: str, top_k: int = 5):
    vectorstore = load_vectorstore()
    if category != "Other":
        results = vectorstore.similarity_search(user_query, k=top_k, filter={"category": category})
    else:
        results = vectorstore.similarity_search(user_query, k=top_k)
    return results


# Step 6: Generate final answer using LLM with retrieved context
def generate_answer(user_query: str, retrieved_docs: list, category: str) -> str:
    # Combine all retrieved chunks into context
    context = "\n\n".join([f"Document {i+1}:\n{doc.page_content}" for i, doc in enumerate(retrieved_docs)])
    
    prompt = f"""
    You are a helpful customer support assistant. Answer the user's question based on the provided context documents.
    
    Context from {category} support documents:
    {context}
    
    User Question: {user_query}
    
    Instructions:
    - Provide a clear, helpful answer based on the context
    - If the context doesn't contain enough information, say so
    - Be concise but comprehensive
    - Use a friendly, professional tone
    
    Answer:
    """
    
    llm = ChatOpenAI(
        temperature=0.3,
        model_name="gpt-4o",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    response = llm.invoke(prompt)
    return response.content.strip()


# ===== Main Pipeline =====
try:
    predicted_category = classify_query_category(user_query)
    print(f"Predicted category: {predicted_category}")
    
    top_docs = search_documents(user_query, predicted_category, top_k=3)
    print(f"\nTop {len(top_docs)} matching chunks:\n")
    for i, doc in enumerate(top_docs, 1):
        print(f"{i}. [Category: {doc.metadata['category']}]")
        print(doc.page_content[:300])  # print first 300 characters
        print("-" * 80)
    
    # Generate final answer
    if top_docs:
        print(f"\n{'='*60}")
        print("FINAL ANSWER:")
        print(f"{'='*60}")
        final_answer = generate_answer(user_query, top_docs, predicted_category)
        print(final_answer)
        print(f"{'='*60}")
    else:
        print("\nNo relevant documents found to answer your question.")

except Exception as e:
    print(f"Error: {e}")
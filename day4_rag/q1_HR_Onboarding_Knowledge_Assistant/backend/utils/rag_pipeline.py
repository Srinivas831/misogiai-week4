from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import RunnableLambda

# Embed documents using OpenAI
def embed_and_store(chunks: list[Document]):
     # Step 1: Create embedding model
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        # Step 2: Store in FAISS vector database
    vectorstore = FAISS.from_documents(chunks, embeddings)

     # Step 3: Save locally to disk
    vectorstore.save_local("vectorstore")

    return vectorstore
    
# Load vectorstore once globally (FAISS will load index and metadata)
def load_vectorstore():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)
    
#  Full RAG QA Pipelin

def query_with_context(question: str) -> str:
    # 1. Load VectorStore
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_type="similarity", k=3)

    # 2. Prompt Template
    template = """
    You are an HR Assistant AI helping new employees understand company policy.
    Use the following extracted document parts to answer the question.
    Always say "According to policy..." and cite the source content.

    Context:
    {context}

    Question:
    {question}
    """
    prompt = PromptTemplate.from_template(template)

    # 3. Chain
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    chain = (
        RunnableLambda(lambda x: {
            "context": retriever.invoke(x["question"]),
            "question": x["question"]
        })
        | prompt
        | model
        | StrOutputParser()
    )

    # 4. Run chain
    answer = chain.invoke({"question": question})
    return answer



    # def query_with_context(question: str) -> str:
    # # 1. Load the vectorstore (loads FAISS index and embeddings)
    # vectorstore = load_vectorstore()

    # # 2. Convert the vectorstore to a retriever (top-k search interface)
    # retriever = vectorstore.as_retriever(search_type="similarity", k=3)

    # # 3. Embed the question and retrieve top 3 relevant chunks
    # print("Embedding and searching for similar chunks...")
    # top_documents = retriever.invoke(question)

    # # Debug: Show retrieved chunks
    # for i, doc in enumerate(top_documents):
    #     print(f"\n--- Retrieved Document {i+1} ---")
    #     print(doc.page_content)

    # # 4. Create a prompt template with placeholders for context and question
    # template = """
    # You are an HR Assistant AI helping new employees understand company policy.
    # Use the following extracted document parts to answer the question.
    # Always say "According to policy..." and cite the source content.

    # Context:
    # {context}

    # Question:
    # {question}
    # """
    # prompt = PromptTemplate.from_template(template)

    # # 5. Fill the prompt with actual values
    # context_text = "\n\n".join([doc.page_content for doc in top_documents])
    # final_prompt = prompt.format(context=context_text, question=question)

    # print("\n--- Final Prompt Sent to LLM ---")
    # print(final_prompt)

    # # 6. Send to OpenAI Chat model
    # llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    # answer = llm.invoke(final_prompt)

    # # 7. Return the final answer
    # return answer
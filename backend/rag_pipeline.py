import os
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

load_dotenv()

VECTOR_DB_PATH = "data/vector_db"
LLM_MODEL = os.getenv("LLM_MODEL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_rag_chain():
    # Load vector DB and embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embeddings)
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    # LLM via Groq
    llm = ChatGroq(api_key=GROQ_API_KEY, model_name=LLM_MODEL, temperature=0)
    # RAG chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain

def answer_query(query):
    qa_chain = get_rag_chain()
    result = qa_chain(query)
    return result["result"], result["source_documents"]

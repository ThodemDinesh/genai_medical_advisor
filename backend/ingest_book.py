import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter



load_dotenv()

BOOK_PATH = "data/medical_book.pdf"
VECTOR_DB_PATH = "data/vector_db"

def ingest_book():
    # Load PDF
    loader = PyPDFLoader(BOOK_PATH)
    docs = loader.load()
    # Split text
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs_split = splitter.split_documents(docs)
    # Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # Vector DB
    vectordb = Chroma.from_documents(docs_split, embeddings, persist_directory=VECTOR_DB_PATH)
    vectordb.persist()
    print("Book ingested and vector DB created.")

if __name__ == "__main__":
    ingest_book()

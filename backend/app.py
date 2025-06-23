# from fastapi import FastAPI, Request
# from pydantic import BaseModel
# from rag_pipeline import answer_query

# app = FastAPI()

# class QueryRequest(BaseModel):
#     question: str

# @app.post("/ask")
# async def ask_medical_advisor(request: QueryRequest):
#     answer, sources = answer_query(request.question)
#     return {
#         "answer": answer,
#         "sources": [src.page_content[:200] for src in sources]
#     }
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain

load_dotenv()

app = FastAPI()

VECTOR_DB_PATH = "data/vector_db"
LLM_MODEL = os.getenv("LLM_MODEL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class Message(BaseModel):
    role: str
    content: str

class QueryRequestWithHistory(BaseModel):
    question: str
    history: List[Message] = []

# Initialize embeddings and vector store once
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embeddings)
retriever = vectordb.as_retriever(search_kwargs={"k": 3})
llm = ChatGroq(api_key=GROQ_API_KEY, model_name=LLM_MODEL, temperature=0)

# Create conversational retrieval chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

@app.post("/ask")
async def ask_medical_advisor(request: QueryRequestWithHistory):
    # Prepare chat history as list of tuples (user, assistant)
    chat_history = []
    # Only keep last 5 user-assistant pairs (10 messages)
    last_five = request.history[-10:]
    for i in range(0, len(last_five), 2):
        if i+1 < len(last_five):
            user_msg = last_five[i].content
            assistant_msg = last_five[i+1].content
            chat_history.append((user_msg, assistant_msg))

    result = qa_chain({"question": request.question, "chat_history": chat_history})

    return {
        "answer": result["answer"],
        "sources": [doc.page_content[:200] for doc in result["source_documents"]]
    }

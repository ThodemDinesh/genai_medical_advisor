# 🩺 GenAI Medical Advisor

A modern, AI-powered medical assistant that provides solutions and precautions for medical queries by referencing a trusted medical book. Built with Retrieval-Augmented Generation (RAG), Large Language Models (LLMs), FastAPI, Streamlit, and a vector database.

---

## 🚀 Features

- **Conversational Chatbot:** Intuitive, chat-style interface for natural interactions.
- **Contextual Memory:** Remembers the last 5 questions and answers for coherent multi-turn conversations.
- **Trusted Knowledge Base:** Answers are grounded in your provided medical book, not just generic AI model data.
- **Retrieval-Augmented Generation (RAG):** Combines semantic search and LLMs for accurate, source-backed responses.
- **Full Stack:** FastAPI backend, Streamlit frontend, and Chroma vector store.
- **Source Transparency:** Users can view which book passages were referenced for each answer.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI, Uvicorn
- **AI Orchestration:** LangChain, ConversationalRetrievalChain
- **LLM Inference:** Groq API (LLama3 or similar)
- **Embeddings:** HuggingFace Transformers
- **Vector Store:** ChromaDB
- **PDF Parsing:** PyPDF
- **Environment Management:** python-dotenv

---

## 📦 Project Structure

```
medical_advisor_gen_ai/
├── backend/
│   ├── app.py
│   ├── rag_pipeline.py
│   ├── ingest_book.py
│   ├── requirements.txt
│   ├── .env
│   └── data/
│       └── medical_book.pdf
├── frontend/
│   ├── app.py
│   └── requirements.txt
└── README.md
```

---

## ⚡ Quickstart

### 1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/medical_advisor_genai.git
cd medical_advisor_genai
```

### 2. **Backend Setup**

```bash
cd backend
pip install -r requirements.txt
# Add your Groq API key and model to .env
python ingest_book.py  # Ingest and index your medical book
python -m uvicorn app:app --reload --port 8000
```

### 3. **Frontend Setup**

Open a new terminal:

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### 4. **Access the App**

- Go to [http://localhost:8501](http://localhost:8501) for the frontend.
- API docs available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 🧑‍💻 How It Works

1. **User asks a medical question** in the chat interface.
2. **Frontend sends the question and recent chat history** to the backend.
3. **Backend retrieves relevant passages** from the medical book using semantic search.
4. **LLM (via Groq) generates an answer**, grounded in the retrieved context.
5. **Sources are displayed** for transparency and trust.

---

## 📝 Customization

- **Change the medical book:** Replace `backend/data/medical_book.pdf` with your own PDF.
- **Adjust context window:** Change the number of remembered Q&A pairs in the code.
- **Switch LLMs:** Update the `.env` file with your preferred model.

---

## 🧩 Example Use Cases

- Medical colleges and clinics seeking AI-powered, book-grounded Q&A.
- Patient-facing health chatbots with reliable, up-to-date information.
- Educational tools for students and professionals.

---

## 🛡️ Disclaimer

> **This project is for educational and research purposes only. It does not provide medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical concerns.**

---

## 🙌 Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [Streamlit](https://streamlit.io/)
- [Groq](https://groq.com/)
- [Chroma](https://www.trychroma.com/)
- [HuggingFace](https://huggingface.co/)

---

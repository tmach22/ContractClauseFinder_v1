# 🧠 Contract Clause Finder — RAG-powered Legal Document Q&A

This is a Retrieval-Augmented Generation (RAG) application that simplifies the understanding of legal documents using AI.

By uploading a contract (PDF), users can ask questions in plain English. The system retrieves the most relevant clauses from the document and uses a state-of-the-art LLM to generate a grounded response, referencing exactly which clauses were used.

---

## 🔍 Why This Matters

Traditional language models can hallucinate or provide vague answers — a critical issue in legal settings. This tool uses a RAG pipeline to ensure:

- ✅ Answers are **grounded** in the uploaded document
- 📄 Supporting **clauses are shown alongside** the response
- 🤖 AI responses are **transparent and verifiable**, not black-box

---

## ✨ Features

- 📎 Upload legal PDFs via an intuitive Streamlit UI
- ✂️ Auto-chunk documents into logical clauses
- 🧠 Embed clauses using **BGE-small**
- 💽 Store vectors in **Qdrant Cloud**
- 🔍 Retrieve top-k relevant clauses
- 🤖 Generate accurate answers using **Mistral-7B** or any OpenRouter-compatible model
- 💬 Display responses **with full source citations**
- 🌐 Modular, easily deployable FastAPI backend + Streamlit frontend

---

## 🛠 Tech Stack

| Layer        | Tools Used |
|--------------|------------|
| UI           | `Streamlit` |
| Backend API  | `FastAPI`, `Uvicorn` |
| Embedding    | `sentence-transformers` (BAAI/bge-base-en-v1.5) |
| Vector DB    | `Qdrant Cloud` |
| LLM          | `Llama-3.3-70B-Instruct` via HuggingFace API |
| PDF Parsing  | `PyMuPDF` |

---

## 🎥 Demo Preview

🔗 https://www.loom.com/share/8ce0110505694625a131d1c58dc22f6d?sid=8525131a-3124-4a29-89bc-093c8750ce69

---

## ⚙️ Local Setup

### 1. Clone the repository
```
git clone https://github.com/tmach22/ContractClauseFinder_v1.git
cd ContractClauseFinder_v1
```
### 2. Create virtual env
```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```
### 3. Install dependencies
```
pip install -r requirements.txt
```
### 4. Create a .env file for secrets
```
OPENROUTER_API_KEY=your_openrouter_key
QDRANT_API_KEY=your_qdrant_key
QDRANT_URL=https://your-qdrant-instance.qdrant.tech
```
### 5. Run the backend
```
uvicorn main:app --reload
```
### 6. Run the StreamLit frontend
```
streamlit run app.py
```

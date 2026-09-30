# 📚 Harry Potter RAG (LangChain + Groq)

A small Retrieval-Augmented Generation (RAG) project built to revise core LangChain and RAG concepts. The goal is a Q&A system that answers questions about a Harry Potter book using only the content of the PDF.

> 🚧 **Status: Work in progress**  
> Phase 1 (ingestion pipeline) is complete. Retrieval and answer generation are coming next.

---

## 🗺️ Roadmap

- [x] **Phase 1 – Ingestion**
  - [x] Load PDF
  - [x] Split into chunks
  - [x] Generate embeddings
  - [x] Store in a persistent vector database
- [ ] **Phase 2 – Retrieval & Generation**
  - [ ] Build a retriever on top of the vector store
  - [ ] Connect the Groq LLM
  - [ ] Build the RAG chain (prompt + context + answer)
  - [ ] Simple CLI / UI for asking questions

---

## ⚙️ How Phase 1 Works

```
PDF  →  PyPDFLoader  →  RecursiveCharacterTextSplitter  →  HuggingFace Embeddings  →  ChromaDB
```

| Step | Tool | Details |
|------|------|---------|
| Document loading | `PyPDFLoader` | Loads the PDF page by page into LangChain `Document` objects |
| Chunking | `RecursiveCharacterTextSplitter` | `chunk_size=1000`, `chunk_overlap=100` |
| Embeddings | `BAAI/bge-small-en-v1.5` | Runs locally through `langchain-huggingface` |
| Vector store | `Chroma` | Persisted to disk at `database/vectorStore` |

---

## 🧰 Tech Stack

- **Python 3.10+**
- [LangChain](https://python.langchain.com/) (`langchain-community`, `langchain-text-splitters`)
- [ChromaDB](https://www.trychroma.com/) – vector database
- [Hugging Face](https://huggingface.co/BAAI/bge-small-en-v1.5) – embedding model
- [Groq](https://groq.com/) – LLM provider (used in Phase 2)
- `python-dotenv` – environment variable management

---

## 📁 Project Structure

```
.
├── backend/
│   └── main.py            # Ingestion pipeline (load → chunk → embed → store)
├── resources/
│   └── harrypotter.pdf    # Source document (not included in the repo)
├── database/
│   └── vectorStore/       # Generated Chroma DB (git-ignored)
├── requirements.txt
├── .env                   # API keys (git-ignored)
├── .env.example           # Template for environment variables
└── .gitignore
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy `.env.example` to `.env` and add your key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> The Groq key isn't used in Phase 1, but it will be needed from Phase 2 onwards.

### 5. Add your PDF

Place the book you want to index at:

```
resources/harrypotter.pdf
```

### 6. Run the ingestion pipeline

Run from the **project root** (paths in the script are relative):

```bash
python backend/main.py
```

This creates the vector database at `database/vectorStore/`.

---

## 📝 Notes

- The first run downloads the embedding model from Hugging Face, so it may take a moment.
- Re-running the script adds the chunks to the existing store again, which creates duplicates. Delete `database/vectorStore/` before re-indexing.
- The PDF is excluded from version control because it is copyrighted material. Bring your own copy.

---

## 🔜 Coming Next

Retrieval, prompt construction, and answer generation with Groq. This README will be updated as each phase lands.
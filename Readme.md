# 📚 Harry Potter RAG (LangChain + Groq)

A small Retrieval-Augmented Generation (RAG) project built to revise core LangChain and RAG concepts. It answers questions about a Harry Potter book using only the content of the PDF, and says so when the answer isn't in the book.

---

## 🗺️ Roadmap

- [x] **Phase 1 – Ingestion**
  - [x] Load PDF
  - [x] Split into chunks
  - [x] Generate embeddings
  - [x] Store in a persistent vector database
- [x] **Phase 2 – Retrieval & Generation**
  - [x] Load the persisted vector store
  - [x] Build a retriever
  - [x] Connect the Groq LLM
  - [x] Grounded prompt (answers only from retrieved context)
  - [x] Command-line chat loop
- [ ] **Ideas for next**
  - [ ] Conversation memory
  - [ ] Show source pages with each answer
  - [ ] Rewrite the flow as a LangChain (LCEL) chain
  - [ ] Simple web UI

---

## ⚙️ How It Works

**Phase 1 – Ingestion** (`backend/main.py`, run once)

```
PDF → PyPDFLoader → RecursiveCharacterTextSplitter → HuggingFace Embeddings → ChromaDB
```

**Phase 2 – Question answering** (`backend/app.py`)

```
Question → Retriever (Chroma) → Relevant chunks → Prompt + Groq LLM → Answer
```

| Step | Tool | Details |
|------|------|---------|
| Document loading | `PyPDFLoader` | Loads the PDF page by page |
| Chunking | `RecursiveCharacterTextSplitter` | `chunk_size=1000`, `chunk_overlap=100` |
| Embeddings | `BAAI/bge-small-en-v1.5` | Runs locally via `langchain-huggingface` |
| Vector store | `Chroma` | Persisted to disk in `vectorStore/` |
| Retrieval | `store.as_retriever()` | Default similarity search (top 4 chunks) |
| LLM | `ChatGroq` | Model: `openai/gpt-oss-20b` |

The prompt tells the model to use only the retrieved context, avoid making things up, and reply *"I don't know based on the provided book."* when the answer isn't there.

---

## 🧰 Tech Stack

- **Python 3.10+**
- [LangChain](https://python.langchain.com/) (`langchain-community`, `langchain-text-splitters`, `langchain-groq`, `langchain-huggingface`)
- [ChromaDB](https://www.trychroma.com/) – vector database
- [Hugging Face](https://huggingface.co/BAAI/bge-small-en-v1.5) – embedding model
- [Groq](https://groq.com/) – LLM inference
- `python-dotenv` – environment variable management

---

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py            # Ingestion: load → chunk → embed → store
│   └── app.py             # Chat loop: retrieve → prompt → answer
├── resources/
│   └── harrypotter.pdf    # Source document (not included in the repo)
├── vectorStore/           # Generated Chroma DB (git-ignored)
├── requirements.txt
├── .env                   # API keys (git-ignored)
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Ishaan0901/harry-potter-rag.git
cd harry-potter-rag
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

### 4. Add your Groq API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

You can get a free key from the [Groq console](https://console.groq.com/).

### 5. Add your PDF

Place the book you want to index at:

```
resources/harrypotter.pdf
```

### 6. Build the vector store (run once)

Run all commands from the **project root**, since paths in the scripts are relative:

```bash
python backend/main.py
```

### 7. Start chatting

```bash
python backend/app.py
```

```
Human: <your question>
```

Type `exit` or `bye` to quit.

---

## 📝 Notes

- The first run downloads the embedding model from Hugging Face, so it may take a moment.
- Re-running `main.py` adds the chunks to the existing store again, which creates duplicates. Delete the `vectorStore/` folder before re-indexing.
- Each question is answered independently, so the bot doesn't remember earlier messages yet.
- The PDF is excluded from version control because it is copyrighted material. Bring your own copy.
# AI RAG Agent Chatbot

A FastAPI-based conversational assistant that can answer questions from uploaded documents and use tools such as web search, calculator, and date/time when required.

This project was built for an AI Developer technical assessment. The focus is on a working API-first application with clean structure, simple local setup, document Q&A, streaming responses, conversation history, and basic agent-style tool usage.

---

## Features

- Upload PDF, TXT, or Markdown files
- Extract and split document text into chunks
- Generate embeddings with OpenAI
- Store document chunks in ChromaDB
- Retrieve relevant chunks for document-based Q&A
- Streaming chat response endpoint
- Session-based conversation history
- System prompt for assistant behavior
- Tool calling support
  - Web search using DuckDuckGo
  - Calculator
  - Current date/time
- Basic Streamlit frontend for local testing
- `.env.example` for environment setup
- Unit tests for chunking logic

---

## Tech Stack

| Area | Technology |
|---|---|
| Backend | FastAPI |
| Frontend | Streamlit |
| LLM | OpenAI Chat Model |
| Embeddings | OpenAI Embeddings |
| Vector Database | ChromaDB |
| PDF Parsing | pypdf |
| Web Search | DuckDuckGo Search |
| Testing | Pytest |

Python **3.11** is recommended for smooth dependency installation, especially on Windows.

---

## Project Structure

```text
ai-rag-agent-chatbot/
│
├── app/
│   ├── api/
│   │   └── routes.py              # FastAPI endpoints
│   │
│   ├── core/
│   │   ├── config.py              # Environment settings
│   │   └── prompts.py             # Assistant system prompt
│   │
│   ├── models/
│   │   └── schemas.py             # Request/response schemas
│   │
│   ├── services/
│   │   ├── chat_service.py        # Chat flow, RAG context, tool calling
│   │   ├── session_store.py       # In-memory chat history
│   │   └── vector_store.py        # ChromaDB and OpenAI embeddings
│   │
│   ├── tools/
│   │   ├── calculator.py          # Safe arithmetic tool
│   │   ├── date_time.py           # Current date/time tool
│   │   └── web_search.py          # DuckDuckGo web search tool
│   │
│   ├── utils/
│   │   ├── chunking.py            # Text chunking logic
│   │   └── file_loader.py         # PDF/TXT/MD text extraction
│   │
│   └── main.py                    # Application entry point
│
├── frontend/
│   └── streamlit_app.py           # Basic UI for testing
│
├── data/
│   ├── chroma/                    # Local ChromaDB data
│   └── uploads/                   # Uploaded files
│
├── tests/
│   └── test_chunking.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone <your-github-repo-url>
cd ai-rag-agent-chatbot
```

If you are running from a ZIP file, extract it and open the `ai-rag-agent-chatbot` folder in VS Code.

---

### 2. Check Python version

Use Python 3.11:

```bash
py -3.11 --version
```

Expected output:

```text
Python 3.11.x
```

---

### 3. Create virtual environment

Windows:

```bash
py -3.11 -m venv .venv
```

Mac/Linux:

```bash
python3.11 -m venv .venv
```

---

### 4. Activate virtual environment

Windows:

```bash
.venv\Scripts\activate
```

Mac/Linux:

```bash
source .venv/bin/activate
```

Check that the correct Python version is active:

```bash
python --version
```

---

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 6. Create `.env` file

Copy `.env.example` and create a new file named `.env` in the project root.

```env
OPENAI_API_KEY=your_openai_api_key_here
CHAT_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
APP_NAME=AI RAG Agent Chatbot
CHROMA_DIR=data/chroma
UPLOAD_DIR=data/uploads
TOP_K=4
```

Do not commit `.env` to GitHub.

---

## Run the Application

### 1. Start FastAPI backend

```bash
uvicorn app.main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

Swagger API docs:

```text
http://127.0.0.1:8000/docs
```

---

### 2. Start Streamlit frontend

Open a second terminal, activate the same virtual environment, then run:

```bash
streamlit run frontend/streamlit_app.py
```

Streamlit usually opens at:

```text
http://localhost:8501
```

---

## How to Test the Flow

### Test 1: Health Check

Open:

```text
http://127.0.0.1:8000/docs
```

Run:

```http
GET /api/health
```

Expected response:

```json
{
  "status": "ok",
  "app_name": "AI RAG Agent Chatbot"
}
```

---

### Test 2: Upload a Document

Use Swagger or Streamlit to upload a PDF/TXT/MD file.

API endpoint:

```http
POST /api/upload
```

Example curl:

```bash
curl -X POST "http://127.0.0.1:8000/api/upload" \
  -F "file=@sample.pdf"
```

Expected behavior:

1. File is saved in `data/uploads`
2. Text is extracted
3. Chunks are created
4. Embeddings are generated
5. Chunks are stored in ChromaDB

---

### Test 3: Ask a Document Question

API endpoint:

```http
POST /api/chat/stream
```

Example request body:

```json
{
  "session_id": "demo-session",
  "message": "What is this document about?",
  "use_rag": true
}
```

Example curl:

```bash
curl -N -X POST "http://127.0.0.1:8000/api/chat/stream" \
  -H "Content-Type: application/json" \
  -d "{\"session_id\":\"demo-session\",\"message\":\"What is this document about?\",\"use_rag\":true}"
```

---

### Test 4: Tool Calling

Try these questions in Streamlit:

```text
Calculate 125 * 18
```

```text
What is today's date and time in India?
```

```text
Search the web for the latest OpenAI model updates.
```

---

## How the System Works

### Document Upload and Indexing

When a file is uploaded, the backend extracts text and splits it into overlapping chunks. Each chunk is converted into an embedding using OpenAI and stored in ChromaDB with metadata such as filename, document id, and chunk index.

### RAG Chat Flow

When the user asks a question, the system retrieves the most relevant chunks from ChromaDB and passes them to the LLM as context. If the answer is not available in the uploaded document, the assistant is instructed to say that clearly instead of guessing.

### Agent Tool Flow

The chat service gives the model access to tools. The model can decide whether a tool is needed based on the user message. Tool results are added back into the conversation before the final response is streamed to the user.

---

## Design Decisions

### FastAPI

FastAPI was chosen because the task is API-focused and FastAPI provides clean routing, validation, and support for streaming responses.

### ChromaDB

ChromaDB was selected as the vector database because it runs locally and keeps the project easy to review without requiring a hosted vector database account.

### OpenAI Embeddings

OpenAI embeddings were used to keep semantic search quality reliable. The embedding model can be changed from the `.env` file.

### Simple Tool Layer

Instead of adding a heavy multi-agent framework, the project uses OpenAI tool calling directly. This keeps the implementation easier to understand and debug while still satisfying the agent/tool requirement.

### In-Memory Sessions

Conversation history is stored in memory using `session_id`. This is enough for an assessment project. For production, Redis or a database would be a better option.

### Streamlit Frontend

The Streamlit app is included only for quick local testing. The main application is the FastAPI backend.

---

## Run Tests

```bash
pytest
```

---

## GitHub Push Steps

### 1. Check ignored files

Make sure `.env` is not tracked:

```bash
git status
```

### 2. Initialize Git

```bash
git init
```

### 3. Add files

```bash
git add .
```

### 4. Commit

```bash
git commit -m "Initial commit: AI RAG agent chatbot"
```

### 5. Connect GitHub repository

```bash
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

---

## Submission Checklist

Before submitting the GitHub link:

- [ ] Backend runs with `uvicorn app.main:app --reload`
- [ ] Swagger opens at `/docs`
- [ ] Streamlit opens successfully
- [ ] PDF/TXT/MD upload works
- [ ] Chunks are stored in ChromaDB
- [ ] Chat endpoint streams response
- [ ] Document-based questions work
- [ ] Calculator/date/web-search tools work
- [ ] `.env.example` is present
- [ ] `.env` is not pushed to GitHub
- [ ] README has setup and run instructions

---

## Known Limitations

- Session history is stored in memory and resets when the server restarts.
- ChromaDB is stored locally, so uploaded document data is local to the machine.
- Web search depends on DuckDuckGo search availability.
- A valid OpenAI API key is required for embeddings and chat responses.

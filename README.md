# AI Research Assistant

AI Research Assistant helps you upload academic PDFs, extract and summarize their content, cluster related topics, detect cross-paper contradictions and research gaps, and chat with your papers using RAG.

## What It Does

- Upload PDF research papers.
- Extract text and split it into semantic chunks.
- Generate structured summaries:
	- Abstract
	- Methodology
	- Results
	- Conclusions
- Build local vector search with FAISS + sentence-transformers.
- Perform cross-paper analysis:
	- Topic clusters
	- Contradictions
	- Research gaps
- Ask natural-language questions against uploaded papers.

## Project Structure

```text
ai-research-assistant/
	ai_engine/               # NLP, embeddings, summarization, clustering, RAG client
	backend/app/             # FastAPI app, routes, schemas, service layer
	frontend/                # React + Vite UI
	data/                    # FAISS index and metadata storage
	notebooks/               # Experimental notebooks
	requirements.txt         # Python dependencies
	verify_setup.py          # Dependency verification script
```

## Tech Stack

- Backend: FastAPI, Uvicorn
- Frontend: React, Vite, Axios, TailwindCSS, Framer Motion
- NLP/ML: spaCy, transformers, sentence-transformers, scikit-learn, BERTopic
- Vector Store: FAISS (local)
- LLM Integration: LangChain + Ollama (local)

## Prerequisites

- Python 3.10+ recommended
- Node.js 18+ recommended
- Ollama installed and running locally
	- Default endpoint: `http://localhost:11434`
	- Default model: `llama3`

Install and pull model (if not already done):

```powershell
ollama pull llama3
```

## Quick Start

### 1) Clone and enter project

```powershell
cd D:\Mini_Project\ai-research-assistant
```

### 2) Set up Python environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3) Download spaCy model (required by `verify_setup.py`)

```powershell
python -m spacy download en_core_web_sm
```

### 4) Verify installation

```powershell
python verify_setup.py
```

### 5) Run backend (FastAPI)

```powershell
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend base URL: `http://localhost:8000`

### 6) Run frontend (React)

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend URL (default Vite): `http://localhost:5173`

## Environment Variables

The app supports optional LLM configuration:

- `OLLAMA_MODEL` (default: `llama3`)
- `OLLAMA_URL` (default: `http://localhost:11434`)

PowerShell example:

```powershell
$env:OLLAMA_MODEL="llama3"
$env:OLLAMA_URL="http://localhost:11434"
```

## API Endpoints

Base route: `/api/papers`

- `POST /api/papers/upload`
	- Upload one PDF file (`multipart/form-data`, field name: `file`)
- `GET /api/papers/`
	- List uploaded papers
- `DELETE /api/papers/{paper_id}`
	- Delete one paper from active session list
- `GET /api/papers/analyze`
	- Generate cross-paper clusters, contradictions, and research gaps
- `POST /api/papers/chat`
	- Ask a question about uploaded papers
	- Body: `{ "query": "..." }`

FastAPI docs:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## How It Works

1. PDF is uploaded to backend.
2. Text extraction is attempted with PyMuPDF, fallback to pdfplumber.
3. Text is chunked and embedded with sentence-transformers.
4. Embeddings are indexed in FAISS.
5. Summaries are generated via Ollama LLM.
6. Cross-paper analysis runs clustering + LLM synthesis.
7. Chat queries use retrieval over top chunks, then LLM response generation.

## Current Limitations

- Data is managed in-memory for paper records during runtime.
- FAISS index files are reset when the backend service initializes.
- `pymongo` is installed but a persistent MongoDB integration is not yet wired into the current backend flow.
- Very large PDFs may increase processing time.

## Troubleshooting

- Upload fails with "Only PDF files are supported":
	- Ensure the file extension is `.pdf`.
- PDF extraction fails with HTML error:
	- The file is likely a webpage saved as PDF; download the actual PDF directly.
- Chat/summary fails:
	- Ensure Ollama is running and the configured model is pulled.
- `verify_setup.py` fails on spaCy model:
	- Run `python -m spacy download en_core_web_sm`.
- Frontend cannot call backend:
	- Ensure backend runs on port 8000 and frontend uses `http://localhost:8000/api/papers`.

## Useful Commands

```powershell
# Backend
cd backend
python -m uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev

# Verify Python dependencies
python verify_setup.py
```

## License

Add your project license here (for example, MIT).
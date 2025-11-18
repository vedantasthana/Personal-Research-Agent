# Personal Research Agent + Coding Agent Hybrid

A modular AI system that learns from documents, research papers, websites, GitHub repositories, and codebases — and uses that knowledge to reason, plan, and modify code.  
This project integrates **RAG**, **vector search**, **agentic planning**, and **MCP tool-based code execution** into a unified platform.

---

## 🚀 Project Goals

- Build a production-grade ingestion → vector DB → RAG → agent → MCP loop.
- Enable deep reasoning over PDFs, research papers, technical blogs, and code.
- Add a coding agent capable of:
  - reading code  
  - applying patches  
  - generating test cases  
  - running tests  
  - refactoring intelligently  
- Learn modern AI infrastructure end-to-end.

---

## 🧩 High-Level Architecture

```
personal-research-agent/
│
├── backend/                 # FastAPI, ingestion, RAG, agents, MCP tools
├── frontend/                # Next.js UI (chat, file upload, code diff)
├── mcp_server/              # Tool definitions (repo, fs, vector, browser)
├── vectorstore/             # Chroma/pgvector implementations
│
└── docker/                  # Deployment configs
```

---

## 🏗 Architecture Diagram (Conceptual)

```text
                 ┌────────────────────────────┐
                 │         Frontend           │
                 │   (Next.js chat + UI)      │
                 └───────────────┬────────────┘
                                 │
                      REST / WebSocket
                                 │
     ┌───────────────────────────────────────────────────────┐
     │                  Backend (FastAPI)                    │
     │                                                       │
     │ 1. Ingestion Pipeline                                 │
     │    - PDF/URL/GitHub ingestion                         │
     │    - chunking, embeddings, metadata                   │
     │                                                       │
     │ 2. Vectorstore                                        │
     │    - Chroma / pgvector                                │
     │                                                       │
     │ 3. RAG Engine                                         │
     │    - retriever, reranker, hybrid search               │
     │    - context builder, query planner                   │
     │                                                       │
     │ 4. Agent Runtime                                      │
     │    - planning, reasoning, tool-calling                │
     │    - short-term & long-term memory                    │
     │                                                       │
     │ 5. MCP Tool Server                                    │
     │    - repo.read, apply_patch, run_tests                │
     │    - fs.read/write, vector.search, browser tools      │
     └───────────────────────────────────────────────────────┘
```

---

## 🔧 Tech Stack

**Backend**
- FastAPI  
- Python 3.10+  
- Chroma / pgvector  
- Tree-sitter (code parsing)  
- MCP tool server  
- OpenAI embeddings  

**Frontend**
- Next.js 14  
- Tailwind  
- CodeMirror / Monaco Editor  

---

## 🧪 Running Locally

### Backend
```
cd backend
pip install -r requirements.txt
uvicorn api.server:app --reload
```

### Frontend
```
cd frontend
npm install
npm run dev
```

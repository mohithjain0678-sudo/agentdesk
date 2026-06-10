# AgentDesk — AI Agent Workspace

AgentDesk is an AI-powered workspace where a single agent autonomously completes multi-step tasks using real tools — web search, file read/write, and directory management — through a clean chat interface.

Built for the **LLM with MCP track** at Hackverse X — Global Tech Innovation 2026.

🔗 **Live Demo:** https://agentdesk-dusky.vercel.app/
🔗 **Backend API:** https://agentdesk-backend-jut7.onrender.com

---

## What It Does

You give AgentDesk a task in plain English. The agent decides which tools to use, executes them autonomously, and returns a structured response — showing exactly what actions it took.

Example tasks:
- "Search the web for the latest AI research in 2026"
- "Write a project plan to notes.txt"
- "List all files in the current directory"
- "Read notes.txt and summarize it"

---

## Architecture
User → React Frontend → FastAPI Backend → LLM Agent (LLaMA 3.3 via Groq)
↓
Tool Dispatcher
├── web_search
├── read_file
├── write_file
└── list_files

The agent runs a reasoning loop — it decides whether to call a tool or return a final answer, processes tool results, and continues until the task is complete.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, CSS |
| Backend | FastAPI, Python |
| LLM | LLaMA 3.3-70b via Groq API |
| Agent Loop | Custom tool-calling implementation |
| Deployment | Vercel (frontend), Render (backend) |

---

## Tools Available

- **web_search** — searches the web via DuckDuckGo instant answers
- **read_file** — reads any file from the server filesystem
- **write_file** — writes content to a file
- **list_files** — lists files in a directory

---

## Running Locally

**Backend**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# add GROQ_API_KEY to .env
python -m uvicorn main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm start
```

---

## Project Structure

agentdesk/
├── backend/
│   ├── main.py        # FastAPI app and routes
│   ├── agent.py       # LLM agent loop and tool calling
│   ├── tools.py       # Tool implementations
│   └── requirements.txt
└── frontend/
└── src/
├── App.js     # Main React component
└── App.css    # Styling
---

## Built By

Mohith Jain — B.Tech ECE, VIT Chennai
GitHub: [@mohithjain0678-sudo](https://github.com/mohithjain0678-sudo)
LinkedIn: [mohith-jain-302076397](https://linkedin.com/in/mohith-jain-302076397)

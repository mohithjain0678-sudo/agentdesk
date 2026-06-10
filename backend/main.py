from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import run_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://agentdesk-dusky.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conversation_history = []

class MessageRequest(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"status": "AgentDesk is running"}

@app.post("/chat")
async def chat(request: MessageRequest):
    global conversation_history
    
    result = await run_agent(request.message, conversation_history)
    
    conversation_history.append({"role": "user", "content": request.message})
    conversation_history.append({"role": "assistant", "content": result["response"]})
    
    return {
        "response": result["response"],
        "actions": result["actions"]
    }

@app.post("/clear")
async def clear():
    global conversation_history
    conversation_history = []
    return {"status": "cleared"}
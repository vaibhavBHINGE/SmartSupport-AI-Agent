from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from backend import Agent
app=FastAPI(title="ChatSupportAI",version="0.1.0")

class cheakRequest(BaseModel):
    message:str
    session_id:str

class ChatResponse(BaseModel):
    response:str
    session_id:str

@app.get("/health")
def health_cheak():
    return {"status": "Active", "agent_model": "HuggingFace- deepseek-ai/DeepSeek-V4-Pro", "vector_db": "Chroma"}

@app.post("/chat",response_model=ChatResponse)
def chat_with_agent(request:cheakRequest):
    try:
        # Pass the frontend's message and session ID directly to your agent
        agent_response = Agent.run_agent(request.message, request.session_id)
        
        return ChatResponse(
            response=agent_response,
            session_id=request.session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""
REX AI - Main Server
FastAPI backend with WebSocket support
100% Offline, No API Keys Required
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import os
import sys
from typing import Dict, List
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.rex_engine import REXEngine

# Initialize FastAPI app
app = FastAPI(
    title="REX AI",
    description="Advanced Offline AI Assistant - 2M+ Skills, 14+ Languages",
    version="1.0.0"
)

# Enable CORS for all origins (for local development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize REX Engine
rex_engine = REXEngine()

# Store active connections
active_connections: Dict[str, WebSocket] = {}

@app.get("/")
async def root():
    """Serve the main frontend"""
    return FileResponse("frontend/index.html")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "REX AI",
        "version": "1.0.0",
        "offline_mode": True,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/status")
async def get_status():
    """Get REX engine status"""
    return rex_engine.get_status()

@app.get("/api/skills")
async def get_skills():
    """Get all available skills"""
    return rex_engine.get_skills_info()

@app.get("/api/skills/search")
async def search_skills(q: str):
    """Search for skills"""
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")
    results = rex_engine.search_skills(q)
    return {"query": q, "results": results, "count": len(results)}

@app.post("/api/chat")
async def chat(message: Dict):
    """Process chat message"""
    text = message.get("message", "")
    context = message.get("context", {})
    
    if not text:
        raise HTTPException(status_code=400, detail="Message text is required")
    
    result = rex_engine.process_message(text, context)
    return result

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    active_connections[client_id] = websocket
    
    # Send welcome message
    await websocket.send_json({
        "type": "welcome",
        "message": f"Welcome to REX AI! Connected as {client_id}",
        "status": rex_engine.get_status()
    })
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            
            try:
                message_data = json.loads(data)
                text = message_data.get("message", "")
                context = message_data.get("context", {})
                
                # Process message
                result = rex_engine.process_message(text, context)
                result["type"] = "response"
                result["client_id"] = client_id
                
                # Send response
                await websocket.send_json(result)
                
            except json.JSONDecodeError:
                # Handle plain text messages
                result = rex_engine.process_message(data, {})
                result["type"] = "response"
                result["client_id"] = client_id
                await websocket.send_json(result)
    
    except WebSocketDisconnect:
        del active_connections[client_id]
        print(f"Client {client_id} disconnected")

@app.get("/api/history")
async def get_history(limit: int = 10):
    """Get conversation history"""
    return {
        "history": rex_engine.get_conversation_history(limit),
        "count": limit
    }

@app.delete("/api/history")
async def clear_history():
    """Clear conversation history"""
    result = rex_engine.clear_history()
    return result

@app.get("/api/languages")
async def get_languages():
    """Get supported languages"""
    return {
        "languages": rex_engine.language_processor.get_supported_languages(),
        "count": len(rex_engine.language_processor.supported_languages)
    }

# Serve static files
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

if os.path.exists("assets"):
    app.mount("/assets", StaticFiles(directory="assets"), name="assets")

def main():
    """Run the server"""
    print("=" * 60)
    print("🤖 REX AI Server Starting...")
    print("=" * 60)
    print(f"📍 Server: http://localhost:8000")
    print(f"🌐 Languages: {len(rex_engine.language_processor.supported_languages)}+")
    print(f"⚡ Skills: {rex_engine.skill_manager.total_skills:,}")
    print(f"🔒 Mode: 100% Offline (No API Keys)")
    print(f"🎤 Voice: Enabled (Web Speech API)")
    print("=" * 60)
    print("\nPress Ctrl+C to stop the server\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

if __name__ == "__main__":
    main()

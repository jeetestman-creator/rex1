"""
REX AI - Advanced Offline AI Assistant
Main Server Entry Point
No API Keys Required - Fully Local Operation
"""

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from typing import Dict, List, Any
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.rex_engine import REXEngine
from skills.skill_manager import SkillManager
from skills.language_processor import LanguageProcessor

app = FastAPI(title="REX AI", version="1.0.0")

# Enable CORS for all origins (local development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core components
rex_engine = REXEngine()
skill_manager = SkillManager()
language_processor = LanguageProcessor()

# Store active connections
active_connections: Dict[str, WebSocket] = {}

@app.on_event("startup")
async def startup_event():
    """Initialize REX AI on startup"""
    print("🚀 REX AI Starting Up...")
    print(f"📦 Loaded {len(skill_manager.skills)} base skills")
    print(f"🌍 Supported languages: {', '.join(language_processor.supported_languages.keys())}")
    print("✅ REX AI Ready - No API Keys Required!")

@app.get("/")
async def get_frontend():
    """Serve the main frontend"""
    return FileResponse("frontend/index.html")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ai_engine": "online",
        "skills_loaded": len(skill_manager.skills),
        "languages_supported": len(language_processor.supported_languages),
        "offline_mode": True,
        "api_keys_required": False
    }

@app.get("/api/skills")
async def get_skills():
    """Get all available skills"""
    return {
        "total_skills": len(skill_manager.skills),
        "categories": skill_manager.get_categories(),
        "skills": skill_manager.list_skills()
    }

@app.get("/api/languages")
async def get_languages():
    """Get supported languages"""
    return {
        "supported_languages": language_processor.supported_languages,
        "default_language": "english"
    }

@app.post("/api/chat")
async def chat(message: dict):
    """Process chat message and return response"""
    user_input = message.get("message", "")
    language = message.get("language", "english")
    
    if not user_input:
        return {"error": "No message provided"}
    
    # Process through REX engine
    response = await rex_engine.process_message(user_input, language)
    
    return response

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    connection_id = id(websocket)
    active_connections[connection_id] = websocket
    
    try:
        # Send welcome message
        await websocket.send_json({
            "type": "welcome",
            "message": "Hello! I'm REX, your advanced offline AI assistant. How can I help you today?",
            "language": "english"
        })
        
        while True:
            data = await websocket.receive_text()
            
            try:
                message_data = json.loads(data)
                user_input = message_data.get("message", "")
                language = message_data.get("language", "english")
                
                if user_input:
                    # Process message
                    response = await rex_engine.process_message(user_input, language)
                    
                    # Send response
                    await websocket.send_json({
                        "type": "response",
                        "data": response
                    })
                    
            except json.JSONDecodeError:
                # Handle plain text messages
                response = await rex_engine.process_message(data, language)
                await websocket.send_json({
                    "type": "response",
                    "data": response
                })
                
    except WebSocketDisconnect:
        del active_connections[connection_id]
        print(f"Client disconnected: {connection_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        if connection_id in active_connections:
            del active_connections[connection_id]

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 REX AI - Advanced Offline AI Assistant")
    print("🔒 No API Keys Required - 100% Local Operation")
    print("🌍 Multi-language Support (Tamil, English + 12 more)")
    print("📱 Cross-platform: Mobile, Desktop, Tablet, Mac, Linux")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

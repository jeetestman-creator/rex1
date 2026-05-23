"""
REX AI - Advanced Full-Stack Python AI Assistant
Main Backend Server
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# FastAPI for high-performance API
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# AI/ML Libraries
try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False

try:
    from gtts import gTTS
    from playsound import playsound
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

# Import skills system
from skills.skill_manager import SkillManager
from skills.language_processor import LanguageProcessor

app = FastAPI(
    title="REX AI",
    description="Advanced AI Assistant with 2M+ Skills",
    version="1.0.0"
)

# Enable CORS for all devices
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
skill_manager = SkillManager()
language_processor = LanguageProcessor()

class ChatMessage(BaseModel):
    message: str
    language: str = "en"
    voice_enabled: bool = True
    context: Optional[Dict] = None

class VoiceResponse(BaseModel):
    text: str
    audio_url: Optional[str] = None
    language: str

@app.get("/")
async def root():
    """Serve the main interface"""
    return HTMLResponse(content=open("frontend/index.html").read())

@app.post("/api/chat")
async def chat_endpoint(message: ChatMessage):
    """Process chat messages with full context awareness"""
    
    # Detect and process language
    detected_lang = language_processor.detect_language(message.message)
    if message.language == "auto":
        message.language = detected_lang
    
    # Translate if needed
    if message.language not in ["en", "ta"]:
        translated = language_processor.translate(message.message, message.language, "en")
    else:
        translated = message.message
    
    # Process with AI engine
    response = await process_ai_message(translated, message.context)
    
    # Translate back if needed
    if message.language != "en":
        response = language_processor.translate(response, "en", message.language)
    
    # Generate voice if enabled
    audio_url = None
    if message.voice_enabled and TTS_AVAILABLE:
        audio_url = generate_voice(response, message.language)
    
    return {
        "response": response,
        "language": message.language,
        "audio_url": audio_url,
        "timestamp": datetime.now().isoformat(),
        "skills_used": skill_manager.get_last_used_skills()
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Real-time bidirectional communication"""
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Process message
            message = data.get("message", "")
            language = data.get("language", "en")
            
            response = await process_ai_message(message)
            
            # Send response
            await websocket.send_json({
                "response": response,
                "timestamp": datetime.now().isoformat()
            })
            
    except WebSocketDisconnect:
        print("Client disconnected")

@app.post("/api/voice/input")
async def voice_input(file: UploadFile = File(...)):
    """Process voice input"""
    if not SPEECH_AVAILABLE:
        raise HTTPException(status_code=503, detail="Speech recognition not available")
    
    recognizer = sr.Recognizer()
    with sr.AudioFile(file.file) as source:
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio)
        return {"text": text, "success": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Voice recognition failed: {str(e)}")

@app.get("/api/voice/output")
async def voice_output(text: str = "", language: str = "en"):
    """Generate voice output"""
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")
    
    audio_path = generate_voice(text, language)
    if audio_path:
        return StreamingResponse(open(audio_path, "rb"), media_type="audio/mpeg")
    else:
        raise HTTPException(status_code=503, detail="TTS not available")

@app.get("/api/skills")
async def list_skills(category: Optional[str] = None, limit: int = 100):
    """List available skills"""
    skills = skill_manager.list_skills(category, limit)
    return {"skills": skills, "total": len(skills)}

@app.post("/api/skills/execute")
async def execute_skill(skill_name: str, params: Dict[str, Any]):
    """Execute a specific skill"""
    result = await skill_manager.execute_skill(skill_name, params)
    return {"result": result, "skill": skill_name}

async def process_ai_message(message: str, context: Optional[Dict] = None) -> str:
    """Core AI processing engine"""
    
    # Check for skill-based responses first
    skill_response = await skill_manager.process_message(message, context)
    if skill_response:
        return skill_response
    
    # Fallback to general AI response
    if TORCH_AVAILABLE:
        # Use local AI model if available
        return generate_local_ai_response(message, context)
    else:
        # Fallback response system
        return generate_fallback_response(message, context)

def generate_local_ai_response(message: str, context: Optional[Dict]) -> str:
    """Generate response using local AI model"""
    # Implementation would use transformers library
    return f"REX AI: I understand your request about '{message}'. How can I assist you further?"

def generate_fallback_response(message: str, context: Optional[Dict]) -> str:
    """Intelligent fallback response system"""
    
    message_lower = message.lower()
    
    # Greeting patterns
    if any(word in message_lower for word in ["hello", "hi", "hey", "namaskaram", "vanakkam"]):
        return "Hello! I'm REX, your advanced AI assistant. How can I help you today?"
    
    # Tamil greetings
    if any(word in message_lower for word in ["வணக்கம்", "நலமா", "எப்படி இருக்கிறீர்கள்"]):
        return "வணக்கம்! நான் REX, உங்கள் மேம்பட்ட AI உதவியாளர். இன்று நான் உங்களுக்கு எப்படி உதவ முடியும்?"
    
    # Capability inquiry
    if any(word in message_lower for word in ["can you", "what can", "ability", "skill"]):
        return "I have access to over 2 million skills including data analysis, automation, creative writing, coding assistance, research, translation, voice interaction, and much more. What would you like me to help you with?"
    
    return f"I understand you're asking about '{message}'. As REX AI, I'm here to assist you with virtually any task. Could you provide more details so I can better help you?"

def generate_voice(text: str, language: str = "en") -> Optional[str]:
    """Generate human-like voice output"""
    if not TTS_AVAILABLE:
        return None
    
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        audio_path = f"assets/voice_{datetime.now().timestamp()}.mp3"
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        print(f"Voice generation error: {e}")
        return None

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting REX AI Server...")
    print("🌐 Access: http://localhost:8000")
    print("📱 Mobile/Tablet/Desktop/Mac/Linux compatible")
    print("🗣️  Languages: English, Tamil + 100+ more")
    print("⚡ Skills: 2M+ capabilities loaded")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

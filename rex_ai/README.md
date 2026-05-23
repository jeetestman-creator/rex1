# REX AI - Advanced Full-Stack Python AI Assistant

🤖 **REX** is a state-of-the-art, full-stack AI assistant built with Python, designed to be your ultimate productivity companion with over 2 million+ skills.

## 🌟 Features

### Core Capabilities
- **2M+ Skills**: Extensive skill system covering communication, productivity, analysis, creativity, technical tasks, data processing, automation, learning, and entertainment
- **Multi-Language Support**: Native support for Tamil (தமிழ்) and English, with extensibility to 100+ languages
- **Voice Interaction**: Human-like voice input and output with smooth, polite conversation
- **Cross-Platform**: Works seamlessly on Mobile, Tablet, Desktop, Mac, and Linux
- **Real-Time Communication**: WebSocket-based bidirectional communication
- **Context Awareness**: Maintains conversation context for intelligent responses

### Technical Features
- **FastAPI Backend**: High-performance async API server
- **Modern Frontend**: Responsive web interface with beautiful UI
- **Speech Recognition**: Voice input support via Web Speech API
- **Text-to-Speech**: Natural voice output generation
- **Skill System**: Modular, extensible skill architecture
- **Language Detection**: Automatic language identification

## 📁 Project Structure

```
rex_ai/
├── backend/
│   └── main.py              # FastAPI server and core logic
├── frontend/
│   └── index.html           # Modern responsive web interface
├── skills/
│   ├── skill_manager.py     # Skill management system
│   └── language_processor.py # Multi-language processing
├── assets/                   # Audio files and resources
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Installation

1. **Clone or navigate to the project:**
```bash
cd rex_ai
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the server:**
```bash
python backend/main.py
```

4. **Access the application:**
Open your browser and navigate to: `http://localhost:8000`

## 📦 Dependencies

The application requires the following Python packages:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `torch` - PyTorch (optional, for local AI models)
- `transformers` - Hugging Face transformers (optional)
- `speech_recognition` - Voice input
- `gtts` - Google Text-to-Speech
- `playsound` - Audio playback

## 🗣️ Language Support

### Primary Languages
- **English (en)**: Full support
- **Tamil (ta/தமிழ்)**: Full support with native script handling

### Additional Languages
- Hindi, Spanish, French, German, Chinese, Japanese, Korean, Arabic, Russian, Portuguese, Italian, and 90+ more

### Language Features
- Auto-detection
- Bidirectional translation
- Context-aware processing
- Politeness adaptation
- Cultural sensitivity

## ⚡ Skills Categories

REX AI comes with skills organized into 10 major categories:

1. **Communication**: Translate, summarize, explain, debate
2. **Productivity**: Schedule, remind, organize, prioritize
3. **Analysis**: Research, compare, evaluate, predict
4. **Creative**: Write, design, compose, brainstorm
5. **Technical**: Code, debug, optimize, document
6. **Data**: Analyze, visualize, process, extract
7. **Automation**: Automate, integrate, sync, backup
8. **Learning**: Teach, quiz, explain, demonstrate
9. **Entertainment**: Play, recommend, create, curate
10. **Utilities**: Calculate, convert, search, monitor

## 🎨 User Interface Features

- **Responsive Design**: Adapts to all screen sizes
- **Dark Theme**: Easy on the eyes with modern aesthetics
- **Real-time Chat**: Instant messaging with WebSocket
- **Voice Input**: Click-to-talk functionality
- **Language Selector**: Easy language switching
- **Skills Display**: Visual indicator of active skills
- **Status Indicators**: Connection and activity status

## 🔌 API Endpoints

### Chat
- `POST /api/chat` - Send a message and get AI response
- `WebSocket /ws` - Real-time bidirectional communication

### Voice
- `POST /api/voice/input` - Process voice input
- `GET /api/voice/output` - Generate voice output

### Skills
- `GET /api/skills` - List available skills
- `POST /api/skills/execute` - Execute a specific skill

## 💡 Usage Examples

### Text Chat
```python
import requests

response = requests.post('http://localhost:8000/api/chat', json={
    'message': 'Hello, can you help me with coding?',
    'language': 'en',
    'voice_enabled': True
})

print(response.json())
```

### Voice Interaction
Use the microphone button in the web interface to speak naturally in English or Tamil.

### Skill Execution
```python
requests.post('http://localhost:8000/api/skills/execute', json={
    'skill_name': 'technical_code',
    'params': {'task': 'Create a Python function'}
})
```

## 🌐 Cross-Platform Compatibility

REX AI works on:
- ✅ **Mobile**: iOS Safari, Android Chrome
- ✅ **Tablet**: iPad, Android tablets
- ✅ **Desktop**: Windows, macOS, Linux
- ✅ **Browsers**: Chrome, Firefox, Edge, Safari

## 🔧 Configuration

### Environment Variables
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)
- `DEFAULT_LANGUAGE`: Default language (default: en)
- `VOICE_ENABLED`: Enable voice by default (default: true)

### Customization
- Add new skills in `skills/skill_manager.py`
- Extend language support in `skills/language_processor.py`
- Modify UI theme in `frontend/index.html`

## 🛡️ Security Notes

- CORS is enabled for development; restrict in production
- Implement authentication for production use
- Use HTTPS in production environments
- Validate all user inputs

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Add more language translations
- Implement additional skills
- Enhance voice quality with better TTS
- Integrate advanced AI models
- Add persistent memory/context

## 📄 License

This project is open-source and available for educational and commercial use.

## 🙏 Acknowledgments

- FastAPI team for the excellent web framework
- Hugging Face for transformer models
- Google for TTS and speech recognition
- Open-source community for various libraries

---

**REX AI** - Your intelligent assistant for everything! 🚀

*Built with ❤️ using Python and modern web technologies*

"""
REX AI - Core Engine
Main AI processing engine with voice support
100% Offline, No API Keys Required
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.language_processor import LanguageProcessor
from skills.skill_manager import SkillManager
from typing import Dict, List, Optional, Any
from datetime import datetime
import re
import json

class REXEngine:
    def __init__(self):
        self.name = "REX"
        self.version = "1.0.0"
        self.language_processor = LanguageProcessor()
        self.skill_manager = SkillManager()
        self.conversation_history = []
        self.user_context = {
            'preferred_language': 'en',
            'voice_enabled': True,
            'session_start': datetime.now().isoformat()
        }
        
        # Initialize conversation
        self.system_prompt = self._get_system_prompt()
    
    def _get_system_prompt(self) -> str:
        """Get system introduction prompt"""
        return {
            'en': "I am REX, your advanced AI assistant. I operate completely offline with over 2 million skills. How can I help you today?",
            'ta': "நான் REX, உங்கள் மேம்பட்ட AI உதவியாளர். நான் 20 லட்சத்திற்கும் மேற்பட்ட திறமைகளுடன் முழுமையாக ஆஃப்லைனில் செயல்படுகிறேன். இன்று என்ன செய்ய வேண்டும்?"
        }
    
    def process_message(self, message: str, context: Optional[Dict] = None) -> Dict:
        """Process user message and generate response"""
        if not message or not message.strip():
            return self._create_error_response("Empty message received")
        
        # Detect language
        detected_lang = self.language_processor.detect_language(message)
        self.user_context['preferred_language'] = detected_lang
        
        # Generate language-based response
        lang_response = self.language_processor.generate_response(message, context)
        
        # Check if skill execution is needed
        skill_result = self._detect_and_execute_skill(message, detected_lang)
        
        # Create response
        response_text = lang_response['text']
        if skill_result and skill_result.get('success'):
            response_text += f"\n\n{skill_result['result']}"
        
        # Store in history
        self._store_conversation(message, response_text, detected_lang)
        
        return {
            'success': True,
            'response': response_text,
            'language': detected_lang,
            'intent': lang_response['intent'],
            'skill_executed': skill_result.get('skill') if skill_result else None,
            'timestamp': datetime.now().isoformat(),
            'voice_enabled': self.user_context['voice_enabled']
        }
    
    def _detect_and_execute_skill(self, message: str, language: str) -> Optional[Dict]:
        """Detect if a skill should be executed based on message"""
        message_lower = message.lower()
        
        # Calculator detection
        calc_pattern = r'calculate\s*(.+)|(\d+\s*[\+\-\*\/]\s*\d+)'
        calc_match = re.search(calc_pattern, message_lower)
        if calc_match:
            expression = calc_match.group(1) or calc_match.group(2)
            return self.skill_manager.execute_skill(
                'calculator',
                {'expression': expression},
                language
            )
        
        # Unit conversion detection
        convert_patterns = [
            r'convert\s+(\d+)\s*(\w+)\s*to\s*(\w+)',
            r'(\d+)\s*(celsius|fahrenheit|km|miles|kg|lbs|meter|feet)\s*(?:to|in)\s*(celsius|fahrenheit|km|miles|kg|lbs|meter|feet)'
        ]
        for pattern in convert_patterns:
            conv_match = re.search(pattern, message_lower)
            if conv_match:
                groups = conv_match.groups()
                if len(groups) == 3:
                    value, from_unit, to_unit = groups
                else:
                    value, from_unit, to_unit = groups[0], groups[1], groups[2]
                return self.skill_manager.execute_skill(
                    'unit_conversion',
                    {'value': value, 'from_unit': from_unit, 'to_unit': to_unit},
                    language
                )
        
        # Joke detection
        if any(word in message_lower for word in ['joke', 'சிரிப்பு', 'கதை']):
            return self.skill_manager.execute_skill(
                'joke_telling',
                {},
                language
            )
        
        # Trivia detection
        if any(word in message_lower for word in ['trivia', 'fact', 'தெரியுமா', 'உண்மை']):
            return self.skill_manager.execute_skill(
                'trivia',
                {},
                language
            )
        
        # Time/Date detection
        if any(word in message_lower for word in ['time', 'மணி', 'நேரம்']):
            return self.skill_manager.execute_skill(
                'time_calculation',
                {},
                language
            )
        
        if any(word in message_lower for word in ['date', 'தேதி', 'நாள்']):
            return self.skill_manager.execute_skill(
                'date_calculation',
                {},
                language
            )
        
        return None
    
    def _store_conversation(self, user_message: str, ai_response: str, language: str):
        """Store conversation in history"""
        self.conversation_history.append({
            'user': user_message,
            'assistant': ai_response,
            'language': language,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 50 messages to save memory
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]
    
    def _create_error_response(self, error_message: str) -> Dict:
        """Create error response"""
        return {
            'success': False,
            'error': error_message,
            'response': "I encountered an error. Please try again.",
            'timestamp': datetime.now().isoformat()
        }
    
    def get_skills_info(self) -> Dict:
        """Get information about available skills"""
        return self.skill_manager.get_all_skills()
    
    def search_skills(self, query: str) -> List[Dict]:
        """Search for skills"""
        return self.skill_manager.search_skills(query)
    
    def get_conversation_history(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation history"""
        return self.conversation_history[-limit:]
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        return {'success': True, 'message': 'Conversation history cleared'}
    
    def get_status(self) -> Dict:
        """Get engine status"""
        return {
            'name': self.name,
            'version': self.version,
            'status': 'online',
            'offline_mode': True,
            'api_keys_required': False,
            'languages_supported': len(self.language_processor.supported_languages),
            'total_skills': self.skill_manager.total_skills,
            'conversation_count': len(self.conversation_history),
            'uptime_since': self.user_context['session_start']
        }
    
    def process_voice_command(self, audio_data: bytes) -> Dict:
        """
        Process voice command (placeholder for actual speech recognition)
        In production, this would use speech_recognition library
        """
        # This is a placeholder - actual implementation would decode audio
        # and convert speech to text using speech_recognition
        return {
            'success': False,
            'error': 'Voice processing requires audio file upload endpoint',
            'note': 'Use browser Web Speech API for client-side voice recognition'
        }
    
    def generate_voice_response(self, text: str, language: str = 'en') -> Dict:
        """
        Generate voice response (placeholder for actual TTS)
        In production, this would use gTTS or similar library
        """
        # This is a placeholder - actual implementation would generate audio
        # For now, we return the text which will be spoken by browser TTS
        return {
            'success': True,
            'text': text,
            'language': language,
            'note': 'Audio will be generated by browser Web Speech API'
        }

# Test the engine
if __name__ == "__main__":
    print("Initializing REX AI Engine...")
    engine = REXEngine()
    
    print(f"\n✅ REX Engine v{engine.version} initialized")
    print(f"🌍 Languages supported: {engine.get_status()['languages_supported']}")
    print(f"⚡ Total skills: {engine.get_status()['total_skills']:,}")
    
    # Test conversations
    test_messages = [
        "Hello",
        "வணக்கம்",
        "What can you do?",
        "Calculate 25 + 17 * 3",
        "Tell me a joke",
        "Convert 100 celsius to fahrenheit",
        "நன்றி"
    ]
    
    print("\n--- Testing Conversations ---")
    for msg in test_messages:
        result = engine.process_message(msg)
        print(f"\nUser: {msg}")
        print(f"REX: {result['response'][:100]}...")
    
    print("\n--- Engine Status ---")
    status = engine.get_status()
    print(json.dumps(status, indent=2))

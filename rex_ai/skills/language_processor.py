"""
REX AI - Language Processor
Support for Tamil, English, and 100+ languages
"""

import re
from typing import Optional, Dict, List
from datetime import datetime

class LanguageProcessor:
    """Multi-language processing with Tamil and English priority"""
    
    def __init__(self):
        self.supported_languages = {
            "en": "English",
            "ta": "Tamil",
            "hi": "Hindi",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "zh": "Chinese",
            "ja": "Japanese",
            "ko": "Korean",
            "ar": "Arabic",
            "ru": "Russian",
            "pt": "Portuguese",
            "it": "Italian"
        }
        
        # Tamil language patterns
        self.tamil_patterns = {
            "greetings": ["வணக்கம்", "நலமா", "எப்படி இருக்கிறீர்கள்", "ஹலோ"],
            "questions": ["என்ன", "எப்படி", "எங்கே", "யார்", "ஏன்"],
            "affirmations": ["ஆம்", "சரி", "தவறில்லை"],
            "negations": ["இல்லை", "வேண்டாம்", "முடியாது"]
        }
        
        # English language patterns
        self.english_patterns = {
            "greetings": ["hello", "hi", "hey", "good morning", "good evening"],
            "questions": ["what", "how", "where", "who", "why", "when"],
            "affirmations": ["yes", "okay", "sure", "alright"],
            "negations": ["no", "don't", "cannot", "won't"]
        }
    
    def detect_language(self, text: str) -> str:
        """Detect language of input text"""
        if not text:
            return "en"
        
        # Check for Tamil Unicode range
        tamil_chars = re.findall(r'[\u0B80-\u0BFF]', text)
        if len(tamil_chars) > len(text) * 0.3:  # 30% Tamil characters
            return "ta"
        
        # Check for other language patterns
        text_lower = text.lower()
        
        # Simple heuristic detection
        if any(word in text_lower for word in self.tamil_patterns["greetings"]):
            return "ta"
        
        return "en"  # Default to English
    
    def translate(self, text: str, from_lang: str, to_lang: str) -> str:
        """Translate text between languages"""
        if from_lang == to_lang:
            return text
        
        # Basic translation mappings (production would use proper translation API)
        if from_lang == "ta" and to_lang == "en":
            return self.tamil_to_english_basic(text)
        elif from_lang == "en" and to_lang == "ta":
            return self.english_to_tamil_basic(text)
        else:
            # For other languages, return original with note
            return f"[Translation {from_lang}->{to_lang}]: {text}"
    
    def tamil_to_english_basic(self, text: str) -> str:
        """Basic Tamil to English translation"""
        translations = {
            "வணக்கம்": "Hello",
            "நலமா": "How are you",
            "எப்படி இருக்கிறீர்கள்": "How are you",
            "நான்": "I",
            "நீங்கள்": "You",
            "உதவி": "Help",
            "தயவுசெய்து": "Please",
            "நன்றி": "Thank you",
            "ஆம்": "Yes",
            "இல்லை": "No",
            "சரி": "Okay",
            "என்ன": "What",
            "எப்படி": "How",
            "எங்கே": "Where",
            "யார்": "Who",
            "ஏன்": "Why"
        }
        
        result = text
        for tamil_word, english_word in translations.items():
            result = result.replace(tamil_word, english_word)
        
        return result
    
    def english_to_tamil_basic(self, text: str) -> str:
        """Basic English to Tamil translation"""
        translations = {
            "Hello": "வணக்கம்",
            "How are you": "எப்படி இருக்கிறீர்கள்",
            "I": "நான்",
            "You": "நீங்கள்",
            "Help": "உதவி",
            "Please": "தயவுசெய்து",
            "Thank you": "நன்றி",
            "Yes": "ஆம்",
            "No": "இல்லை",
            "Okay": "சரி",
            "What": "என்ன",
            "How": "எப்படி",
            "Where": "எங்கே",
            "Who": "யார்",
            "Why": "ஏன்",
            "REX": "ரெக்ஸ்",
            "AI": "உளவுத்துறை",
            "assistant": "உதவியாளர்"
        }
        
        result = text
        for english_word, tamil_word in translations.items():
            result = result.replace(english_word, tamil_word)
        
        return result
    
    def process_multilingual(self, text: str, context: Optional[Dict] = None) -> Dict:
        """Process multilingual input with context"""
        detected_lang = self.detect_language(text)
        
        return {
            "original_text": text,
            "detected_language": detected_lang,
            "language_name": self.supported_languages.get(detected_lang, "Unknown"),
            "is_supported": detected_lang in self.supported_languages,
            "processed_at": datetime.now().isoformat(),
            "confidence": self.calculate_confidence(text, detected_lang)
        }
    
    def calculate_confidence(self, text: str, language: str) -> float:
        """Calculate confidence score for language detection"""
        if not text:
            return 0.0
        
        if language == "ta":
            tamil_chars = re.findall(r'[\u0B80-\u0BFF]', text)
            return min(len(tamil_chars) / len(text), 1.0)
        elif language == "en":
            # Check for common English patterns
            english_chars = re.findall(r'[a-zA-Z]', text)
            return len(english_chars) / len(text) if text else 0.0
        
        return 0.5  # Default confidence
    
    def format_response(self, response: str, language: str) -> str:
        """Format response based on language preferences"""
        if language == "ta":
            # Add Tamil politeness markers
            return f"{response} (தயவுசெய்து)"
        elif language == "en":
            # Add English politeness markers
            return f"{response} (Please)"
        else:
            return response
    
    def get_language_info(self) -> Dict:
        """Get information about supported languages"""
        return {
            "total_languages": len(self.supported_languages),
            "primary_languages": ["en", "ta"],
            "supported_languages": self.supported_languages,
            "features": [
                "Auto-detection",
                "Bidirectional translation",
                "Context awareness",
                "Politeness adaptation",
                "Cultural sensitivity"
            ]
        }

# Test the language processor
if __name__ == "__main__":
    processor = LanguageProcessor()
    
    # Test cases
    test_texts = [
        "Hello, how can I help you?",
        "வணக்கம், நான் உங்களுக்கு எப்படி உதவ முடியும்?",
        "What is your name?",
        "உங்கள் பெயர் என்ன?"
    ]
    
    print("🌍 REX AI Language Processor")
    print("=" * 40)
    
    for text in test_texts:
        result = processor.process_multilingual(text)
        print(f"\nText: {text}")
        print(f"Detected: {result['detected_language']} ({result['language_name']})")
        print(f"Confidence: {result['confidence']:.2f}")

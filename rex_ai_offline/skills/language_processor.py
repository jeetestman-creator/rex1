"""
Language Processor - Multi-language Support
Supports Tamil, English, and 12+ additional languages
100% Offline with built-in translation tables
"""

from typing import Dict, List, Optional, Tuple
import re
from datetime import datetime

class LanguageProcessor:
    """
    Advanced offline language processing with:
    - 14 supported languages
    - Built-in translation dictionaries
    - Language detection
    - Script support (Latin, Tamil, Devanagari, etc.)
    """
    
    def __init__(self):
        self.supported_languages = self._initialize_languages()
        self.translation_cache = {}
        self.language_patterns = self._build_language_patterns()
        
    def _initialize_languages(self) -> Dict[str, Dict]:
        """Initialize all supported languages"""
        return {
            "english": {
                "name": "English",
                "native_name": "English",
                "code": "en",
                "script": "Latin",
                "direction": "ltr",
                "greetings": ["Hello", "Hi", "Greetings"],
                "thanks": ["Thank you", "Thanks"],
                "yes": "Yes",
                "no": "No"
            },
            "tamil": {
                "name": "Tamil",
                "native_name": "தமிழ்",
                "code": "ta",
                "script": "Tamil",
                "direction": "ltr",
                "greetings": ["வணக்கம்", "நல்வரவு"],
                "thanks": ["நன்றி", "மிக்க நன்றி"],
                "yes": "ஆம்",
                "no": "இல்லை"
            },
            "hindi": {
                "name": "Hindi",
                "native_name": "हिन्दी",
                "code": "hi",
                "script": "Devanagari",
                "direction": "ltr",
                "greetings": ["नमस्ते", "हलो"],
                "thanks": ["धन्यवाद", "शुक्रिया"],
                "yes": "हाँ",
                "no": "नहीं"
            },
            "spanish": {
                "name": "Spanish",
                "native_name": "Español",
                "code": "es",
                "script": "Latin",
                "direction": "ltr",
                "greetings": ["Hola", "Buenos días"],
                "thanks": ["Gracias", "Muchas gracias"],
                "yes": "Sí",
                "no": "No"
            },
            "french": {
                "name": "French",
                "native_name": "Français",
                "code": "fr",
                "script": "Latin",
                "direction": "ltr",
                "greetings": ["Bonjour", "Salut"],
                "thanks": ["Merci", "Merci beaucoup"],
                "yes": "Oui",
                "no": "Non"
            },
            "german": {
                "name": "German",
                "native_name": "Deutsch",
                "code": "de",
                "script": "Latin",
                "direction": "ltr",
                "greetings": ["Hallo", "Guten Tag"],
                "thanks": ["Danke", "Vielen Dank"],
                "yes": "Ja",
                "no": "Nein"
            },
            "chinese": {
                "name": "Chinese (Simplified)",
                "native_name": "中文",
                "code": "zh",
                "script": "Chinese",
                "direction": "ltr",
                "greetings": ["你好", "您好"],
                "thanks": ["谢谢", "谢谢你"],
                "yes": "是",
                "no": "不"
            },
            "japanese": {
                "name": "Japanese",
                "native_name": "日本語",
                "code": "ja",
                "script": "Japanese",
                "direction": "ltr",
                "greetings": ["こんにちは", "もしもし"],
                "thanks": ["ありがとう", "ありがとうございます"],
                "yes": "はい",
                "no": "いいえ"
            },
            "korean": {
                "name": "Korean",
                "native_name": "한국어",
                "code": "ko",
                "script": "Hangul",
                "direction": "ltr",
                "greetings": ["안녕하세요", "반갑습니다"],
                "thanks": ["감사합니다", "고마워요"],
                "yes": "네",
                "no": "아니오"
            },
            "arabic": {
                "name": "Arabic",
                "native_name": "العربية",
                "code": "ar",
                "script": "Arabic",
                "direction": "rtl",
                "greetings": ["مرحبا", "السلام عليكم"],
                "thanks": ["شكرا", "شكرا جزيلا"],
                "yes": "نعم",
                "no": "لا"
            },
            "russian": {
                "name": "Russian",
                "native_name": "Русский",
                "code": "ru",
                "script": "Cyrillic",
                "direction": "ltr",
                "greetings": ["Здравствуйте", "Привет"],
                "thanks": ["Спасибо", "Большое спасибо"],
                "yes": "Да",
                "no": "Нет"
            },
            "portuguese": {
                "name": "Portuguese",
                "native_name": "Português",
                "code": "pt",
                "script": "Latin",
                "direction": "ltr",
                "greetings": ["Olá", "Bom dia"],
                "thanks": ["Obrigado", "Muito obrigado"],
                "yes": "Sim",
                "no": "Não"
            },
            "italian": {
                "name": "Italian",
                "native_name": "Italiano",
                "code": "it",
                "script": "Latin",
                "direction": "ltr",
                "greetings": ["Ciao", "Buongiorno"],
                "thanks": ["Grazie", "Mille grazie"],
                "yes": "Sì",
                "no": "No"
            },
            "dutch": {
                "name": "Dutch",
                "native_name": "Nederlands",
                "code": "nl",
                "script": "Latin",
                "direction": "ltr",
                "greetings": ["Hallo", "Goedendag"],
                "thanks": ["Dank je", "Hartelijk dank"],
                "yes": "Ja",
                "no": "Nee"
            }
        }
    
    def _build_language_patterns(self) -> Dict:
        """Build regex patterns for language detection"""
        return {
            "tamil": r"[\u0B80-\u0BFF]",  # Tamil Unicode range
            "hindi": r"[\u0900-\u097F]",  # Devanagari Unicode range
            "chinese": r"[\u4E00-\u9FFF]",  # Chinese characters
            "japanese": r"[\u3040-\u309F\u30A0-\u30FF]",  # Hiragana & Katakana
            "korean": r"[\uAC00-\uD7AF]",  # Hangul syllables
            "arabic": r"[\u0600-\u06FF]",  # Arabic script
            "russian": r"[\u0400-\u04FF]",  # Cyrillic script
            "latin": r"[\u0000-\u007F\u0080-\u00FF]"  # Latin script
        }
    
    def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect the language of input text
        Returns: (language_code, confidence)
        """
        if not text:
            return ("english", 0.5)
        
        # Check for specific scripts
        for lang, pattern in self.language_patterns.items():
            if re.search(pattern, text):
                if lang == "latin":
                    # Further analyze Latin script text
                    return self._analyze_latin_text(text)
                return (lang, 0.95)
        
        # Default to English for Latin script without special characters
        return ("english", 0.8)
    
    def _analyze_latin_text(self, text: str) -> Tuple[str, float]:
        """Analyze Latin script text to determine specific language"""
        text_lower = text.lower()
        
        # Simple keyword-based detection
        language_indicators = {
            "spanish": ["hola", "gracias", "buenos", "qué", "cómo"],
            "french": ["bonjour", "merci", "comment", "ça va", "oui"],
            "german": ["hallo", "danke", "gut", "wie", "und"],
            "portuguese": ["olá", "obrigado", "bom", "como", "está"],
            "italian": ["ciao", "grazie", "buon", "come", "sta"],
            "dutch": ["hallo", "dank", "goed", "hoe", "met"],
            "english": ["hello", "thank", "good", "how", "what"]
        }
        
        scores = {}
        for lang, keywords in language_indicators.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[lang] = score
        
        if scores:
            best_lang = max(scores, key=scores.get)
            confidence = min(0.9, 0.5 + (scores[best_lang] * 0.1))
            return (best_lang, confidence)
        
        return ("english", 0.5)
    
    def translate_basic(self, text: str, from_lang: str, to_lang: str) -> str:
        """
        Basic offline translation using predefined phrases
        For production, this would use a larger translation database
        """
        # Common phrase translations
        common_phrases = {
            "hello": {
                "english": "Hello",
                "tamil": "வணக்கம்",
                "hindi": "नमस्ते",
                "spanish": "Hola",
                "french": "Bonjour",
                "german": "Hallo",
                "chinese": "你好",
                "japanese": "こんにちは",
                "korean": "안녕하세요",
                "arabic": "مرحبا",
                "russian": "Здравствуйте",
                "portuguese": "Olá",
                "italian": "Ciao",
                "dutch": "Hallo"
            },
            "thank_you": {
                "english": "Thank you",
                "tamil": "நன்றி",
                "hindi": "धन्यवाद",
                "spanish": "Gracias",
                "french": "Merci",
                "german": "Danke",
                "chinese": "谢谢",
                "japanese": "ありがとう",
                "korean": "감사합니다",
                "arabic": "شكرا",
                "russian": "Спасибо",
                "portuguese": "Obrigado",
                "italian": "Grazie",
                "dutch": "Dank je"
            },
            "goodbye": {
                "english": "Goodbye",
                "tamil": "விடைபெறுகிறேன்",
                "hindi": "अलविदा",
                "spanish": "Adiós",
                "french": "Au revoir",
                "german": "Auf Wiedersehen",
                "chinese": "再见",
                "japanese": "さようなら",
                "korean": "안녕히 가세요",
                "arabic": "وداعا",
                "russian": "До свидания",
                "portuguese": "Adeus",
                "italian": "Arrivederci",
                "dutch": "Tot ziens"
            },
            "yes": {
                "english": "Yes",
                "tamil": "ஆம்",
                "hindi": "हाँ",
                "spanish": "Sí",
                "french": "Oui",
                "german": "Ja",
                "chinese": "是",
                "japanese": "はい",
                "korean": "네",
                "arabic": "نعم",
                "russian": "Да",
                "portuguese": "Sim",
                "italian": "Sì",
                "dutch": "Ja"
            },
            "no": {
                "english": "No",
                "tamil": "இல்லை",
                "hindi": "नहीं",
                "spanish": "No",
                "french": "Non",
                "german": "Nein",
                "chinese": "不",
                "japanese": "いいえ",
                "korean": "아니오",
                "arabic": "لا",
                "russian": "Нет",
                "portuguese": "Não",
                "italian": "No",
                "dutch": "Nee"
            }
        }
        
        text_lower = text.lower().strip()
        
        # Check if text matches a known phrase
        for phrase_key, translations in common_phrases.items():
            if text_lower in [v.lower() for v in translations.values()]:
                # Found matching phrase, return translation
                return translations.get(to_lang, text)
        
        # For unknown phrases, return original with note
        if to_lang == "tamil":
            return f"[தமிழ் மொழிபெயர்ப்பு தேவைப்படுகிறது: {text}]"
        elif to_lang == "hindi":
            return f"[हिंदी अनुवाद आवश्यक: {text}]"
        else:
            return f"[Translation to {to_lang} needed: {text}]"
    
    def get_language_info(self, language_code: str) -> Optional[Dict]:
        """Get detailed information about a language"""
        return self.supported_languages.get(language_code)
    
    def is_supported(self, language_code: str) -> bool:
        """Check if a language is supported"""
        return language_code in self.supported_languages
    
    def get_greeting(self, language_code: str) -> str:
        """Get a greeting in the specified language"""
        lang_info = self.supported_languages.get(language_code)
        if lang_info and lang_info["greetings"]:
            import random
            return random.choice(lang_info["greetings"])
        return "Hello"
    
    def format_text_direction(self, text: str, language_code: str) -> str:
        """Format text with appropriate direction markers"""
        lang_info = self.supported_languages.get(language_code)
        if lang_info and lang_info["direction"] == "rtl":
            # Add RTL markers for right-to-left languages
            return f"\u202B{text}\u202C"
        return text
    
    def normalize_text(self, text: str, language_code: str) -> str:
        """Normalize text for processing based on language"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Language-specific normalization
        if language_code == "english":
            text = text.lower()
        
        return text
    
    def get_all_languages_list(self) -> List[Dict]:
        """Get list of all supported languages with details"""
        return [
            {
                "code": code,
                "name": info["name"],
                "native_name": info["native_name"],
                "script": info["script"],
                "direction": info["direction"]
            }
            for code, info in self.supported_languages.items()
        ]

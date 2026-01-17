import os
import httpx
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="TranslateGemma Web")

# Add CORS middleware for Chrome extension support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for extension compatibility
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Supported languages with their codes
LANGUAGES = [
    {"code": "en", "name": "English", "nativeName": "English"},
    {"code": "zh-Hans", "name": "Chinese (Simplified)", "nativeName": "简体中文"},
    {"code": "zh-Hant", "name": "Chinese (Traditional)", "nativeName": "繁體中文"},
    {"code": "ja", "name": "Japanese", "nativeName": "日本語"},
    {"code": "ko", "name": "Korean", "nativeName": "한국어"},
    {"code": "es", "name": "Spanish", "nativeName": "Español"},
    {"code": "fr", "name": "French", "nativeName": "Français"},
    {"code": "de", "name": "German", "nativeName": "Deutsch"},
    {"code": "it", "name": "Italian", "nativeName": "Italiano"},
    {"code": "pt", "name": "Portuguese", "nativeName": "Português"},
    {"code": "ru", "name": "Russian", "nativeName": "Русский"},
    {"code": "ar", "name": "Arabic", "nativeName": "العربية"},
    {"code": "hi", "name": "Hindi", "nativeName": "हिन्दी"},
    {"code": "th", "name": "Thai", "nativeName": "ไทย"},
    {"code": "vi", "name": "Vietnamese", "nativeName": "Tiếng Việt"},
    {"code": "id", "name": "Indonesian", "nativeName": "Bahasa Indonesia"},
    {"code": "ms", "name": "Malay", "nativeName": "Bahasa Melayu"},
    {"code": "tl", "name": "Filipino", "nativeName": "Filipino"},
    {"code": "nl", "name": "Dutch", "nativeName": "Nederlands"},
    {"code": "pl", "name": "Polish", "nativeName": "Polski"},
    {"code": "tr", "name": "Turkish", "nativeName": "Türkçe"},
    {"code": "uk", "name": "Ukrainian", "nativeName": "Українська"},
    {"code": "cs", "name": "Czech", "nativeName": "Čeština"},
    {"code": "sv", "name": "Swedish", "nativeName": "Svenska"},
    {"code": "da", "name": "Danish", "nativeName": "Dansk"},
    {"code": "fi", "name": "Finnish", "nativeName": "Suomi"},
    {"code": "no", "name": "Norwegian", "nativeName": "Norsk"},
    {"code": "el", "name": "Greek", "nativeName": "Ελληνικά"},
    {"code": "he", "name": "Hebrew", "nativeName": "עברית"},
    {"code": "hu", "name": "Hungarian", "nativeName": "Magyar"},
    {"code": "ro", "name": "Romanian", "nativeName": "Română"},
    {"code": "bg", "name": "Bulgarian", "nativeName": "Български"},
    {"code": "hr", "name": "Croatian", "nativeName": "Hrvatski"},
    {"code": "sk", "name": "Slovak", "nativeName": "Slovenčina"},
    {"code": "sl", "name": "Slovenian", "nativeName": "Slovenščina"},
    {"code": "sr", "name": "Serbian", "nativeName": "Српски"},
    {"code": "lt", "name": "Lithuanian", "nativeName": "Lietuvių"},
    {"code": "lv", "name": "Latvian", "nativeName": "Latviešu"},
    {"code": "et", "name": "Estonian", "nativeName": "Eesti"},
    {"code": "bn", "name": "Bengali", "nativeName": "বাংলা"},
    {"code": "ta", "name": "Tamil", "nativeName": "தமிழ்"},
    {"code": "te", "name": "Telugu", "nativeName": "తెలుగు"},
    {"code": "mr", "name": "Marathi", "nativeName": "मराठी"},
    {"code": "gu", "name": "Gujarati", "nativeName": "ગુજરાતી"},
    {"code": "kn", "name": "Kannada", "nativeName": "ಕನ್ನಡ"},
    {"code": "ml", "name": "Malayalam", "nativeName": "മലയാളം"},
    {"code": "pa", "name": "Punjabi", "nativeName": "ਪੰਜਾਬੀ"},
    {"code": "ur", "name": "Urdu", "nativeName": "اردو"},
    {"code": "fa", "name": "Persian", "nativeName": "فارسی"},
    {"code": "sw", "name": "Swahili", "nativeName": "Kiswahili"},
    {"code": "af", "name": "Afrikaans", "nativeName": "Afrikaans"},
    {"code": "ca", "name": "Catalan", "nativeName": "Català"},
    {"code": "eu", "name": "Basque", "nativeName": "Euskara"},
    {"code": "gl", "name": "Galician", "nativeName": "Galego"},
]

class TranslateRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str
    model: str = "translategemma:4b"

class TranslateResponse(BaseModel):
    translated_text: str

# Available models
AVAILABLE_MODELS = [
    {"id": "translategemma:4b", "name": "TranslateGemma 4B", "size": "3.3 GB", "description": "快速 · 適合日常翻譯"},
    {"id": "translategemma:12b", "name": "TranslateGemma 12B", "size": "8.1 GB", "description": "高品質 · 更準確的翻譯"},
]

# Immersive Translate API Models
class ImmersiveTranslateRequest(BaseModel):
    source_lang: str
    target_lang: str
    text_list: List[str]

class ImmersiveTranslation(BaseModel):
    detected_source_lang: str
    text: str

class ImmersiveTranslateResponse(BaseModel):
    translations: List[ImmersiveTranslation]

# Language code mapping: Immersive Translate <-> Internal
LANG_CODE_MAP = {
    "zh-CN": "zh-Hans",
    "zh-TW": "zh-Hant",
    "auto": "en",  # Default to English for auto detection
}

REVERSE_LANG_CODE_MAP = {v: k for k, v in LANG_CODE_MAP.items() if k != "auto"}

def convert_lang_code(code: str, to_internal: bool = True) -> str:
    """Convert language codes between Immersive Translate and internal format"""
    if to_internal:
        return LANG_CODE_MAP.get(code, code)
    else:
        return REVERSE_LANG_CODE_MAP.get(code, code)

def get_language_name(code: str) -> str:
    """Get language name from code"""
    for lang in LANGUAGES:
        if lang["code"] == code:
            return lang["name"]
    return code

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.get("/api/languages")
async def get_languages():
    """Get list of supported languages"""
    return {"languages": LANGUAGES}

@app.get("/api/models")
async def get_models():
    """Get list of available models"""
    # Check which models are actually installed
    installed_models = []
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{OLLAMA_HOST}/api/tags")
            if response.status_code == 200:
                result = response.json()
                installed_names = [m["name"] for m in result.get("models", [])]
                for model in AVAILABLE_MODELS:
                    model_info = model.copy()
                    model_info["installed"] = model["id"] in installed_names
                    installed_models.append(model_info)
    except Exception:
        installed_models = AVAILABLE_MODELS
    return {"models": installed_models}

@app.post("/api/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest):
    """Translate text using TranslateGemma"""
    if not request.text.strip():
        return TranslateResponse(translated_text="")
    
    source_name = get_language_name(request.source_lang)
    target_name = get_language_name(request.target_lang)
    
    # Build the prompt according to TranslateGemma format
    prompt = f"""You are a professional {source_name} ({request.source_lang}) to {target_name} ({request.target_lang}) translator. Your goal is to accurately convey the meaning and nuances of the original {source_name} text while adhering to {target_name} grammar, vocabulary, and cultural sensitivities. Produce only the {target_name} translation, without any additional explanations or commentary. Please translate the following {source_name} text into {target_name}:


{request.text}"""

    try:
        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                f"{OLLAMA_HOST}/api/generate",
                json={
                    "model": request.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "top_p": 0.9,
                    }
                }
            )
            response.raise_for_status()
            result = response.json()
            translated_text = result.get("response", "").strip()
            return TranslateResponse(translated_text=translated_text)
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Translation request timed out")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Ollama error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/immersive-translate", response_model=ImmersiveTranslateResponse)
async def immersive_translate(
    request: ImmersiveTranslateRequest,
    model: str = Query(default="translategemma:4b", description="Model to use for translation")
):
    """
    Immersive Translate Custom API compatible endpoint.
    Translates a list of texts from source to target language.
    """
    if not request.text_list:
        return ImmersiveTranslateResponse(translations=[])
    
    # Convert language codes
    internal_source = convert_lang_code(request.source_lang, to_internal=True)
    internal_target = convert_lang_code(request.target_lang, to_internal=True)
    
    source_name = get_language_name(internal_source)
    target_name = get_language_name(internal_target)
    
    # For auto detection, we'll assume the source is different from target
    detected_source = request.source_lang if request.source_lang != "auto" else "en"
    
    translations = []
    
    for text in request.text_list:
        if not text.strip():
            translations.append(ImmersiveTranslation(
                detected_source_lang=detected_source,
                text=""
            ))
            continue
        
        # Build the prompt according to TranslateGemma format
        prompt = f"""You are a professional {source_name} ({internal_source}) to {target_name} ({internal_target}) translator. Your goal is to accurately convey the meaning and nuances of the original {source_name} text while adhering to {target_name} grammar, vocabulary, and cultural sensitivities. Produce only the {target_name} translation, without any additional explanations or commentary. Please translate the following {source_name} text into {target_name}:


{text}"""

        try:
            async with httpx.AsyncClient(timeout=180.0) as client:
                response = await client.post(
                    f"{OLLAMA_HOST}/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.1,
                            "top_p": 0.9,
                        }
                    }
                )
                response.raise_for_status()
                result = response.json()
                translated_text = result.get("response", "").strip()
                translations.append(ImmersiveTranslation(
                    detected_source_lang=detected_source,
                    text=translated_text
                ))
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Translation request timed out")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=502, detail=f"Ollama error: {e.response.text}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return ImmersiveTranslateResponse(translations=translations)

# OpenAI-compatible API Models
class OpenAIChatMessage(BaseModel):
    role: str
    content: str

class OpenAIChatRequest(BaseModel):
    model: str = "translategemma:4b"
    messages: List[OpenAIChatMessage]
    temperature: Optional[float] = 0.1
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False

class OpenAIChatChoice(BaseModel):
    index: int
    message: OpenAIChatMessage
    finish_reason: str

class OpenAIChatResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[OpenAIChatChoice]

@app.post("/v1/chat/completions", response_model=OpenAIChatResponse)
async def openai_chat_completions(request: OpenAIChatRequest):
    """
    OpenAI Chat Completions compatible endpoint for Immersive Translate.
    Parses translation requests from the messages and returns translated text.
    """
    import time
    import re
    
    # Extract the text to translate from messages
    text_to_translate = ""
    source_lang = "en"
    target_lang = "zh-Hant"
    
    for msg in request.messages:
        if msg.role == "system":
            # Try to parse source/target language from system prompt
            # Common patterns: "translate from English to Chinese" or similar
            content_lower = msg.content.lower()
            if "chinese" in content_lower or "中文" in msg.content:
                target_lang = "zh-Hant"
            if "english" in content_lower:
                source_lang = "en"
        elif msg.role == "user":
            text_to_translate = msg.content
    
    if not text_to_translate.strip():
        return OpenAIChatResponse(
            id=f"chatcmpl-{int(time.time())}",
            created=int(time.time()),
            model=request.model,
            choices=[OpenAIChatChoice(
                index=0,
                message=OpenAIChatMessage(role="assistant", content=""),
                finish_reason="stop"
            )]
        )
    
    # Map model names
    model = request.model
    if model not in ["translategemma:4b", "translategemma:12b"]:
        model = "translategemma:4b"  # Default to 4b
    
    source_name = get_language_name(source_lang)
    target_name = get_language_name(target_lang)
    
    # Build translation prompt
    prompt = f"""You are a professional {source_name} ({source_lang}) to {target_name} ({target_lang}) translator. Your goal is to accurately convey the meaning and nuances of the original {source_name} text while adhering to {target_name} grammar, vocabulary, and cultural sensitivities. Produce only the {target_name} translation, without any additional explanations or commentary. Please translate the following {source_name} text into {target_name}:


{text_to_translate}"""

    try:
        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                f"{OLLAMA_HOST}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": request.temperature or 0.1,
                        "top_p": 0.9,
                    }
                }
            )
            response.raise_for_status()
            result = response.json()
            translated_text = result.get("response", "").strip()
            
            return OpenAIChatResponse(
                id=f"chatcmpl-{int(time.time())}",
                created=int(time.time()),
                model=model,
                choices=[OpenAIChatChoice(
                    index=0,
                    message=OpenAIChatMessage(role="assistant", content=translated_text),
                    finish_reason="stop"
                )]
            )
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Translation request timed out")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Ollama error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")



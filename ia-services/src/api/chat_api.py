from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import sys
import os

# Agregar el path para importar el chat_bot
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chat_bot.chat_bot import chat_manager
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="NeuraTask Chat Bot API",
    description="API para interactuar con el sistema de IA usando OpenRouter",
    version="1.0.0"
)

# Modelos Pydantic para las requests
class SimpleMessage(BaseModel):
    message: str
    system_prompt: Optional[str] = None

class ConversationMessage(BaseModel):
    role: str  # "user", "assistant", "system"
    content: str

class ConversationRequest(BaseModel):
    messages: List[ConversationMessage]

class AnalysisRequest(BaseModel):
    text: str
    analysis_type: str = "sentiment"  # sentiment, summary, keywords, classification

class StructuredRequest(BaseModel):
    message: str
    system_prompt: Optional[str] = None

# Endpoints
@app.get("/")
async def root():
    """Endpoint de salud de la API"""
    return {"message": "NeuraTask Chat Bot API is running", "status": "healthy"}

@app.post("/chat/simple")
async def simple_chat(request: SimpleMessage):
    """
    Envía un mensaje simple al chatbot
    """
    try:
        response = chat_manager.simple_chat(
            user_message=request.message,
            system_prompt=request.system_prompt
        )
        
        return {
            "success": True,
            "response": response,
            "message": "Chat completed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error in simple_chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/conversation")
async def conversation_chat(request: ConversationRequest):
    """
    Mantiene una conversación con múltiples mensajes
    """
    try:
        # Convertir los mensajes de Pydantic a dict
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        response = chat_manager.conversation_chat(messages)
        
        return {
            "success": True,
            "response": response,
            "message": "Conversation completed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error in conversation_chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/structured")
async def structured_response(request: StructuredRequest):
    """
    Solicita una respuesta estructurada en formato JSON
    """
    try:
        response = chat_manager.structured_response(
            user_message=request.message,
            system_prompt=request.system_prompt
        )
        
        return {
            "success": True,
            "structured_response": response,
            "message": "Structured response completed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error in structured_response endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/text")
async def analyze_text(request: AnalysisRequest):
    """
    Analiza un texto según el tipo especificado
    """
    try:
        analysis = chat_manager.analyze_text(
            text=request.text,
            analysis_type=request.analysis_type
        )
        
        return {
            "success": True,
            "analysis": analysis,
            "analysis_type": request.analysis_type,
            "message": "Text analysis completed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error in analyze_text endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models/available")
async def get_available_models():
    """
    Lista los modelos disponibles (información estática por ahora)
    """
    models = [
        "deepseek/deepseek-r1-distill-llama-70b:free",
        "meta-llama/llama-3.2-3b-instruct:free",
        "microsoft/phi-3-mini-128k-instruct:free",
        "google/gemma-2-9b-it:free"
    ]
    
    return {
        "success": True,
        "available_models": models,
        "current_model": chat_manager.client.model
    }

@app.get("/health")
async def health_check():
    """
    Endpoint de verificación de salud del servicio
    """
    try:
        # Probar una request simple para verificar que la API de OpenRouter funciona
        test_response = chat_manager.simple_chat("Hello", "Respond with 'OK'")
        
        return {
            "status": "healthy",
            "api_status": "connected",
            "model": chat_manager.client.model,
            "test_response": test_response[:50] + "..." if len(test_response) > 50 else test_response
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "api_status": "disconnected",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

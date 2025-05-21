from typing import List, Dict, Optional
from pydantic import BaseModel

class ChatMessage(BaseModel):
    """Modelo para un mensaje en una conversación de chat"""
    role: str  # "system", "user" o "assistant"
    content: str

class ChatRequest(BaseModel):
    """Modelo para una solicitud de chat"""
    messages: List[ChatMessage]
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    response_format: Optional[Dict] = None

class ChatResponse(BaseModel):
    """Modelo para una respuesta de chat"""
    message: ChatMessage
    usage: Optional[Dict] = None

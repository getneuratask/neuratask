from typing import Protocol, List, Dict, Any
from src.domain.schemas.chatbot_entity import ChatMessage, ChatResponse, ChatRequest

class ChatbotService(Protocol):
    """
    Puerto (interfaz) para el servicio de chatbot
    """
    def generate_chat_response(self, chat_request: ChatRequest) -> ChatResponse:
        """
        Genera una respuesta para una solicitud de chat.
        
        Args:
            chat_request: La solicitud de chat con los mensajes y parámetros
            
        Returns:
            Una respuesta de chat con el mensaje generado
        """
        ...

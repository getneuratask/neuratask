from typing import Dict, Any
from src.domain.schemas.chatbot_entity import ChatMessage, ChatResponse, ChatRequest
from src.utils.OpenRouter import OpenRouterAPI
from src.ports.drivers.chatbot_service import ChatbotService

class ChatbotServiceImpl(ChatbotService):
    """
    Implementación del servicio de chatbot utilizando OpenRouter
    """
    
    def __init__(self, openrouter_api: OpenRouterAPI = None):
        """
        Inicializa el servicio con una instancia de OpenRouterAPI.
        Si no se proporciona, crea una nueva.
        
        Args:
            openrouter_api: Una instancia opcional de OpenRouterAPI
        """
        self.openrouter_api = openrouter_api or OpenRouterAPI()
    
    def generate_chat_response(self, chat_request: ChatRequest) -> ChatResponse:
        """
        Genera una respuesta para una solicitud de chat usando OpenRouter.
        
        Args:
            chat_request: La solicitud de chat con los mensajes y parámetros
            
        Returns:
            Una respuesta de chat con el mensaje generado
        """
        # Prepara los mensajes en el formato que espera OpenRouter
        messages = [message.dict() for message in chat_request.messages]
        
        # Prepara los parámetros opcionales para OpenRouter
        params = {}
        if chat_request.model:
            params["model"] = chat_request.model
        if chat_request.temperature:
            params["temperature"] = chat_request.temperature
        if chat_request.max_tokens:
            params["max_tokens"] = chat_request.max_tokens
        if chat_request.response_format:
            params["response_format"] = chat_request.response_format
        
        # Crea una instancia de OpenRouterAPI con los parámetros personalizados si es necesario
        api = self.openrouter_api
        if params:
            api = OpenRouterAPI(**params)
        
        # Envía la solicitud a OpenRouter
        response = api.send_request(messages, response_format=chat_request.response_format)
        
        # Extrae y formatea la respuesta
        ai_message = response['choices'][0]['message']
        chat_message = ChatMessage(
            role=ai_message.get('role', 'assistant'),
            content=ai_message.get('content', '')
        )
        
        # Crea y retorna la respuesta del chat
        return ChatResponse(
            message=chat_message,
            usage=response.get('usage', {})
        )

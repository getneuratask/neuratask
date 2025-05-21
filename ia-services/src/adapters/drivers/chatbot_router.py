from fastapi import APIRouter, HTTPException, Depends
from src.domain.schemas.chatbot_entity import ChatRequest, ChatResponse
from src.domain.chatbot_service import ChatbotServiceImpl
from src.utils.OpenRouter import OpenRouterAPI

# Crear una instancia de OpenRouterAPI para ser reutilizada
openrouter_api = OpenRouterAPI()

# Crear una instancia del servicio de chatbot
chatbot_service = ChatbotServiceImpl(openrouter_api)

# Crear un router para las rutas del chatbot
router = APIRouter(
    prefix="/chat",
    tags=["Chatbot"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint para generar respuestas de chat usando OpenRouter.
    
    Args:
        request: La solicitud de chat con mensajes y parámetros opcionales
        
    Returns:
        La respuesta generada por el modelo de OpenRouter
    """
    try:
        response = chatbot_service.generate_chat_response(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar la solicitud de chat: {str(e)}"
        )

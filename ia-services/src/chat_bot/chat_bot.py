import sys
import os
# Agregar el path del directorio padre para acceder a utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.OpenRouterClient import OpenRouterAPI
from typing import List, Dict, Any, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatBotManager:
    def __init__(self, model="deepseek/deepseek-r1-distill-llama-70b:free", 
                 temperature=0.7, max_tokens=1000):
        """
        Manejador de requests para IA usando OpenRouter
        
        :param model: Modelo de IA a utilizar
        :param temperature: Grado de aleatoriedad en la respuesta
        :param max_tokens: Número máximo de tokens en la respuesta
        """
        try:
            self.client = OpenRouterAPI(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            logger.info(f"ChatBotManager iniciado con modelo: {model}")
        except Exception as e:
            logger.error(f"Error al inicializar OpenRouterAPI: {e}")
            raise

    def simple_chat(self, user_message: str, system_prompt: Optional[str] = None) -> str:
        """
        Envía un mensaje simple al chatbot
        
        :param user_message: Mensaje del usuario
        :param system_prompt: Prompt del sistema (opcional)
        :return: Respuesta del chatbot
        """
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": user_message})
            
            response = self.client.send_request(messages)
            return response['choices'][0]['message']['content']
            
        except Exception as e:
            logger.error(f"Error en simple_chat: {e}")
            raise

    def conversation_chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Mantiene una conversación con múltiples mensajes
        
        :param messages: Lista de mensajes en formato [{"role": "user|assistant|system", "content": "mensaje"}, ...]
        :return: Respuesta del chatbot
        """
        try:
            response = self.client.send_request(messages)
            return response['choices'][0]['message']['content']
            
        except Exception as e:
            logger.error(f"Error en conversation_chat: {e}")
            raise

    def structured_response(self, user_message: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Solicita una respuesta estructurada en formato JSON
        
        :param user_message: Mensaje del usuario
        :param system_prompt: Prompt del sistema (opcional)
        :return: Respuesta estructurada del chatbot
        """
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": user_message})
            
            response = self.client.send_request(
                messages, 
                response_format={"type": "json_object"}
            )
            
            content = response['choices'][0]['message']['content']
            
            # Intentar parsear el JSON
            import json
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {"response": content}
                
        except Exception as e:
            logger.error(f"Error en structured_response: {e}")
            raise

    def analyze_text(self, text: str, analysis_type: str = "sentiment") -> Dict[str, Any]:
        """
        Analiza un texto según el tipo especificado
        
        :param text: Texto a analizar
        :param analysis_type: Tipo de análisis (sentiment, summary, keywords, etc.)
        :return: Resultado del análisis
        """
        analysis_prompts = {
            "sentiment": "Analiza el sentimiento del siguiente texto y responde en formato JSON con: sentiment (positive/negative/neutral), confidence (0-1), y reason.",
            "summary": "Resume el siguiente texto en formato JSON con: summary, key_points (lista), y word_count.",
            "keywords": "Extrae las palabras clave del siguiente texto y responde en formato JSON con: keywords (lista), topics (lista), y relevance_scores.",
            "classification": "Clasifica el siguiente texto en formato JSON con: category, subcategory, confidence, y explanation."
        }
        
        system_prompt = analysis_prompts.get(analysis_type, analysis_prompts["sentiment"])
        
        return self.structured_response(text, system_prompt)

# Instancia global para reusar
chat_manager = ChatBotManager()
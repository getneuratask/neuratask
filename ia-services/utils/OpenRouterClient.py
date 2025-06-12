import requests
import json
import logging
import os
from dotenv import load_dotenv
import time

load_dotenv('.apikeys')  # Cambiar al nuevo nombre del archivo

class OpenRouterAPI:
    def __init__(self, api_key=None, model="deepseek/deepseek-r1-distill-llama-70b:free", 
                 temperature=0.7, max_tokens=500, response_format=None, 
                 top_p=1, frequency_penalty=0, presence_penalty=0):
        """
        Clase para realizar peticiones a la API de OpenRouter.
        
        :param api_key: Clave de autenticación para la API de OpenRouter.
        :param model: Modelo de IA a utilizar. [Lista de modelos disponibles](https://openrouter.ai/models)
        :param temperature: Grado de aleatoriedad en la respuesta (por defecto 0.7).
        :param max_tokens: Número máximo de tokens en la respuesta (por defecto 500).
        :param response_format: Formato de respuesta deseado (e.g., {"type": "json_object"})
        :param top_p: Núcleo de probabilidad acumulativa para muestreo (por defecto 1).
        :param frequency_penalty: Penalización por frecuencia de tokens (por defecto 0).
        :param presence_penalty: Penalización por presencia de tokens (por defecto 0).
        """
        self.api_key = "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" 
        if not self.api_key:
            raise ValueError("API key must be provided either as parameter or in .env file")
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.response_format = response_format
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def send_request(self, messages, response_format=None):
        """
        Envía una solicitud a OpenRouter con los mensajes proporcionados.
        :param messages: Lista de mensajes en formato [{"role": "system|user|assistant", "content": "mensaje"}, ...]
        :param response_format: Formato de respuesta deseado (e.g., {"type": "json_object"})
        Retorna la respuesta directa de la API o lanza una excepción si algo falla.
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            "stream": False
        }

        if response_format is not None:
            payload["response_format"] = response_format

        response = requests.post(self.url, headers=self.headers, json=payload)
        response.raise_for_status()
        time.sleep(1)
        return response.json()


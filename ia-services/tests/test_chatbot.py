#!/usr/bin/env python3
import requests
import json

def test_chat_endpoint():
    """
    Prueba el endpoint de chat con un mensaje simple.
    """
    url = "http://localhost:47337/chat"
    
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "Eres un asistente útil y amigable."
            },
            {
                "role": "user",
                "content": "Hola, ¿cómo estás?"
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()
        
        print("Respuesta exitosa:")
        print(f"Mensaje: {response_data['message']['content']}")
        if 'usage' in response_data:
            print(f"Tokens utilizados: {response_data['usage'].get('total_tokens', 'N/A')}")
        
        return response_data
    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP: {e}")
        if e.response is not None:
            print(f"Detalles: {e.response.text}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_chat_endpoint()

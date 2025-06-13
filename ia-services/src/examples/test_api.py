"""
Ejemplos de uso de la NeuraTask Chat Bot API
"""
import requests
import json

# URL base de la API
BASE_URL = "http://localhost:8000"

def test_simple_chat():
    """Ejemplo de chat simple"""
    url = f"{BASE_URL}/chat/simple"
    payload = {
        "message": "¿Cuál es la capital de Francia?",
        "system_prompt": "Eres un asistente helpful que responde de forma concisa."
    }
    
    response = requests.post(url, json=payload)
    print("=== Chat Simple ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_conversation():
    """Ejemplo de conversación"""
    url = f"{BASE_URL}/chat/conversation"
    payload = {
        "messages": [
            {"role": "system", "content": "Eres un asistente de programación."},
            {"role": "user", "content": "¿Qué es Python?"},
            {"role": "assistant", "content": "Python es un lenguaje de programación de alto nivel."},
            {"role": "user", "content": "¿Cuáles son sus ventajas?"}
        ]
    }
    
    response = requests.post(url, json=payload)
    print("=== Conversación ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_structured_response():
    """Ejemplo de respuesta estructurada"""
    url = f"{BASE_URL}/chat/structured"
    payload = {
        "message": "Dame información sobre el lenguaje Python incluyendo año de creación, creador y principales características",
        "system_prompt": "Responde en formato JSON con las claves: año, creador, características (array)"
    }
    
    response = requests.post(url, json=payload)
    print("=== Respuesta Estructurada ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_text_analysis():
    """Ejemplo de análisis de texto"""
    url = f"{BASE_URL}/analyze/text"
    payload = {
        "text": "Estoy muy feliz con los resultados del proyecto. Todo salió mejor de lo esperado y el equipo trabajó increíblemente bien.",
        "analysis_type": "sentiment"
    }
    
    response = requests.post(url, json=payload)
    print("=== Análisis de Sentimiento ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_health_check():
    """Verificar salud de la API"""
    url = f"{BASE_URL}/health"
    
    response = requests.get(url)
    print("=== Health Check ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_available_models():
    """Ver modelos disponibles"""
    url = f"{BASE_URL}/models/available"
    
    response = requests.get(url)
    print("=== Modelos Disponibles ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

if __name__ == "__main__":
    print("🧪 Probando NeuraTask Chat Bot API...")
    print("=" * 50)
    
    try:
        # Verificar que la API esté funcionando
        test_health_check()
        
        # Probar diferentes endpoints
        test_simple_chat()
        test_conversation()
        test_structured_response()
        test_text_analysis()
        test_available_models()
        
        print("✅ Todas las pruebas completadas!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar a la API.")
        print("Asegúrate de que la API esté ejecutándose en http://localhost:8000")
        print("Ejecuta: python src/run_api.py")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

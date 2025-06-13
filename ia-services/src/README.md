# NeuraTask Chat Bot API

API REST para interactuar con servicios de IA usando OpenRouter.

## Estructura

```
src/
├── api/
│   ├── __init__.py
│   └── chat_api.py          # API REST con FastAPI
├── chat_bot/
│   └── chat_bot.py          # Manejador de requests de IA
├── examples/
│   └── test_api.py          # Ejemplos de uso
└── run_api.py               # Script para ejecutar la API
```

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Asegúrate de que tienes tu API key de OpenRouter configurada en `utils/OpenRouterClient.py`

## Uso

### Ejecutar la API

Desde el directorio `ia-services`:

```bash
python src/run_api.py
```

La API estará disponible en:
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Endpoints Disponibles

#### 1. Chat Simple
```bash
POST /chat/simple
```
```json
{
  "message": "¿Cuál es la capital de Francia?",
  "system_prompt": "Eres un asistente helpful."
}
```

#### 2. Conversación
```bash
POST /chat/conversation
```
```json
{
  "messages": [
    {"role": "system", "content": "Eres un asistente."},
    {"role": "user", "content": "Hola"},
    {"role": "assistant", "content": "¡Hola! ¿En qué puedo ayudarte?"},
    {"role": "user", "content": "¿Qué tiempo hace?"}
  ]
}
```

#### 3. Respuesta Estructurada
```bash
POST /chat/structured
```
```json
{
  "message": "Dame información sobre Python",
  "system_prompt": "Responde en JSON con: año, creador, características"
}
```

#### 4. Análisis de Texto
```bash
POST /analyze/text
```
```json
{
  "text": "Estoy muy feliz con los resultados",
  "analysis_type": "sentiment"  // sentiment, summary, keywords, classification
}
```

#### 5. Modelos Disponibles
```bash
GET /models/available
```

#### 6. Health Check
```bash
GET /health
```

### Ejemplos de Uso

Ejecutar ejemplos de prueba:

```bash
# Asegúrate de que la API esté ejecutándose primero
python src/examples/test_api.py
```

### Uso Programático

```python
from chat_bot.chat_bot import chat_manager

# Chat simple
response = chat_manager.simple_chat("Hola", "Eres un asistente amigable")

# Respuesta estructurada
data = chat_manager.structured_response("Dame info sobre Python", 
                                      "Responde en JSON")

# Análisis de texto
analysis = chat_manager.analyze_text("Texto a analizar", "sentiment")
```

## Configuración

### Modelos Disponibles

- `deepseek/deepseek-r1-distill-llama-70b:free` (por defecto)
- `meta-llama/llama-3.2-3b-instruct:free`
- `microsoft/phi-3-mini-128k-instruct:free`
- `google/gemma-2-9b-it:free`

### Parámetros Configurables

- `temperature`: Creatividad de la respuesta (0.0 - 1.0)
- `max_tokens`: Máximo de tokens en la respuesta
- `model`: Modelo de IA a utilizar

## Logs

La API usa logging estándar de Python. Los logs se mostrarán en la consola cuando ejecutes la API.

## Troubleshooting

### Error de importación
- Asegúrate de ejecutar desde el directorio correcto
- Verifica que todas las dependencias estén instaladas

### Error de conexión a OpenRouter
- Verifica tu API key
- Comprueba tu conexión a internet
- Revisa el endpoint `/health` para diagnóstico

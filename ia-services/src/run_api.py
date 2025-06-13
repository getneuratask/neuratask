#!/usr/bin/env python3
"""
Script para ejecutar la API de NeuraTask Chat Bot
"""
import uvicorn
import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.chat_api import app

if __name__ == "__main__":
    print("🚀 Iniciando NeuraTask Chat Bot API...")
    print("📖 Documentación disponible en: http://localhost:8000/docs")
    print("🔧 API disponible en: http://localhost:8000")
    print("❤️  Health check: http://localhost:8000/health")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )

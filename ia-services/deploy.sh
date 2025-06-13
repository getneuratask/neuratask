#!/bin/bash

# Deployment script for NeuraTask IA Services
# Usage: ./deploy.sh [development|production]

set -e

MODE=${1:-development}

echo "🚀 Deploying NeuraTask IA Services in $MODE mode..."

# Create network if it doesn't exist
docker network create neuratask-network 2>/dev/null || true

# Build and start services
if [ "$MODE" = "production" ]; then
    echo "📦 Building production image..."
    docker-compose -f docker-compose.yml build --no-cache
    docker-compose -f docker-compose.yml up -d
else
    echo "🔧 Starting development environment..."
    docker-compose -f docker-compose.yml up --build -d
fi

echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
if curl -f http://localhost:8000/ > /dev/null 2>&1; then
    echo "✅ IA Services are running successfully!"
    echo "📖 API Documentation: http://localhost:8000/docs"
    echo "🔧 API Health Check: http://localhost:8000/"
else
    echo "❌ Services failed to start properly"
    echo "📋 Checking logs..."
    docker-compose logs ia-services
    exit 1
fi

echo "🎉 Deployment completed!"
echo ""
echo "Available endpoints:"
echo "  - Health: http://localhost:8000/"
echo "  - Simple Chat: POST http://localhost:8000/chat/simple"
echo "  - Conversation: POST http://localhost:8000/chat/conversation"
echo "  - Structured Response: POST http://localhost:8000/chat/structured"
echo "  - Text Analysis: POST http://localhost:8000/analyze/text"
echo "  - Available Models: GET http://localhost:8000/models/available"
echo ""
echo "📖 Full API documentation: http://localhost:8000/docs"

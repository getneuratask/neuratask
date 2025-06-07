#!/bin/bash

# NeuralTask Backend Deployment Script

echo "🚀 NeuralTask Backend Deployment"
echo "================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/Update dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if database is running (optional)
echo "🗄️  Checking database connection..."
python -c "
import psycopg2
try:
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='neuratask',
        user='postgres',
        password='postgres'
    )
    conn.close()
    print('✅ Database connection successful')
except Exception as e:
    print('❌ Database connection failed:', str(e))
    print('Please ensure PostgreSQL is running and database exists')
"

# Start the application
echo "🌟 Starting NeuralTask API..."
echo "📍 API will be available at: http://localhost:8000"
echo "📖 Documentation: http://localhost:8000/docs"
echo "🔄 Press Ctrl+C to stop the server"
echo ""

python main.py

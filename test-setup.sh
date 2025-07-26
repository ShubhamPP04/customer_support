#!/bin/bash

echo "🚀 Testing Customer Support Chatbot Docker Setup"
echo "================================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env file and add your GROQ_API_KEY"
    echo "   Then run this script again."
    exit 1
fi

# Check if GROQ_API_KEY is set
if ! grep -q "GROQ_API_KEY=gsk_" .env; then
    echo "⚠️  GROQ_API_KEY not configured in .env file"
    echo "📝 Please add your GROQ API key to .env file"
    exit 1
fi

echo "✅ Docker is running"
echo "✅ Environment file configured"

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Test backend health
echo "🔍 Testing backend health..."
if curl -f http://localhost:5001/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
    docker-compose logs backend
fi

# Test frontend health
echo "🔍 Testing frontend health..."
if curl -f http://localhost:3000/health > /dev/null 2>&1; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend health check failed"
    docker-compose logs frontend
fi

# Test database
echo "🔍 Testing database connection..."
if docker-compose exec -T database mysql -u customer_support_user -pcustomer_support_password -e "SELECT 1;" > /dev/null 2>&1; then
    echo "✅ Database is healthy"
else
    echo "❌ Database connection failed"
    docker-compose logs database
fi

echo ""
echo "🎉 Setup complete!"
echo "📱 Frontend: http://localhost:3000"
echo "🔗 Backend API: http://localhost:5001"
echo "🗄️  Database: localhost:3306"
echo ""
echo "To stop: docker-compose down"
echo "To view logs: docker-compose logs -f"

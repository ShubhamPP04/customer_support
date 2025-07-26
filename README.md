# Customer Support Chatbot

A full-stack AI-powered customer support chatbot for e-commerce clothing sites, built with React, Flask, and MySQL.

## 🚀 Features

- **Intelligent AI Chat**: Powered by Groq's Llama 3 model for natural conversations
- **Conversation History**: Persistent chat history with automatic updates
- **Modern UI**: Professional React interface with blue theme
- **Real-time Updates**: Auto-refreshing conversation history
- **Responsive Design**: Works on desktop and mobile devices
- **Docker Support**: Full containerization for easy deployment

## 🛠 Tech Stack

### Frontend
- **React 18** with TypeScript
- **Context API** for state management
- **Axios** for API communication
- **Lucide React** for icons
- **CSS3** with gradients and animations

### Backend
- **Flask** web framework
- **Groq API** for LLM integration
- **SQLAlchemy** ORM
- **MySQL** database
- **Flask-CORS** for cross-origin requests

### DevOps
- **Docker** & **Docker Compose**
- **Nginx** for frontend serving
- **Multi-stage builds** for optimization

## 📋 Prerequisites

- Docker and Docker Compose
- Groq API key (get from [Groq Console](https://console.groq.com/))

## 🚀 Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd customer_support
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Groq API key:
   ```
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5001
   - Database: localhost:3306

5. **Stop the application**
   ```bash
   docker-compose down
   ```

## 🔧 Development Setup

### Manual Setup (without Docker)

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Add your Groq API key to .env
   ```

5. **Run the backend**
   ```bash
   python app_simple.py
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```

#### Database Setup (MySQL)

1. **Install MySQL** (version 8.0+)

2. **Create database**
   ```sql
   CREATE DATABASE customer_support;
   CREATE USER 'customer_support_user'@'localhost' IDENTIFIED BY 'customer_support_password';
   GRANT ALL PRIVILEGES ON customer_support.* TO 'customer_support_user'@'localhost';
   ```

3. **Load sample data** (optional)
   ```bash
   mysql -u customer_support_user -p customer_support < backend/archive/sample_data.sql
   ```

## 📁 Project Structure

```
customer_support/
├── backend/
│   ├── app_simple.py          # Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Backend Docker image
│   └── archive/              # Sample CSV data
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── context/          # React Context
│   │   └── services/         # API services
│   ├── package.json          # Node dependencies
│   ├── Dockerfile           # Frontend Docker image
│   └── nginx.conf           # Nginx configuration
├── docker-compose.yml        # Docker orchestration
├── .env.example             # Environment template
└── README.md               # This file
```

## 🐳 Docker Services

### Services Overview

- **database**: MySQL 8.0 database
- **backend**: Flask API server
- **frontend**: React app served by Nginx

### Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f [service_name]

# Restart a service
docker-compose restart [service_name]

# Stop all services
docker-compose down

# Remove volumes (data will be lost)
docker-compose down -v

# Rebuild images
docker-compose build --no-cache
```

## 🌐 API Endpoints

### Chat API
- `POST /api/chat` - Send message to chatbot
- `GET /api/conversations` - Get conversation list
- `GET /api/conversations/{id}/history` - Get conversation history

### Health Check
- `GET /health` - Service health status

## 🎨 Features

### Chat Functionality
- Real-time AI responses using Groq's Llama 3
- Conversation history persistence
- Auto-updating conversation list
- Professional message styling with markdown support

### UI Features
- Modern blue gradient theme
- Responsive design for all screen sizes
- Professional avatars for user and AI
- Smooth animations and transitions
- Auto-scrolling message list

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=mysql://user:password@localhost:3306/customer_support
FLASK_ENV=development
PORT=5001
```

#### Frontend (.env)
```
REACT_APP_API_BASE_URL=http://localhost:5001
REACT_APP_ENV=development
```

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using the port
   lsof -i :3000
   lsof -i :5001
   
   # Kill the process or change ports in docker-compose.yml
   ```

2. **Database connection failed**
   - Ensure MySQL is running
   - Check credentials in .env file
   - Wait for database to be ready (health check)

3. **CORS errors**
   - Check API_BASE_URL in frontend .env
   - Verify CORS configuration in backend

4. **Groq API errors**
   - Verify API key is correct
   - Check API rate limits
   - Ensure internet connectivity

### Health Checks

```bash
# Check backend health
curl http://localhost:5001/health

# Check frontend health
curl http://localhost:3000/health

# Check database connection
docker-compose exec database mysql -u customer_support_user -p -e "SELECT 1;"
```

## 📈 Performance

### Optimization Features
- Multi-stage Docker builds for smaller images
- Nginx gzip compression
- React code splitting
- Image caching headers
- Database connection pooling

## 🔒 Security

### Security Measures
- Non-root user in Docker containers
- Security headers in Nginx
- Environment variable isolation
- CORS configuration
- Input validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support, please:
1. Check the troubleshooting section
2. Review Docker logs: `docker-compose logs`
3. Open an issue on GitHub

---

**Built with ❤️ for customer support automation**

# 🚨 Multi-Agent Emergency Response System

A sophisticated AI-powered emergency response system designed specifically for Karachi, Pakistan. This system uses multiple specialized AI agents to handle different types of emergencies and coordinate responses efficiently.

## 🌟 Features

### 🤖 Multi-Agent Architecture
- **Medical Emergency Agent**: Handles medical emergencies, hospital routing, and ambulance coordination
- **Fire Emergency Agent**: Manages fire emergencies, fire station routing, and fire brigade coordination
- **Police Emergency Agent**: Handles security incidents, police station routing, and law enforcement coordination
- **Multi-Agent Coordinator**: Intelligently routes queries to appropriate agents and coordinates multi-service emergencies

### 🧠 AI-Powered Intelligence
- **Google Gemini Integration**: Uses Google's Gemini 2.0 Flash model for natural language processing
- **Context-Aware Routing**: Analyzes emergency queries to determine the most appropriate response
- **Multi-Service Detection**: Automatically detects emergencies requiring multiple services (e.g., fire with injuries)
- **Chat Memory**: Maintains conversation context for better user experience

### 📍 Location Services
- **Karachi-Specific Data**: Comprehensive database of hospitals, fire stations, and police stations in Karachi
- **IP-Based Location Detection**: Automatically detects user location for faster response
- **Real-Time Routing**: Provides optimal routes to emergency services

### 🔄 Real-Time Communication
- **FastAPI Backend**: High-performance REST API with automatic documentation
- **WebSocket Support**: Real-time communication capabilities
- **CORS Enabled**: Cross-origin resource sharing for web applications

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Multi-Agent Coordinator                  │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│  │  Medical Agent  │ │   Fire Agent    │ │  Police Agent   │ │
│  │                 │ │                 │ │                 │ │
│  │ • Hospitals     │ │ • Fire Stations │ │ • Police Stations│ │
│  │ • Ambulances    │ │ • Fire Brigade  │ │ • Law Enforcement│ │
│  │ • Medical Data  │ │ • Fire Equipment│ │ • Security Data  │ │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
│  • REST API Endpoints                                       │
│  • WebSocket Support                                        │
│  • CORS Middleware                                          │
│  • Health Check Endpoints                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                               │
│  • Karachi Hospitals Database                               │
│  • Emergency Services Database                              │
│  • Police Stations Database                                 │
│  • Location Services                                        │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Google Gemini API Key
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd Emergency_Agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
   
   # Edit the file and replace with your actual API key
   notepad .env
   ```

4. **Get your Gemini API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Create a new API key
   - Copy the key to your `.env` file

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Access the API**
   - API Documentation: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/status`
   - Root Endpoint: `http://localhost:8000/`

## 📚 API Documentation

### Core Endpoints

#### Health Check
```http
GET /status
```
Returns system status and health information.

#### Multi-Agent Chat
```http
POST /multi-agent/chat
Content-Type: application/json

{
  "message": "I need help with a fire emergency",
  "session_id": "optional-session-id"
}
```

#### Emergency Services Summary
```http
GET /multi-agent/services
```
Returns available emergency services and their capabilities.

#### Chat History
```http
GET /multi-agent/session/{session_id}/history
```
Retrieves chat history for a specific session.

### Individual Agent Endpoints

#### Medical Emergency
```http
POST /medical/chat
Content-Type: application/json

{
  "message": "I need medical assistance",
  "location": "optional-location"
}
```

#### Fire Emergency
```http
POST /fire/chat
Content-Type: application/json

{
  "message": "There's a fire in my building",
  "location": "optional-location"
}
```

#### Police Emergency
```http
POST /police/chat
Content-Type: application/json

{
  "message": "I need police assistance",
  "location": "optional-location"
}
```

## 🗂️ Project Structure

```
Emergency_Agent/
├── agents/                          # AI Agent implementations
│   ├── medical_coordinator.py       # Medical emergency agent
│   ├── fire_emergency_coordinator.py # Fire emergency agent
│   ├── police_emergency_coordinator.py # Police emergency agent
│   ├── multi_agent_coordinator.py   # Main coordinator
│   ├── gemini_client.py             # Google Gemini integration
│   └── ...                          # Other agent utilities
├── data/                            # Emergency services data
│   ├── karachi_hospitals_comprehensive.json
│   ├── karachi_emergency_services.json
│   └── karachi_police_services.json
├── models/                          # Data models and schemas
│   ├── schemas.py                   # Core data schemas
│   ├── chat_schemas.py              # Chat-related schemas
│   └── location_schemas.py          # Location-related schemas
├── main.py                          # FastAPI application entry point
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker configuration
├── railway.json                     # Railway deployment config
├── railway.toml                     # Railway environment config
└── README.md                        # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes | - |
| `PORT` | Server port | No | 8000 |
| `DEBUG` | Debug mode | No | False |

### Data Configuration

The system uses JSON files for emergency services data:

- **Hospitals**: 60+ hospitals in Karachi with contact details and specialties
- **Fire Stations**: 15+ fire stations with equipment and response capabilities
- **Police Stations**: 16+ police stations and units with jurisdiction areas

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Docker Deployment
```bash
# Build the image
docker build -t emergency-agent .

# Run the container
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key emergency-agent
```

### Railway Deployment

1. **Connect your repository to Railway**
2. **Set environment variables**:
   - `GEMINI_API_KEY`: Your Google Gemini API key
3. **Deploy**: Railway will automatically build and deploy using the Dockerfile

### Health Checks

The system includes comprehensive health checks:
- `/status` - Basic system status
- `/health` - Detailed health information
- Docker health check integration

## 🧪 Testing

### Manual Testing
```bash
# Test health endpoint
curl http://localhost:8000/status

# Test multi-agent chat
curl -X POST http://localhost:8000/multi-agent/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I need medical help"}'
```

### Example Queries

#### Medical Emergency
```
"I need an ambulance for a heart attack"
"Where is the nearest hospital?"
"I have chest pain and need immediate help"
```

#### Fire Emergency
```
"There's a fire in my apartment building"
"I smell smoke and need the fire department"
"Fire emergency at my location"
```

#### Police Emergency
```
"I need police assistance"
"There's a break-in at my house"
"Emergency situation requiring police"
```

#### Multi-Service Emergency
```
"There's a fire with people trapped inside"
"Car accident with injuries and fire"
"Building collapse with multiple casualties"
```

## 🔒 Security Features

- **API Key Protection**: Environment variable-based API key management
- **CORS Configuration**: Proper cross-origin resource sharing setup
- **Input Validation**: Pydantic models for request validation
- **Error Handling**: Comprehensive error handling and logging

## 📊 Performance Features

- **Async Operations**: FastAPI async/await for high performance
- **Connection Pooling**: Efficient database connections
- **Caching**: Intelligent caching of emergency services data
- **Load Balancing**: Ready for horizontal scaling

## 🛠️ Development

### Adding New Agents

1. Create a new agent class in `agents/`
2. Implement the required methods
3. Add the agent to the multi-agent coordinator
4. Update the API endpoints in `main.py`

### Adding New Data Sources

1. Add JSON data files to `data/`
2. Update the corresponding agent to load the new data
3. Test the integration

### Customizing Responses

1. Modify the prompt templates in agent classes
2. Update the response formatting
3. Test with various emergency scenarios

## 📈 Monitoring and Logging

- **Structured Logging**: Comprehensive logging throughout the system
- **Health Monitoring**: Built-in health check endpoints
- **Performance Metrics**: Request timing and response metrics
- **Error Tracking**: Detailed error logging and reporting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the health check endpoint at `/status`

## 🔮 Future Enhancements

- **WhatsApp Integration**: Direct emergency reporting via WhatsApp
- **SMS Notifications**: Emergency alerts via SMS
- **Voice Integration**: Voice-based emergency reporting
- **Mobile App**: Native mobile application
- **Real-time Tracking**: Live tracking of emergency response units
- **Machine Learning**: Improved emergency classification and routing

---

**Built with ❤️ for the safety and security of Karachi, Pakistan**
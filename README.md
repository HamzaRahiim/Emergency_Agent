# Emergency Medical Agent System

An AI-powered emergency medical response system for Karachi, Pakistan, built with FastAPI and Google Gemini AI.

## Features

- **Multi-Agent Architecture**: Specialized agents for hospital finding, appointment booking, and ambulance dispatch
- **AI-Powered Analysis**: Google Gemini integration for intelligent emergency assessment
- **Real-time Response**: Fast emergency processing with comprehensive recommendations
- **Karachi-Focused**: Optimized for Karachi's healthcare infrastructure
- **Cost-Optimized**: Single AI call design to minimize API costs

## Architecture

The system consists of three specialized medical agents:

1. **Hospital Finder Agent** - Locates nearby hospitals and clinics
2. **Appointment Agent** - Handles booking and scheduling
3. **Ambulance Agent** - Manages emergency dispatch

All agents are coordinated by the **Medical Coordinator** which makes a single comprehensive call to Google Gemini for AI analysis.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `env_example.txt` to `.env` and add your Google Gemini API key:

```bash
cp env_example.txt .env
```

Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your API key from: https://makersuite.google.com/app/apikey

### 3. Run the Application

```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Access the Application

- **Frontend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## API Endpoints

- `POST /emergency/medical` - Main emergency processing endpoint
- `GET /hospitals` - Get all available hospitals
- `GET /hospitals/nearby` - Find hospitals near a location
- `GET /ambulance/status/{ambulance_id}` - Check ambulance status
- `GET /appointments/{patient_id}` - Get patient appointments

## Data Sources

The system uses two hospital datasets:
- `hospiatl_dataset.json` - Structured hospital data with contact information
- `hospital data 2.json` - OpenStreetMap hospital data with coordinates

## Usage

1. Open the web interface at http://localhost:8000
2. Fill in the emergency details:
   - Emergency type (medical, trauma, cardiac, etc.)
   - Priority level (low, medium, high, critical)
   - Location (address and coordinates)
   - Patient information
   - Emergency description
3. Submit the request
4. The system will:
   - Analyze the emergency using AI
   - Find nearby hospitals
   - Dispatch ambulance if needed
   - Book appointments if appropriate
   - Provide recommendations and follow-up instructions

## Cost Optimization

The system is designed to minimize Google Gemini API costs by:
- Making only one comprehensive AI call per emergency
- Including all necessary context in a single request
- Providing fallback responses if AI analysis fails

## Development

### Project Structure

```
Emergency_Agent/
├── agents/                 # Medical agents
│   ├── medical_coordinator.py
│   ├── hospital_finder.py
│   ├── appointment_agent.py
│   ├── ambulance_agent.py
│   └── gemini_client.py
├── models/                 # Data models
│   └── schemas.py
├── data/                   # Data storage
├── templates/              # Frontend templates
├── static/                 # Static files
├── main.py                 # FastAPI application
├── requirements.txt        # Dependencies
└── README.md
```

### Adding New Features

1. **New Emergency Types**: Add to `EmergencyType` enum in `models/schemas.py`
2. **New Agents**: Create new agent class in `agents/` directory
3. **New Endpoints**: Add routes in `main.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.


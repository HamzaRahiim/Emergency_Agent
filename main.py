from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
import uuid

from agents.medical_coordinator import MedicalCoordinator
from agents.chat_coordinator import ChatCoordinator
from agents.professional_emergency_coordinator import ProfessionalEmergencyCoordinator
from agents.ai_chat_coordinator import AIChatCoordinator
from agents.fire_emergency_coordinator import FireEmergencyCoordinator
from agents.police_emergency_coordinator import PoliceEmergencyCoordinator
from agents.multi_agent_coordinator import MultiAgentCoordinator
from models.schemas import EmergencyRequest, EmergencyResponse
from models.chat_schemas import ChatRequest, ChatResponse, ConfirmationRequest
from models.location_schemas import LocationRequest, PhoneVerification

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Emergency Medical Agent System",
    description="AI-powered emergency medical response system for Karachi",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize coordinators
medical_coordinator = MedicalCoordinator()
chat_coordinator = ChatCoordinator()
professional_emergency_coordinator = ProfessionalEmergencyCoordinator()
ai_chat_coordinator = AIChatCoordinator()
fire_emergency_coordinator = FireEmergencyCoordinator()
police_emergency_coordinator = PoliceEmergencyCoordinator()
multi_agent_coordinator = MultiAgentCoordinator()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the simple professional chat interface (main page)"""
    return templates.TemplateResponse("simple_chat.html", {"request": request})

@app.get("/form", response_class=HTMLResponse)
async def read_form(request: Request):
    """Serve the form-based interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/fire", response_class=HTMLResponse)
async def read_fire_emergency(request: Request):
    """Serve the Fire & Emergency Services interface"""
    return templates.TemplateResponse("fire_emergency_chat.html", {"request": request})

@app.get("/police", response_class=HTMLResponse)
async def read_police_emergency(request: Request):
    """Serve the Police Emergency Services interface"""
    return templates.TemplateResponse("police_emergency_chat.html", {"request": request})

@app.get("/hub", response_class=HTMLResponse)
async def read_multi_agent_hub(request: Request):
    """Serve the Multi-Agent Emergency Services Hub interface"""
    return templates.TemplateResponse("multi_agent_chat.html", {"request": request})

@app.post("/emergency/medical", response_model=EmergencyResponse)
async def handle_medical_emergency(request: EmergencyRequest):
    """
    Handle medical emergency requests
    """
    try:
        response = await medical_coordinator.process_emergency(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/hospitals")
async def get_hospitals():
    """Get list of all hospitals"""
    return medical_coordinator.hospital_finder.get_all_hospitals()

@app.get("/hospitals/nearby")
async def get_nearby_hospitals(lat: float, lon: float, radius: float = 10.0):
    """Get hospitals near a location"""
    return medical_coordinator.hospital_finder.find_nearby_hospitals(lat, lon, radius)

@app.get("/ambulance/status/{ambulance_id}")
async def get_ambulance_status(ambulance_id: str):
    """Get status of a dispatched ambulance"""
    return medical_coordinator.ambulance_agent.get_ambulance_status(ambulance_id)

@app.get("/appointments/{patient_id}")
async def get_patient_appointments(patient_id: str):
    """Get appointments for a patient"""
    return medical_coordinator.appointment_agent.get_patient_appointments(patient_id)

# Chat-based emergency endpoints
@app.post("/chat/emergency", response_model=ChatResponse)
async def chat_emergency(request: ChatRequest):
    """
    Process emergency request through chat interface
    """
    try:
        response = await chat_coordinator.process_chat_message(
            message=request.message,
            user_location=request.user_location,
            session_id=request.session_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/confirm", response_model=ChatResponse)
async def confirm_emergency(confirmation: ConfirmationRequest):
    """
    Confirm emergency processing
    """
    try:
        response = await chat_coordinator.confirm_and_process(
            session_id=confirmation.message_id,
            confirmed=confirmation.confirmed,
            additional_info=confirmation.additional_info
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/session/{session_id}")
async def get_chat_session(session_id: str):
    """Get chat session information"""
    session_info = chat_coordinator.get_session_info(session_id)
    if not session_info:
        raise HTTPException(status_code=404, detail="Session not found")
    return session_info

# Location and phone verification endpoints
@app.post("/location/set", response_model=ChatResponse)
async def set_user_location(request: dict):
    """Set user location (GPS or manual)"""
    try:
        response = await chat_coordinator.handle_location_request(
            session_id=request.get("session_id"),
            latitude=request.get("latitude"),
            longitude=request.get("longitude"),
            address=request.get("address"),
            accuracy=request.get("accuracy")
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/phone/verify", response_model=ChatResponse)
async def verify_phone_number(request: dict):
    """Verify phone number for emergency contact"""
    try:
        response = await chat_coordinator.handle_phone_request(
            session_id=request.get("session_id"),
            phone_number=request.get("phone_number"),
            country_code=request.get("country_code", "+92")
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/process", response_model=ChatResponse)
async def process_chat_with_requirements(request: ChatRequest):
    """
    Process chat message with location and phone requirements
    """
    try:
        # Use the new requirements-based processing
        response = await chat_coordinator.check_requirements_and_process(
            message=request.message,
            session_id=request.session_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/location/permission", response_model=ChatResponse)
async def update_location_permission(
    session_id: str,
    granted: bool,
    denied_reason: Optional[str] = None
):
    """Update location permission status"""
    try:
        success = chat_coordinator.location_manager.update_location_permission(
            session_id=session_id,
            granted=granted,
            denied_reason=denied_reason
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        
        message = "✅ Location permission updated." if granted else "❌ Location permission denied. Please provide manual location."
        
        return ChatResponse(
            message_id=str(uuid.uuid4()),
            type="system",
            content=message,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# AI Chat Coordinator endpoints
@app.post("/ai/chat", response_model=ChatResponse)
async def ai_chat_with_user(request_data: dict, request: Request):
    """Direct AI chat with user - Natural conversation"""
    try:
        message = request_data.get("message", "")
        session_id = request_data.get("session_id")
        
        # Get client IP from request headers
        client_ip = request.headers.get("x-forwarded-for", request.headers.get("x-real-ip", "127.0.0.1"))
        
        response = await ai_chat_coordinator.process_user_message(
            message=message,
            user_ip=client_ip,
            session_id=session_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/confirm", response_model=ChatResponse)
async def ai_confirm_emergency(request: dict):
    """Confirm emergency action through AI coordinator"""
    try:
        session_id = request.get("session_id")
        confirmed = request.get("confirmed", False)
        
        response = await ai_chat_coordinator.confirm_emergency_action(
            session_id=session_id,
            confirmed=confirmed
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/dispatch", response_model=ChatResponse)
async def ai_dispatch_ambulance(request: dict):
    """Process hospital dispatch through AI coordinator"""
    try:
        session_id = request.get("session_id")
        hospital_number = request.get("hospital_number")
        phone_number = request.get("phone_number")
        additional_info = request.get("additional_info", "")
        
        response = await ai_chat_coordinator.process_hospital_dispatch(
            session_id=session_id,
            hospital_number=hospital_number,
            phone_number=phone_number,
            additional_info=additional_info
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Professional Emergency Coordinator endpoints
@app.post("/emergency/process", response_model=ChatResponse)
async def process_emergency_request(request: dict):
    """Process emergency request through professional coordinator"""
    try:
        message = request.get("message", "")
        session_id = request.get("session_id")
        
        # Get client IP (you might want to get this from request headers)
        client_ip = request.get("client_ip")
        
        response = await professional_emergency_coordinator.process_emergency_request(
            message=message,
            user_ip=client_ip,
            session_id=session_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/emergency/dispatch", response_model=ChatResponse)
async def confirm_hospital_dispatch(request: dict):
    """Confirm hospital dispatch and ambulance"""
    try:
        session_id = request.get("session_id")
        hospital_number = request.get("hospital_number")
        phone_number = request.get("phone_number")
        additional_info = request.get("additional_info", "")
        
        response = await professional_emergency_coordinator.confirm_hospital_dispatch(
            session_id=session_id,
            hospital_number=hospital_number,
            phone_number=phone_number,
            additional_info=additional_info
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/emergency/confirm", response_model=ChatResponse)
async def confirm_emergency_action(request: dict):
    """Confirm emergency action"""
    try:
        message_id = request.get("message_id")
        session_id = request.get("session_id")
        confirmed = request.get("confirmed", False)
        
        if confirmed:
            # Get session and process the emergency
            session = professional_emergency_coordinator.location_manager.get_session(session_id)
            if session and session.location:
                # Process emergency with confirmed location
                response = await professional_emergency_coordinator.process_emergency_request(
                    message="Emergency confirmed with location",
                    user_ip=None,
                    session_id=session_id
                )
                return response
            else:
                return ChatResponse(
                    message_id=str(uuid.uuid4()),
                    type="system",
                    content="❌ Location not found. Please provide your location first.",
                    timestamp=datetime.now()
                )
        else:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type="system",
                content="Action cancelled. How else can I help you?",
                timestamp=datetime.now()
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Chat memory management endpoints
@app.get("/ai/session/{session_id}/history")
async def get_session_history(session_id: str):
    """Get chat history for a session (for debugging/monitoring)"""
    try:
        history_info = ai_chat_coordinator.get_session_chat_history(session_id)
        return history_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/ai/session/{session_id}/history")
async def clear_session_history(session_id: str):
    """Clear chat history for a session"""
    try:
        success = ai_chat_coordinator.clear_session_history(session_id)
        return {"success": success, "message": "Session history cleared" if success else "Session not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Fire Emergency Services endpoints
@app.post("/fire/chat", response_model=ChatResponse)
async def fire_emergency_chat(request_data: dict, request: Request):
    """Direct Fire Emergency Services chat with user"""
    try:
        message = request_data.get("message", "")
        session_id = request_data.get("session_id")
        
        # Get client IP from request headers
        client_ip = request.headers.get("x-forwarded-for", request.headers.get("x-real-ip", "127.0.0.1"))
        
        response = await fire_emergency_coordinator.process_fire_emergency_request(
            message=message,
            user_ip=client_ip,
            session_id=session_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/fire/confirm", response_model=ChatResponse)
async def fire_confirm_emergency(request: dict):
    """Confirm fire emergency action"""
    try:
        session_id = request.get("session_id")
        confirmed = request.get("confirmed", False)
        
        if confirmed:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type="system",
                content="✅ Emergency services have been dispatched to your location. Help is on the way!",
                timestamp=datetime.now()
            )
        else:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type="system",
                content="Action cancelled. How else can I help you?",
                timestamp=datetime.now()
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fire/stations")
async def get_emergency_stations():
    """Get list of all emergency stations"""
    try:
        stations = []
        for station in fire_emergency_coordinator.emergency_stations:
            stations.append({
                "id": station.id,
                "name": station.name,
                "type": station.type,
                "address": station.address,
                "area": station.area,
                "contact_numbers": station.contact_numbers,
                "emergency_number": station.emergency_number,
                "services": station.services
            })
        return {"stations": stations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fire/stations/nearby")
async def get_nearby_emergency_stations(lat: float, lon: float, radius: float = 15.0):
    """Get emergency stations near a location"""
    try:
        nearby_stations = fire_emergency_coordinator._find_nearby_stations(lat, lon, radius)
        stations = []
        for station in nearby_stations:
            stations.append({
                "id": station.id,
                "name": station.name,
                "type": station.type,
                "address": station.address,
                "contact_numbers": station.contact_numbers,
                "emergency_number": station.emergency_number,
                "response_time_minutes": station.response_time_minutes,
                "distance_km": station.distance_km
            })
        return {"stations": stations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fire/session/{session_id}/history")
async def get_fire_session_history(session_id: str):
    """Get fire emergency chat history for a session"""
    try:
        history_info = fire_emergency_coordinator.get_session_chat_history(session_id)
        return history_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Police Emergency Services endpoints
@app.post("/police/chat", response_model=ChatResponse)
async def police_emergency_chat(request_data: dict, request: Request):
    """Direct Police Emergency Services chat with user"""
    try:
        message = request_data.get("message", "")
        session_id = request_data.get("session_id")
        
        # Get client IP from request headers
        client_ip = request.headers.get("x-forwarded-for", request.headers.get("x-real-ip", "127.0.0.1"))
        
        response = await police_emergency_coordinator.process_police_emergency_request(
            message=message,
            user_ip=client_ip,
            session_id=session_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/police/confirm", response_model=ChatResponse)
async def police_confirm_emergency(request: dict):
    """Confirm police emergency action"""
    try:
        session_id = request.get("session_id")
        confirmed = request.get("confirmed", False)
        
        if confirmed:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type="system",
                content="✅ Police services have been dispatched to your location. Help is on the way!",
                timestamp=datetime.now()
            )
        else:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type="system",
                content="Action cancelled. How else can I help you?",
                timestamp=datetime.now()
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/police/stations")
async def get_police_stations():
    """Get list of all police stations and units"""
    try:
        stations = []
        for station in police_emergency_coordinator.police_stations:
            stations.append({
                "id": station.id,
                "name": station.name,
                "type": station.type,
                "address": station.address,
                "area": station.area,
                "contact_numbers": station.contact_numbers,
                "emergency_number": station.emergency_number,
                "services": station.services,
                "specialties": station.specialties,
                "jurisdiction": station.jurisdiction
            })
        return {"stations": stations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/police/stations/nearby")
async def get_nearby_police_stations(lat: float, lon: float, radius: float = 15.0):
    """Get police stations near a location"""
    try:
        nearby_stations = police_emergency_coordinator._find_nearby_stations(lat, lon, radius)
        stations = []
        for station in nearby_stations:
            stations.append({
                "id": station.id,
                "name": station.name,
                "type": station.type,
                "address": station.address,
                "contact_numbers": station.contact_numbers,
                "emergency_number": station.emergency_number,
                "response_time_minutes": station.response_time_minutes,
                "specialties": station.specialties,
                "distance_km": station.distance_km
            })
        return {"stations": stations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/police/session/{session_id}/history")
async def get_police_session_history(session_id: str):
    """Get police emergency chat history for a session"""
    try:
        history_info = police_emergency_coordinator.get_session_chat_history(session_id)
        return history_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Multi-Agent Emergency Services Hub endpoints
@app.post("/multi-agent/chat", response_model=ChatResponse)
async def multi_agent_emergency_chat(request_data: dict, request: Request):
    """Master Multi-Agent Emergency Services chat - Routes to appropriate sub-agent"""
    try:
        message = request_data.get("message", "")
        session_id = request_data.get("session_id")
        
        # Get client IP from request headers
        client_ip = request.headers.get("x-forwarded-for", request.headers.get("x-real-ip", "127.0.0.1"))
        
        response = await multi_agent_coordinator.process_emergency_request(
            message=message,
            user_ip=client_ip,
            session_id=session_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/multi-agent/confirm", response_model=ChatResponse)
async def multi_agent_confirm_emergency(request: dict):
    """Confirm multi-agent emergency action"""
    try:
        session_id = request.get("session_id")
        confirmed = request.get("confirmed", False)
        
        if confirmed:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type="system",
                content="✅ Emergency services have been dispatched to your location. Help is on the way!",
                timestamp=datetime.now()
            )
        else:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type="system",
                content="Action cancelled. How else can I help you?",
                timestamp=datetime.now()
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/multi-agent/services")
async def get_emergency_services_summary():
    """Get summary of all available emergency services"""
    try:
        summary = await multi_agent_coordinator.get_emergency_services_summary()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/multi-agent/session/{session_id}/history")
async def get_multi_agent_session_history(session_id: str):
    """Get multi-agent chat history for a session"""
    try:
        history_info = multi_agent_coordinator.get_session_chat_history(session_id)
        return history_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Railway-compatible startup
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)

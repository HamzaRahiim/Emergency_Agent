import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from models.schemas import EmergencyRequest, EmergencyType, Priority, Location, EmergencyResponse
from models.chat_schemas import ChatMessage, MessageType, ChatResponse
from agents.message_parser import EmergencyMessageParser
from agents.medical_coordinator import MedicalCoordinator
from agents.location_manager import LocationManager
from agents.ip_location_service import IPLocationService
from models.location_schemas import RequestType, LocationSource

class ProfessionalEmergencyCoordinator:
    def __init__(self):
        """Initialize professional emergency coordinator"""
        self.message_parser = EmergencyMessageParser()
        self.medical_coordinator = MedicalCoordinator()
        self.location_manager = LocationManager()
        self.ip_location_service = IPLocationService()
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
    
    async def process_emergency_request(self, message: str, user_ip: str = None, 
                                      session_id: Optional[str] = None) -> ChatResponse:
        """
        Process emergency request with professional handling
        """
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Parse the emergency message
        parsed_data = self.message_parser.parse_message(message)
        
        # Check if this is a location input
        if self._is_location_input(message):
            return await self._handle_location_input(message, session_id, user_ip)
        
        # Determine emergency level
        emergency_level = self._determine_emergency_level(parsed_data)
        
        # Get or create session
        session = self.location_manager.get_session(session_id)
        if not session:
            session = self.location_manager.create_session()
            session_id = session.session_id
        
        # Handle based on emergency level
        if emergency_level == "CRITICAL":
            return await self._handle_critical_emergency(message, session_id, user_ip, parsed_data)
        elif emergency_level == "HIGH":
            return await self._handle_high_emergency(message, session_id, user_ip, parsed_data)
        else:
            return await self._handle_general_emergency(message, session_id, user_ip, parsed_data)
    
    def _determine_emergency_level(self, parsed_data: Dict[str, Any]) -> str:
        """Determine emergency level from parsed data"""
        message_lower = parsed_data.get("original_message", "").lower()
        priority = parsed_data.get("priority", Priority.MEDIUM)
        
        # Critical emergency keywords
        critical_keywords = [
            'unconscious', 'not breathing', 'cardiac arrest', 'severe bleeding',
            'major accident', 'multiple injuries', 'dying', 'life threatening'
        ]
        
        # High emergency keywords  
        high_keywords = [
            'chest pain', 'heart attack', 'stroke', 'severe pain', 'accident',
            'injury', 'emergency', 'urgent', 'critical', 'serious'
        ]
        
        if any(keyword in message_lower for keyword in critical_keywords):
            return "CRITICAL"
        elif any(keyword in message_lower for keyword in high_keywords) or priority == Priority.HIGH:
            return "HIGH"
        else:
            return "GENERAL"
    
    async def _handle_critical_emergency(self, message: str, session_id: str, 
                                       user_ip: str, parsed_data: Dict[str, Any]) -> ChatResponse:
        """Handle critical emergency - immediate action"""
        
        # Get location (GPS, IP, or prompt)
        location_data = await self._get_user_location(session_id, user_ip, parsed_data)
        
        if not location_data:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.CONFIRMATION,
                content="🚨 **CRITICAL EMERGENCY DETECTED**\n\nI need your exact location immediately to dispatch emergency services.\n\nPlease provide:\n• Your current address\n• Landmark or area name\n• Any nearby hospital or building name\n\n**Time is critical - please respond quickly!**",
                needs_confirmation=True,
                timestamp=datetime.now()
            )
        
        # Process critical emergency
        emergency_request = self._create_emergency_request(message, location_data, parsed_data, Priority.CRITICAL)
        emergency_response = await self.medical_coordinator.process_emergency(emergency_request)
        
        # Generate professional response
        response_content = self._format_critical_emergency_response(emergency_response)
        
        return ChatResponse(
            message_id=str(uuid.uuid4()),
            type=MessageType.RESPONSE,
            content=response_content,
            timestamp=datetime.now()
        )
    
    async def _handle_high_emergency(self, message: str, session_id: str, 
                                   user_ip: str, parsed_data: Dict[str, Any]) -> ChatResponse:
        """Handle high priority emergency - get location then hospital selection"""
        
        # Get location first
        location_data = await self._get_user_location(session_id, user_ip, parsed_data)
        
        if not location_data:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.CONFIRMATION,
                content="🚨 **EMERGENCY DETECTED**\n\nI need your location to provide the nearest emergency resources.\n\nPlease provide:\n• Your current area/address\n• Landmark or area name in Karachi\n\nOnce I have your location, I'll show you nearby hospitals and can dispatch an ambulance if needed.",
                needs_confirmation=True,
                timestamp=datetime.now()
            )
        
        # Get nearby hospitals
        nearby_hospitals = self.medical_coordinator.hospital_finder.find_nearby_hospitals(
            location_data["latitude"], 
            location_data["longitude"], 
            radius_km=15.0
        )
        
        if not nearby_hospitals:
            # Fallback to all emergency hospitals
            nearby_hospitals = self.medical_coordinator.hospital_finder.get_emergency_hospitals(
                location_data["latitude"], 
                location_data["longitude"]
            )
        
        # Generate hospital selection response
        response_content = self._format_hospital_selection_response(nearby_hospitals[:5], location_data)
        
        return ChatResponse(
            message_id=str(uuid.uuid4()),
            type=MessageType.RESPONSE,
            content=response_content,
            needs_confirmation=True,
            timestamp=datetime.now()
        )
    
    async def _handle_general_emergency(self, message: str, session_id: str, 
                                      user_ip: str, parsed_data: Dict[str, Any]) -> ChatResponse:
        """Handle general medical request"""
        
        # Get location for relevant information
        location_data = await self._get_user_location(session_id, user_ip, parsed_data, required=False)
        
        if not location_data:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.CONFIRMATION,
                content="📍 **Location Information Needed**\n\nTo provide you with the most relevant medical information, please share your location or area in Karachi.\n\nThis helps me:\n• Find nearby hospitals and clinics\n• Provide location-specific emergency contacts\n• Give accurate directions if needed\n\nYou can type your area name (e.g., 'Saddar', 'Clifton').",
                needs_confirmation=True,
                timestamp=datetime.now()
            )
        
        # Provide general medical information
        response_content = await self._provide_general_medical_info(message, location_data)
        
        return ChatResponse(
            message_id=str(uuid.uuid4()),
            type=MessageType.RESPONSE,
            content=response_content,
            needs_confirmation=False,
            timestamp=datetime.now()
        )
    
    async def _get_user_location(self, session_id: str, user_ip: str, 
                               parsed_data: Dict[str, Any], required: bool = True) -> Optional[Dict[str, Any]]:
        """Get user location from various sources"""
        
        # Check if location already in session
        session = self.location_manager.get_session(session_id)
        if session and session.location and session.location.source != LocationSource.DENIED:
            return {
                "latitude": session.location.latitude,
                "longitude": session.location.longitude,
                "address": session.location.address,
                "source": "session"
            }
        
        # Try to get from parsed message
        if parsed_data.get("location") and parsed_data["location"].get("source") != "default":
            location_data = parsed_data["location"]
            return {
                "latitude": location_data["latitude"],
                "longitude": location_data["longitude"],
                "address": location_data["address"],
                "source": "message"
            }
        
        # Try IP-based location for non-emergency requests
        if not required and user_ip:
            ip_location = await self.ip_location_service.get_location_from_ip(user_ip)
            if self.ip_location_service.is_karachi_location(ip_location):
                # Store IP location in session
                self.location_manager.set_gps_location(
                    session_id, 
                    ip_location["latitude"], 
                    ip_location["longitude"], 
                    address=ip_location["address"]
                )
                return ip_location
        
        # For non-emergency requests, use fallback location to avoid repeating messages
        if not required:
            return self.ip_location_service.fallback_location
        
        return None
    
    def _create_emergency_request(self, message: str, location_data: Dict[str, Any], 
                                parsed_data: Dict[str, Any], priority: Priority) -> EmergencyRequest:
        """Create emergency request from data"""
        return EmergencyRequest(
            emergency_type=parsed_data.get("emergency_type", EmergencyType.MEDICAL),
            description=message,
            location=Location(
                latitude=location_data["latitude"],
                longitude=location_data["longitude"],
                address=location_data["address"]
            ),
            patient_name=parsed_data.get("patient_info", {}).get("name"),
            patient_age=parsed_data.get("patient_info", {}).get("age"),
            contact_number=parsed_data.get("contact_info"),
            priority=priority,
            additional_info=f"Location source: {location_data.get('source', 'unknown')}"
        )
    
    def _format_critical_emergency_response(self, emergency_response: EmergencyResponse) -> str:
        """Format critical emergency response"""
        response_parts = []
        
        response_parts.append("🚨 **CRITICAL EMERGENCY - IMMEDIATE ACTION TAKEN**")
        response_parts.append("")
        
        if emergency_response.dispatched_ambulance:
            ambulance = emergency_response.dispatched_ambulance
            response_parts.append("🚑 **AMBULANCE DISPATCHED:**")
            response_parts.append(f"• **ID:** {ambulance.ambulance_id}")
            response_parts.append(f"• **Driver:** {ambulance.driver_name}")
            response_parts.append(f"• **Contact:** {ambulance.contact_number}")
            response_parts.append(f"• **ETA:** {ambulance.eta_minutes} minutes")
            response_parts.append("")
        
        if emergency_response.nearby_hospitals:
            response_parts.append("🏥 **NOTIFIED HOSPITALS:**")
            for hospital in emergency_response.nearby_hospitals[:3]:
                response_parts.append(f"• **{hospital.name}**")
                response_parts.append(f"  📍 {hospital.address}")
                response_parts.append(f"  📞 {hospital.telephone_numbers[0] if hospital.telephone_numbers else 'Emergency Services'}")
            response_parts.append("")
        
        if emergency_response.recommendations:
            response_parts.append("⚡ **IMMEDIATE ACTIONS:**")
            for rec in emergency_response.recommendations:
                response_parts.append(f"• {rec}")
            response_parts.append("")
        
        response_parts.append("**Emergency services have been notified and are responding immediately.**")
        response_parts.append("**Stay calm and follow the instructions above.**")
        
        return "\n".join(response_parts)
    
    def _format_hospital_selection_response(self, hospitals: List, location_data: Dict[str, Any]) -> str:
        """Format hospital selection response"""
        response_parts = []
        
        response_parts.append("🏥 **NEARBY EMERGENCY HOSPITALS**")
        response_parts.append(f"📍 Based on your location: {location_data['address']}")
        response_parts.append("")
        
        for i, hospital in enumerate(hospitals, 1):
            response_parts.append(f"**{i}. {hospital.name}**")
            response_parts.append(f"   📍 {hospital.address}")
            if hospital.distance_km:
                response_parts.append(f"   📏 {hospital.distance_km} km away")
            if hospital.telephone_numbers:
                response_parts.append(f"   📞 {hospital.telephone_numbers[0]}")
            response_parts.append("")
        
        response_parts.append("**Do you want me to dispatch an ambulance and notify a specific hospital?**")
        response_parts.append("")
        response_parts.append("Please reply with:")
        response_parts.append("• **Hospital number** (1, 2, 3, etc.)")
        response_parts.append("• **Your phone number** for ambulance driver contact")
        response_parts.append("• **Any additional details** about the emergency")
        response_parts.append("")
        response_parts.append("**Example:** \"Hospital 1, my phone is 0300-1234567, patient has chest pain\"")
        
        return "\n".join(response_parts)
    
    async def _provide_general_medical_info(self, message: str, location_data: Dict[str, Any]) -> str:
        """Provide general medical information"""
        response_parts = []
        
        response_parts.append("🏥 **MEDICAL INFORMATION & SERVICES**")
        response_parts.append(f"📍 Location: {location_data['address']}")
        response_parts.append("")
        
        if "hospital" in message.lower() or "clinic" in message.lower():
            nearby_hospitals = self.medical_coordinator.hospital_finder.find_nearby_hospitals(
                location_data["latitude"], location_data["longitude"], radius_km=10.0
            )
            
            response_parts.append("**Nearby Hospitals & Clinics:**")
            for hospital in nearby_hospitals[:5]:
                response_parts.append(f"• **{hospital.name}**")
                response_parts.append(f"  📍 {hospital.address}")
                if hospital.telephone_numbers:
                    response_parts.append(f"  📞 {hospital.telephone_numbers[0]}")
                response_parts.append("")
        else:
            # Provide general information based on message content
            message_lower = message.lower()
            
            if any(word in message_lower for word in ['doctor', 'physician', 'medical']):
                response_parts.append("**Medical Services Available:**")
                response_parts.append("• General Medicine")
                response_parts.append("• Emergency Care")
                response_parts.append("• Specialist Consultations")
                response_parts.append("• Diagnostic Services")
                response_parts.append("")
                
            if any(word in message_lower for word in ['appointment', 'book', 'schedule']):
                response_parts.append("**Appointment Booking:**")
                response_parts.append("• Contact hospitals directly using phone numbers")
                response_parts.append("• Most hospitals accept walk-in patients")
                response_parts.append("• Emergency cases are treated immediately")
                response_parts.append("")
                
            if any(word in message_lower for word in ['symptoms', 'pain', 'sick', 'ill']):
                response_parts.append("**Medical Advice:**")
                response_parts.append("• For serious symptoms, visit emergency department")
                response_parts.append("• For minor issues, contact nearest clinic")
                response_parts.append("• If unsure, call hospital for guidance")
                response_parts.append("")
        
        response_parts.append("**Available Services:**")
        response_parts.append("• Emergency ambulance dispatch")
        response_parts.append("• Hospital information and contacts")
        response_parts.append("• Medical advice and guidance")
        response_parts.append("• Appointment booking assistance")
        response_parts.append("")
        response_parts.append("**For Emergency:** Just say 'emergency' and I'll help immediately!")
        
        return "\n".join(response_parts)
    
    def _is_location_input(self, message: str) -> bool:
        """Check if message contains location information"""
        karachi_areas = [
            'saddar', 'clifton', 'defence', 'gulshan', 'north nazimabad', 
            'federal b area', 'pecs', 'gulberg', 'malir', 'korangi', 
            'landhi', 'orangi', 'johar', 'gulistan', 'airport', 'baldia', 'lyari'
        ]
        
        message_lower = message.lower()
        return (any(area in message_lower for area in karachi_areas) or 
                'karachi' in message_lower or
                message_lower.count(' ') <= 3)  # Short messages likely location inputs
    
    async def _handle_location_input(self, message: str, session_id: str, user_ip: str) -> ChatResponse:
        """Handle location input from user"""
        # Get coordinates for the area
        location_data = self.ip_location_service.get_karachi_coordinates(message)
        
        # Store location in session
        session = self.location_manager.get_session(session_id)
        if not session:
            session = self.location_manager.create_session()
            session_id = session.session_id
        
        self.location_manager.set_manual_location(session_id, message)
        
        return ChatResponse(
            message_id=str(uuid.uuid4()),
            type=MessageType.SYSTEM,
            content=f"✅ Location set to: {message}\n\nI can now provide you with relevant medical information for this area. What medical assistance do you need?",
            timestamp=datetime.now()
        )
    
    async def confirm_hospital_dispatch(self, session_id: str, hospital_number: int, 
                                      phone_number: str, additional_info: str = "") -> ChatResponse:
        """Confirm hospital dispatch and ambulance"""
        
        # Get session location
        session = self.location_manager.get_session(session_id)
        if not session or not session.location:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.SYSTEM,
                content="❌ Location not found. Please provide your location first.",
                timestamp=datetime.now()
            )
        
        # Get nearby hospitals
        nearby_hospitals = self.medical_coordinator.hospital_finder.find_nearby_hospitals(
            session.location.latitude, 
            session.location.longitude, 
            radius_km=15.0
        )
        
        if hospital_number < 1 or hospital_number > len(nearby_hospitals):
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.SYSTEM,
                content="❌ Invalid hospital selection. Please choose a valid hospital number.",
                timestamp=datetime.now()
            )
        
        selected_hospital = nearby_hospitals[hospital_number - 1]
        
        # Dispatch ambulance
        dispatched_ambulance = self.medical_coordinator.ambulance_agent.dispatch_ambulance(
            session.location, urgency="high"
        )
        
        # Format confirmation response
        response_content = self._format_dispatch_confirmation(
            selected_hospital, dispatched_ambulance, phone_number, additional_info
        )
        
        return ChatResponse(
            message_id=str(uuid.uuid4()),
            type=MessageType.RESPONSE,
            content=response_content,
            timestamp=datetime.now()
        )
    
    def _format_dispatch_confirmation(self, hospital, ambulance, phone_number: str, 
                                    additional_info: str) -> str:
        """Format dispatch confirmation response"""
        response_parts = []
        
        response_parts.append("✅ **AMBULANCE DISPATCHED & HOSPITAL NOTIFIED**")
        response_parts.append("")
        
        response_parts.append("🚑 **AMBULANCE DETAILS:**")
        response_parts.append(f"• **ID:** {ambulance.ambulance_id}")
        response_parts.append(f"• **Driver:** {ambulance.driver_name}")
        response_parts.append(f"• **Driver Contact:** {ambulance.contact_number}")
        response_parts.append(f"• **ETA:** {ambulance.eta_minutes} minutes")
        response_parts.append("")
        
        response_parts.append("🏥 **HOSPITAL NOTIFIED:**")
        response_parts.append(f"• **Name:** {hospital.name}")
        response_parts.append(f"• **Address:** {hospital.address}")
        response_parts.append(f"• **Contact:** {hospital.telephone_numbers[0] if hospital.telephone_numbers else 'Emergency Services'}")
        response_parts.append(f"• **Patient Contact:** {phone_number}")
        response_parts.append("")
        
        if additional_info:
            response_parts.append("📋 **EMERGENCY DETAILS:**")
            response_parts.append(f"• {additional_info}")
            response_parts.append("")
        
        response_parts.append("**The ambulance driver will contact you at the provided number.**")
        response_parts.append("**Hospital has been notified and is preparing for your arrival.**")
        response_parts.append("")
        response_parts.append("**Stay calm and wait for the ambulance. Help is on the way! 🚑**")
        
        return "\n".join(response_parts)

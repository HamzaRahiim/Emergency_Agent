import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from models.schemas import EmergencyRequest, EmergencyType, Priority, Location, EmergencyResponse
from models.chat_schemas import ChatMessage, MessageType, ChatResponse
from agents.message_parser import EmergencyMessageParser
from agents.medical_coordinator import MedicalCoordinator
from agents.location_manager import LocationManager
from models.location_schemas import RequestType, LocationSource

class ChatCoordinator:
    def __init__(self):
        """Initialize chat coordinator for conversational emergency handling"""
        self.message_parser = EmergencyMessageParser()
        self.medical_coordinator = MedicalCoordinator()
        self.location_manager = LocationManager()
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
    
    async def process_chat_message(self, message: str, user_location: Optional[Dict] = None, 
                                 session_id: Optional[str] = None) -> ChatResponse:
        """
        Process incoming chat message and return appropriate response
        """
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Parse the message
        parsed_data = self.message_parser.parse_message(message, user_location)
        
        # Check if we need confirmation
        if parsed_data["needs_confirmation"]:
            return self._generate_confirmation_response(parsed_data, session_id)
        
        # If we have enough information, process the emergency
        if parsed_data["confidence_score"] > 0.7:
            return await self._process_emergency(parsed_data, session_id)
        
        # Otherwise, ask for clarification
        return self._generate_clarification_response(parsed_data, session_id)
    
    async def handle_location_request(self, session_id: str, latitude: Optional[float] = None,
                                    longitude: Optional[float] = None, address: Optional[str] = None,
                                    accuracy: Optional[float] = None) -> ChatResponse:
        """Handle location data from user"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Get or create session
        session = self.location_manager.get_session(session_id)
        if not session:
            session = self.location_manager.create_session()
            session_id = session.session_id
        
        # Set location based on provided data
        if latitude and longitude:
            # GPS location
            self.location_manager.set_gps_location(
                session_id, latitude, longitude, accuracy, address
            )
            message = "📍 Location received! I can now provide accurate emergency services for your area."
        elif address:
            # Manual location
            self.location_manager.set_manual_location(session_id, address)
            message = f"📍 Location set to: {address}. I can now provide emergency services for this area."
        else:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.SYSTEM,
                content="❌ Location data is incomplete. Please provide either GPS coordinates or address.",
                timestamp=datetime.now()
            )
        
        return ChatResponse(
            message_id=str(uuid.uuid4()),
            type=MessageType.SYSTEM,
            content=message,
            timestamp=datetime.now()
        )
    
    async def handle_phone_request(self, session_id: str, phone_number: str, 
                                 country_code: str = "+92") -> ChatResponse:
        """Handle phone number verification request"""
        if not session_id:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.SYSTEM,
                content="❌ Session not found. Please start a new emergency request.",
                timestamp=datetime.now()
            )
        
        # Set phone verification
        success = self.location_manager.set_phone_verification(session_id, phone_number, country_code)
        
        if success:
            message = f"📞 Phone number verified: {country_code}{phone_number}. Emergency services can now contact you if needed."
        else:
            message = "❌ Failed to verify phone number. Please try again."
        
        return ChatResponse(
            message_id=str(uuid.uuid4()),
            type=MessageType.SYSTEM,
            content=message,
            timestamp=datetime.now()
        )
    
    async def check_requirements_and_process(self, message: str, session_id: str) -> ChatResponse:
        """Check requirements and process request based on type"""
        # Detect request type
        request_type = self.location_manager.detect_request_type(message)
        
        # Get session
        session = self.location_manager.get_session(session_id)
        if not session:
            session = self.location_manager.create_session()
            session_id = session.session_id
        
        # Update session with request type
        session.request_type = request_type
        session.last_activity = datetime.now()
        
        # Check if it's an emergency
        is_emergency = request_type == RequestType.EMERGENCY or self._is_emergency_message(message)
        session.emergency_detected = is_emergency
        
        if is_emergency:
            return await self._handle_emergency_with_requirements(message, session_id)
        else:
            return await self._handle_non_emergency_with_location(message, session_id)
    
    async def _handle_emergency_with_requirements(self, message: str, session_id: str) -> ChatResponse:
        """Handle emergency request with location and phone requirements"""
        # Check emergency requirements
        requirements = self.location_manager.check_emergency_requirements(session_id)
        
        if not requirements.can_proceed:
            # Build missing requirements message
            missing_parts = []
            if "location" in requirements.missing_requirements:
                missing_parts.append("📍 **Location** (required for emergency response)")
            if "phone" in requirements.missing_requirements:
                missing_parts.append("📞 **Phone number** (required for emergency contact)")
            
            response_content = "🚨 **EMERGENCY DETECTED** - I need additional information to proceed:\n\n"
            response_content += "\n".join(missing_parts)
            response_content += "\n\nPlease provide the missing information so I can dispatch emergency services immediately."
            
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.CONFIRMATION,
                content=response_content,
                needs_confirmation=True,
                timestamp=datetime.now()
            )
        
        # All requirements met, process emergency
        return await self._process_emergency_with_session(message, session_id)
    
    async def _handle_non_emergency_with_location(self, message: str, session_id: str) -> ChatResponse:
        """Handle non-emergency request with location requirement"""
        # Validate location
        location_validation = self.location_manager.validate_location(session_id)
        
        if not location_validation.is_valid:
            response_content = "📍 **Location Required**\n\n"
            response_content += f"I need your location to provide relevant information: {location_validation.error_message}\n\n"
            
            if location_validation.suggestions:
                response_content += "**Suggestions:**\n"
                for suggestion in location_validation.suggestions:
                    response_content += f"• {suggestion}\n"
            
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.CONFIRMATION,
                content=response_content,
                needs_confirmation=True,
                timestamp=datetime.now()
            )
        
        # Location is valid, process request
        return await self._process_information_request(message, session_id)
    
    def _is_emergency_message(self, message: str) -> bool:
        """Check if message indicates emergency"""
        emergency_keywords = [
            'emergency', 'urgent', 'critical', 'help', 'accident', 'injury',
            'pain', 'unconscious', 'bleeding', 'chest pain', 'heart attack',
            'stroke', 'breathing', 'asap', 'immediately', 'dying', 'serious'
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in emergency_keywords)
    
    async def _process_emergency_with_session(self, message: str, session_id: str) -> ChatResponse:
        """Process emergency with session data"""
        session = self.location_manager.get_session(session_id)
        if not session or not session.location:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.SYSTEM,
                content="❌ Session or location data not found. Please provide location first.",
                timestamp=datetime.now()
            )
        
        # Parse message with location context
        parsed_data = self.message_parser.parse_message(message, {
            "latitude": session.location.latitude,
            "longitude": session.location.longitude,
            "address": session.location.address
        })
        
        # Process emergency
        return await self._process_emergency(parsed_data, session_id)
    
    async def _process_information_request(self, message: str, session_id: str) -> ChatResponse:
        """Process non-emergency information request"""
        session = self.location_manager.get_session(session_id)
        if not session or not session.location:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.SYSTEM,
                content="❌ Location data not found. Please provide location first.",
                timestamp=datetime.now()
            )
        
        # For information requests, we can provide general info without full emergency processing
        response_content = f"📍 **Location-Based Information**\n\n"
        response_content += f"Based on your location: {session.location.address}\n\n"
        
        if "hospital" in message.lower() or "clinic" in message.lower():
            response_content += "🏥 **Nearby Hospitals:**\n"
            # Get nearby hospitals (simplified)
            response_content += "• Anklesaria Nursing Home - Junction of Randal Garden Road\n"
            response_content += "• Hashmanis Hospital - JM-75, Jacob Lines\n"
            response_content += "• J.J. Hospital & Nursing Home - Al-Haroon Chambers\n\n"
            response_content += "For emergency services, please mention 'emergency' in your message."
        
        elif "doctor" in message.lower() or "appointment" in message.lower():
            response_content += "👨‍⚕️ **Appointment Services:**\n"
            response_content += "I can help you book appointments at nearby hospitals.\n"
            response_content += "Please specify:\n"
            response_content += "• Type of consultation needed\n"
            response_content += "• Preferred hospital or doctor\n"
            response_content += "• Urgency level\n\n"
            response_content += "For immediate medical attention, mention 'emergency'."
        
        else:
            response_content += "💡 **Available Services:**\n"
            response_content += "• Hospital information and locations\n"
            response_content += "• Doctor appointments and consultations\n"
            response_content += "• Emergency services (mention 'emergency')\n"
            response_content += "• Medical advice and guidance\n\n"
            response_content += "What specific information do you need?"
        
        return ChatResponse(
            message_id=str(uuid.uuid4()),
            type=MessageType.RESPONSE,
            content=response_content,
            timestamp=datetime.now()
        )
    
    async def confirm_and_process(self, session_id: str, confirmed: bool, 
                                additional_info: Optional[str] = None) -> ChatResponse:
        """
        Handle confirmation response and process emergency
        """
        # Find session by message_id (since session_id is actually message_id in this context)
        session_data = None
        actual_session_id = None
        
        for sid, data in self.active_sessions.items():
            if data.get("message_id") == session_id:
                session_data = data
                actual_session_id = sid
                break
        
        if not session_data:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.SYSTEM,
                content="Sorry, I couldn't find your session. Please start a new emergency request.",
                timestamp=datetime.now()
            )
        
        if not confirmed:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.SYSTEM,
                content="No problem! Please let me know if you need any emergency assistance in the future. Stay safe!",
                timestamp=datetime.now()
            )
        
        # Update session with additional info if provided
        if additional_info:
            session_data["parsed_emergency"] = self.message_parser.parse_message(
                additional_info, session_data.get("user_location")
            )
        
        # Process the emergency
        return await self._process_emergency(session_data["parsed_emergency"], actual_session_id)
    
    def _generate_confirmation_response(self, parsed_data: Dict[str, Any], 
                                      session_id: str) -> ChatResponse:
        """Generate confirmation message"""
        confirmation_message = self.message_parser.generate_confirmation_message(parsed_data)
        
        # Store session data for confirmation
        message_id = str(uuid.uuid4())
        self.active_sessions[session_id] = {
            "message_id": message_id,
            "parsed_emergency": parsed_data,
            "user_location": parsed_data.get("location"),
            "created_at": datetime.now()
        }
        
        return ChatResponse(
            message_id=message_id,
            type=MessageType.CONFIRMATION,
            content=confirmation_message,
            needs_confirmation=True,
            parsed_emergency=parsed_data,
            timestamp=datetime.now()
        )
    
    def _generate_clarification_response(self, parsed_data: Dict[str, Any], 
                                       session_id: str) -> ChatResponse:
        """Generate clarification request"""
        clarification_parts = []
        
        if parsed_data["emergency_type"] is None:
            clarification_parts.append("What type of emergency are you experiencing?")
        
        if parsed_data["location"] and parsed_data["location"].get("source") == "default":
            clarification_parts.append("Which area of Karachi are you in?")
        
        clarification_message = "I need a bit more information to help you better. " + " ".join(clarification_parts)
        
        # Store session data
        message_id = str(uuid.uuid4())
        self.active_sessions[session_id] = {
            "message_id": message_id,
            "parsed_emergency": parsed_data,
            "user_location": parsed_data.get("location"),
            "created_at": datetime.now()
        }
        
        return ChatResponse(
            message_id=message_id,
            type=MessageType.CONFIRMATION,
            content=clarification_message,
            needs_confirmation=True,
            parsed_emergency=parsed_data,
            timestamp=datetime.now()
        )
    
    async def _process_emergency(self, parsed_data: Dict[str, Any], 
                               session_id: str) -> ChatResponse:
        """Process emergency with medical coordinator"""
        try:
            # Create emergency request
            emergency_request = self._create_emergency_request(parsed_data)
            
            # Process with medical coordinator
            emergency_response = await self.medical_coordinator.process_emergency(emergency_request)
            
            # Generate chat response
            response_content = self._format_emergency_response(emergency_response)
            
            # Store successful processing
            self.active_sessions[session_id]["emergency_response"] = emergency_response
            
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.RESPONSE,
                content=response_content,
                needs_confirmation=False,
                parsed_emergency=parsed_data,
                actions_taken=emergency_response.actions_taken,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.SYSTEM,
                content=f"I encountered an issue processing your emergency request: {str(e)}. Please try again or contact emergency services directly.",
                needs_confirmation=False,
                timestamp=datetime.now()
            )
    
    def _create_emergency_request(self, parsed_data: Dict[str, Any]) -> EmergencyRequest:
        """Create EmergencyRequest from parsed data"""
        location_data = parsed_data["location"]
        patient_info = parsed_data.get("patient_info", {})
        
        return EmergencyRequest(
            emergency_type=parsed_data["emergency_type"] or EmergencyType.MEDICAL,
            description=parsed_data["original_message"],
            location=Location(
                latitude=location_data["latitude"],
                longitude=location_data["longitude"],
                address=location_data["address"]
            ),
            patient_name=patient_info.get("name"),
            patient_age=patient_info.get("age"),
            contact_number=parsed_data.get("contact_info"),
            priority=parsed_data["priority"],
            additional_info=f"Parsed from chat message. Confidence: {parsed_data['confidence_score']:.2f}"
        )
    
    def _format_emergency_response(self, emergency_response: EmergencyResponse) -> str:
        """Format emergency response for chat"""
        response_parts = []
        
        # Main response
        response_parts.append(f"🚨 **Emergency Response Activated**")
        response_parts.append(f"Request ID: {emergency_response.request_id}")
        response_parts.append("")
        
        # Actions taken
        if emergency_response.actions_taken:
            response_parts.append("✅ **Actions Taken:**")
            for action in emergency_response.actions_taken:
                response_parts.append(f"   • {action}")
            response_parts.append("")
        
        # Ambulance dispatch
        if emergency_response.dispatched_ambulance:
            ambulance = emergency_response.dispatched_ambulance
            response_parts.append(f"🚑 **Ambulance Dispatched:**")
            response_parts.append(f"   • ID: {ambulance.ambulance_id}")
            response_parts.append(f"   • Driver: {ambulance.driver_name}")
            response_parts.append(f"   • Contact: {ambulance.contact_number}")
            response_parts.append(f"   • ETA: {ambulance.eta_minutes} minutes")
            response_parts.append(f"   • Status: {ambulance.status.upper()}")
            response_parts.append("")
        
        # Appointment booking
        if emergency_response.booked_appointment:
            appointment = emergency_response.booked_appointment
            response_parts.append(f"📅 **Appointment Booked:**")
            response_parts.append(f"   • Hospital: {appointment.hospital_name}")
            response_parts.append(f"   • Doctor: {appointment.doctor_name}")
            response_parts.append(f"   • Time: {appointment.appointment_time.strftime('%Y-%m-%d %H:%M')}")
            response_parts.append("")
        
        # Nearby hospitals
        if emergency_response.nearby_hospitals:
            response_parts.append(f"🏥 **Nearest Hospitals:**")
            for i, hospital in enumerate(emergency_response.nearby_hospitals[:3], 1):
                response_parts.append(f"   {i}. **{hospital.name}**")
                response_parts.append(f"      📍 {hospital.address}")
                if hospital.distance_km:
                    response_parts.append(f"      📏 {hospital.distance_km} km away")
                if hospital.telephone_numbers:
                    response_parts.append(f"      📞 {hospital.telephone_numbers[0]}")
            response_parts.append("")
        
        # Recommendations
        if emergency_response.recommendations:
            response_parts.append("💡 **Immediate Actions:**")
            for rec in emergency_response.recommendations:
                response_parts.append(f"   • {rec}")
            response_parts.append("")
        
        # Follow-up instructions
        if emergency_response.follow_up_instructions:
            response_parts.append("📋 **Follow-up Instructions:**")
            for inst in emergency_response.follow_up_instructions:
                response_parts.append(f"   • {inst}")
            response_parts.append("")
        
        # AI analysis
        if emergency_response.ai_analysis:
            response_parts.append(f"🤖 **AI Analysis:** {emergency_response.ai_analysis}")
        
        response_parts.append("")
        response_parts.append("**Stay calm and follow the instructions above. Help is on the way! 🚑**")
        
        return "\n".join(response_parts)
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session information"""
        return self.active_sessions.get(session_id)
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """Clean up old sessions"""
        current_time = datetime.now()
        sessions_to_remove = []
        
        for session_id, session_data in self.active_sessions.items():
            age = current_time - session_data["created_at"]
            if age.total_seconds() > max_age_hours * 3600:
                sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            del self.active_sessions[session_id]

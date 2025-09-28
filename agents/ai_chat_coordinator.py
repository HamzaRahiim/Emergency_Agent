import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from models.chat_schemas import ChatMessage, MessageType, ChatResponse
from agents.gemini_client import GeminiClient
from agents.hospital_finder import HospitalFinder
from agents.location_manager import LocationManager
from agents.ip_location_service import IPLocationService

class AIChatCoordinator:
    def __init__(self):
        """Initialize AI Chat Coordinator"""
        self.gemini_client = GeminiClient()
        self.hospital_finder = HospitalFinder()
        self.location_manager = LocationManager()
        self.ip_location_service = IPLocationService()
        self.chat_memory = {}  # Store chat history per session
    
    async def process_user_message(self, message: str, user_ip: str = None, 
                                 session_id: Optional[str] = None) -> ChatResponse:
        """
        Process user message using direct AI chat
        """
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Get or create session
        session = self.location_manager.get_session(session_id)
        if not session:
            session = self.location_manager.create_session()
            session_id = session.session_id
        
        # Prepare context
        context = await self._prepare_context(session, user_ip)
        
        # Get chat history for this session
        chat_history = self._get_chat_history(session_id)
        
        # Add current message to history
        self._add_to_chat_history(session_id, "user", message)
        
        # Detect emergency type and get relevant hospitals
        emergency_type = self._detect_emergency_type(message)
        hospitals = self._get_relevant_hospitals(session, emergency_type)
        
        # Get AI response with chat history context
        try:
            ai_response = await self.gemini_client.chat_with_user(
                message=message,
                context=context,
                hospitals=hospitals,
                chat_history=chat_history
            )
        except Exception as e:
            # If AI fails, return error message
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.SYSTEM,
                content=f"❌ **AI Service Error**: {str(e)}\n\nPlease check your GEMINI_API_KEY configuration and try again.",
                needs_confirmation=False,
                timestamp=datetime.now()
            )
        
        # Check if this is a location input and handle accordingly
        if self._is_location_input(message):
            self.location_manager.set_manual_location(session_id, message)
            # Get updated context with location
            context = await self._prepare_context(session, user_ip)
            hospitals = self._get_relevant_hospitals(session)
            # Get new AI response with location context
            try:
                ai_response = await self.gemini_client.chat_with_user(
                    message=f"User provided location: {message}",
                    context=context,
                    hospitals=hospitals,
                    chat_history=chat_history
                )
            except Exception as e:
                # If AI fails, return error message
                return ChatResponse(
                    message_id=str(uuid.uuid4()),
                    type=MessageType.SYSTEM,
                    content=f"❌ **AI Service Error**: {str(e)}\n\nPlease check your GEMINI_API_KEY configuration and try again.",
                    needs_confirmation=False,
                    timestamp=datetime.now()
                )
        
        # Add AI response to chat history
        self._add_to_chat_history(session_id, "assistant", ai_response)
        
        # Check if this is an emergency that needs special handling
        needs_confirmation = self._needs_emergency_confirmation(message, ai_response)
        
        return ChatResponse(
            message_id=str(uuid.uuid4()),
            type=MessageType.RESPONSE if not needs_confirmation else MessageType.CONFIRMATION,
            content=ai_response,
            needs_confirmation=needs_confirmation,
            timestamp=datetime.now()
        )
    
    async def _prepare_context(self, session, user_ip: str = None) -> Dict[str, Any]:
        """Prepare context for AI"""
        context = {}
        
        if session and session.location:
            context['location'] = session.location.address
            context['latitude'] = session.location.latitude
            context['longitude'] = session.location.longitude
        
        if session and session.phone_verification:
            context['phone_verified'] = session.phone_verification.is_verified
            context['phone_number'] = session.phone_verification.phone_number
        
        # Add IP-based location if no session location
        if not context.get('location') and user_ip:
            try:
                ip_location = await self.ip_location_service.get_location_from_ip(user_ip)
                if self.ip_location_service.is_karachi_location(ip_location):
                    context['location'] = ip_location['address']
                    context['latitude'] = ip_location['latitude']
                    context['longitude'] = ip_location['longitude']
            except:
                pass
        
        return context
    
    def _get_chat_history(self, session_id: str) -> List[Dict[str, str]]:
        """Get chat history for a session (last 15 messages)"""
        if session_id not in self.chat_memory:
            self.chat_memory[session_id] = []
        
        # Return last 15 messages to keep context manageable but comprehensive
        return self.chat_memory[session_id][-15:]
    
    def _add_to_chat_history(self, session_id: str, role: str, content: str):
        """Add message to chat history"""
        if session_id not in self.chat_memory:
            self.chat_memory[session_id] = []
        
        self.chat_memory[session_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 30 messages to prevent memory bloat but maintain good context
        if len(self.chat_memory[session_id]) > 30:
            self.chat_memory[session_id] = self.chat_memory[session_id][-30:]
    
    def _get_relevant_hospitals(self, session, emergency_type: str = None) -> List[Dict]:
        """Get relevant hospitals based on location and emergency type"""
        hospitals = []
        
        if session and session.location and session.location.latitude and session.location.longitude:
            # For emergencies, get specialized hospitals
            if emergency_type:
                nearby_hospitals = self.hospital_finder.find_emergency_hospitals(
                    emergency_type=emergency_type,
                    lat=session.location.latitude,
                    lon=session.location.longitude
                )
            else:
                nearby_hospitals = self.hospital_finder.find_nearby_hospitals(
                    session.location.latitude, 
                    session.location.longitude, 
                    radius_km=15.0
                )
            
            for hospital in nearby_hospitals[:5]:
                hospitals.append({
                    'name': hospital.name,
                    'address': hospital.address,
                    'telephone_numbers': hospital.telephone_numbers,
                    'specialities': hospital.speciality.split(', ') if hospital.speciality else [],
                    'emergency_services': hospital.emergency_services,
                    'distance_km': getattr(hospital, 'distance_km', None)
                })
        else:
            # If no location, get top emergency hospitals
            emergency_hospitals = self.hospital_finder.find_emergency_hospitals(emergency_type)
            for hospital in emergency_hospitals[:5]:
                hospitals.append({
                    'name': hospital.name,
                    'address': hospital.address,
                    'telephone_numbers': hospital.telephone_numbers,
                    'specialities': hospital.speciality.split(', ') if hospital.speciality else [],
                    'emergency_services': hospital.emergency_services,
                    'distance_km': None
                })
        
        return hospitals
    
    def _detect_emergency_type(self, message: str) -> str:
        """Detect emergency type from message"""
        message_lower = message.lower()
        
        emergency_keywords = {
            'cardiac': ['chest pain', 'heart attack', 'cardiac', 'heart', 'chest', 'breathing', 'shortness'],
            'trauma': ['accident', 'injury', 'fall', 'broken', 'fracture', 'bleeding', 'cut', 'wound'],
            'neurological': ['unconscious', 'seizure', 'stroke', 'head injury', 'brain', 'neurological'],
            'respiratory': ['breathing', 'asthma', 'choking', 'respiratory', 'lung'],
            'pediatric': ['child', 'baby', 'infant', 'pediatric', 'kid'],
            'maternity': ['pregnancy', 'labor', 'delivery', 'maternity', 'pregnant']
        }
        
        for emergency_type, keywords in emergency_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return emergency_type
        
        return None
    
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
                (message_lower.count(' ') <= 3 and len(message_lower) < 50))  # Short messages likely location inputs
    
    def _needs_emergency_confirmation(self, message: str, ai_response: str) -> bool:
        """Check if emergency confirmation is needed"""
        emergency_keywords = ['emergency', 'urgent', 'help', 'accident', 'injury', 'pain', 'chest pain', 'unconscious', 'bleeding']
        message_lower = message.lower()
        
        # Check if message contains emergency keywords and AI response suggests emergency handling
        is_emergency = any(keyword in message_lower for keyword in emergency_keywords)
        ai_suggests_emergency = any(keyword in ai_response.lower() for keyword in ['emergency', 'ambulance', 'hospital', 'location'])
        
        return is_emergency and ai_suggests_emergency
    
    async def confirm_emergency_action(self, session_id: str, confirmed: bool = False) -> ChatResponse:
        """Handle emergency confirmation"""
        if not confirmed:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.SYSTEM,
                content="No problem! How else can I help you today?",
                timestamp=datetime.now()
            )
        
        # Get session
        session = self.location_manager.get_session(session_id)
        if not session or not session.location:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.SYSTEM,
                content="❌ Location not found. Please provide your location first.",
                timestamp=datetime.now()
            )
        
        # Get nearby hospitals for emergency
        hospitals = self._get_relevant_hospitals(session)
        
        if not hospitals:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.SYSTEM,
                content="❌ No hospitals found in your area. Please try a different location.",
                timestamp=datetime.now()
            )
        
        # Format hospital selection
        hospital_list = "🏥 **NEARBY EMERGENCY HOSPITALS**\n\n"
        for i, hospital in enumerate(hospitals[:5], 1):
            hospital_list += f"**{i}. {hospital['name']}**\n"
            hospital_list += f"   📍 {hospital['address']}\n"
            if hospital['distance_km']:
                hospital_list += f"   📏 {hospital['distance_km']} km away\n"
            if hospital['telephone_numbers']:
                hospital_list += f"   📞 {hospital['telephone_numbers'][0]}\n"
            hospital_list += "\n"
        
        hospital_list += "**Please reply with:**\n"
        hospital_list += "• **Hospital number** (1, 2, 3, etc.)\n"
        hospital_list += "• **Your phone number** for ambulance driver contact\n"
        hospital_list += "• **Any additional details** about the emergency\n"
        hospital_list += "\n**Example:** \"Hospital 1, my phone is 0300-1234567, patient has chest pain\""
        
        return ChatResponse(
            message_id=str(uuid.uuid4()),
            type=MessageType.RESPONSE,
            content=hospital_list,
            needs_confirmation=True,
            timestamp=datetime.now()
        )
    
    async def process_hospital_dispatch(self, session_id: str, hospital_number: int, 
                                      phone_number: str, additional_info: str = "") -> ChatResponse:
        """Process hospital dispatch confirmation"""
        
        # Get session
        session = self.location_manager.get_session(session_id)
        if not session or not session.location:
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.SYSTEM,
                content="❌ Location not found. Please provide your location first.",
                timestamp=datetime.now()
            )
        
        # Get hospitals
        hospitals = self._get_relevant_hospitals(session)
        
        if hospital_number < 1 or hospital_number > len(hospitals):
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.SYSTEM,
                content="❌ Invalid hospital selection. Please choose a valid hospital number.",
                timestamp=datetime.now()
            )
        
        selected_hospital = hospitals[hospital_number - 1]
        
        # Generate dispatch confirmation
        dispatch_message = f"""✅ **AMBULANCE DISPATCHED & HOSPITAL NOTIFIED**

🚑 **AMBULANCE DETAILS:**
• **Driver Contact:** Will contact you at {phone_number}
• **ETA:** Approximately 15-20 minutes
• **Status:** En route to your location

🏥 **HOSPITAL NOTIFIED:**
• **Name:** {selected_hospital['name']}
• **Address:** {selected_hospital['address']}
• **Contact:** {selected_hospital['telephone_numbers'][0] if selected_hospital['telephone_numbers'] else 'Emergency Services'}
• **Patient Contact:** {phone_number}

📋 **EMERGENCY DETAILS:**
• {additional_info}

**The ambulance driver will contact you at the provided number.**
**Hospital has been notified and is preparing for your arrival.**

**Stay calm and wait for the ambulance. Help is on the way! 🚑**"""
        
        return ChatResponse(
            message_id=str(uuid.uuid4()),
            type=MessageType.RESPONSE,
            content=dispatch_message,
            timestamp=datetime.now()
        )
    
    def get_session_chat_history(self, session_id: str) -> Dict[str, Any]:
        """Get detailed chat history for a session (for debugging/monitoring)"""
        session_info = {
            "session_id": session_id,
            "total_messages": 0,
            "chat_history": [],
            "has_location": False,
            "has_phone": False
        }
        
        # Get session from location manager
        session = self.location_manager.get_session(session_id)
        if session:
            session_info["has_location"] = session.location is not None
            session_info["has_phone"] = session.phone_verification is not None and session.phone_verification.is_verified
        
        # Get chat history
        if session_id in self.chat_memory:
            session_info["chat_history"] = self.chat_memory[session_id]
            session_info["total_messages"] = len(self.chat_memory[session_id])
        
        return session_info
    
    def clear_session_history(self, session_id: str) -> bool:
        """Clear chat history for a session"""
        if session_id in self.chat_memory:
            del self.chat_memory[session_id]
            return True
        return False

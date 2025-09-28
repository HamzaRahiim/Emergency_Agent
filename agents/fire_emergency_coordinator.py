import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from models.chat_schemas import ChatMessage, MessageType, ChatResponse
from agents.gemini_client import GeminiClient
from agents.location_manager import LocationManager
from agents.ip_location_service import IPLocationService

class EmergencyStation:
    """Emergency station data model"""
    def __init__(self, station_data: Dict[str, Any]):
        self.id = station_data.get('id')
        self.name = station_data.get('name')
        self.type = station_data.get('type')
        self.address = station_data.get('address')
        self.area = station_data.get('area')
        self.latitude = station_data.get('latitude')
        self.longitude = station_data.get('longitude')
        self.contact_numbers = station_data.get('contact_numbers', [])
        self.emergency_number = station_data.get('emergency_number')
        self.services = station_data.get('services', [])
        self.vehicles = station_data.get('vehicles', [])
        self.response_time_minutes = station_data.get('response_time_minutes', 15)
        self.operational_hours = station_data.get('operational_hours', '24/7')
        self.specialties = station_data.get('specialties', [])
        self.distance_km = None

class FireEmergencyCoordinator:
    def __init__(self):
        """Initialize Fire Emergency Coordinator"""
        self.gemini_client = GeminiClient()
        self.location_manager = LocationManager()
        self.ip_location_service = IPLocationService()
        self.emergency_stations = self._load_emergency_stations()
        self.chat_memory = {}  # Store chat history per session
    
    def _load_emergency_stations(self) -> List[EmergencyStation]:
        """Load emergency stations from JSON file"""
        stations = []
        try:
            with open('data/karachi_emergency_services.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                for station_data in data:
                    station = EmergencyStation(station_data)
                    stations.append(station)
                print(f"Loaded {len(stations)} emergency stations")
                return stations
        except FileNotFoundError:
            print("Warning: Emergency services data not found")
            return []
        except Exception as e:
            print(f"Error loading emergency stations: {e}")
            return []
    
    async def process_fire_emergency_request(self, message: str, user_ip: str = None, 
                                           session_id: Optional[str] = None) -> ChatResponse:
        """
        Process fire/emergency service request
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
        
        # Detect emergency type and get relevant stations
        emergency_type = self._detect_emergency_type(message)
        stations = self._get_relevant_stations(session, emergency_type)
        
        # Get AI response with chat history context
        try:
            ai_response = await self.gemini_client.chat_with_fire_emergency(
                message=message,
                context=context,
                stations=stations,
                chat_history=chat_history,
                emergency_type=emergency_type
            )
        except Exception as e:
            # If AI fails, return error message
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.SYSTEM,
                content=f"❌ **Emergency Service Error**: {str(e)}\n\nPlease check your GEMINI_API_KEY configuration and try again.",
                needs_confirmation=False,
                timestamp=datetime.now()
            )
        
        # Check if this is a location input and handle accordingly
        if self._is_location_input(message):
            self.location_manager.set_manual_location(session_id, message)
            # Get updated context with location
            context = await self._prepare_context(session, user_ip)
            stations = self._get_relevant_stations(session, emergency_type)
            # Get new AI response with location context
            try:
                ai_response = await self.gemini_client.chat_with_fire_emergency(
                    message=f"User provided location: {message}",
                    context=context,
                    stations=stations,
                    chat_history=chat_history,
                    emergency_type=emergency_type
                )
            except Exception as e:
                return ChatResponse(
                    message_id=str(uuid.uuid4()),
                    type=MessageType.SYSTEM,
                    content=f"❌ **Emergency Service Error**: {str(e)}\n\nPlease check your GEMINI_API_KEY configuration and try again.",
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
    
    def _detect_emergency_type(self, message: str) -> str:
        """Detect emergency type from message"""
        message_lower = message.lower()
        
        emergency_keywords = {
            'fire': ['fire', 'burning', 'smoke', 'flame', 'blaze', 'arson'],
            'police': ['crime', 'robbery', 'theft', 'violence', 'fight', 'police', 'criminal'],
            'rescue': ['accident', 'trapped', 'collapsed', 'disaster', 'rescue', 'stuck'],
            'gas': ['gas leak', 'gas smell', 'gas emergency', 'gas explosion'],
            'power': ['power outage', 'electrical', 'electric shock', 'power line'],
            'water': ['water leak', 'flood', 'water emergency', 'sewer']
        }
        
        for emergency_type, keywords in emergency_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return emergency_type
        
        return None
    
    def _get_relevant_stations(self, session, emergency_type: str = None) -> List[Dict]:
        """Get relevant emergency stations based on location and emergency type"""
        stations = []
        
        if session and session.location and session.location.latitude and session.location.longitude:
            # For emergencies, get specialized stations
            if emergency_type:
                relevant_stations = self._find_emergency_stations(
                    emergency_type=emergency_type,
                    lat=session.location.latitude,
                    lon=session.location.longitude
                )
            else:
                relevant_stations = self._find_nearby_stations(
                    session.location.latitude,
                    session.location.longitude,
                    radius_km=15.0
                )
            
            for station in relevant_stations[:5]:
                stations.append({
                    'name': station.name,
                    'type': station.type,
                    'address': station.address,
                    'contact_numbers': station.contact_numbers,
                    'emergency_number': station.emergency_number,
                    'services': station.services,
                    'vehicles': station.vehicles,
                    'response_time_minutes': station.response_time_minutes,
                    'specialties': station.specialties,
                    'distance_km': station.distance_km
                })
        else:
            # If no location, get top emergency stations by type
            if emergency_type:
                relevant_stations = self._find_emergency_stations(emergency_type)
            else:
                relevant_stations = self.emergency_stations[:5]
            
            for station in relevant_stations:
                stations.append({
                    'name': station.name,
                    'type': station.type,
                    'address': station.address,
                    'contact_numbers': station.contact_numbers,
                    'emergency_number': station.emergency_number,
                    'services': station.services,
                    'vehicles': station.vehicles,
                    'response_time_minutes': station.response_time_minutes,
                    'specialties': station.specialties,
                    'distance_km': None
                })
        
        return stations
    
    def _find_nearby_stations(self, lat: float, lon: float, radius_km: float = 15.0) -> List[EmergencyStation]:
        """Find emergency stations within specified radius"""
        nearby_stations = []
        
        for station in self.emergency_stations:
            if station.latitude and station.longitude:
                distance = self._calculate_distance(lat, lon, station.latitude, station.longitude)
                if distance <= radius_km:
                    station.distance_km = round(distance, 2)
                    nearby_stations.append(station)
        
        # Sort by distance
        nearby_stations.sort(key=lambda s: s.distance_km or float('inf'))
        return nearby_stations
    
    def _find_emergency_stations(self, emergency_type: str = None, lat: float = None, lon: float = None) -> List[EmergencyStation]:
        """Find stations suitable for emergency type"""
        relevant_stations = []
        
        # Map emergency types to station types
        type_mapping = {
            'fire': ['fire_station'],
            'police': ['police_station'],
            'rescue': ['civil_defence', 'rescue_services'],
            'gas': ['gas_services'],
            'power': ['utility_services'],
            'water': ['utility_services']
        }
        
        target_types = type_mapping.get(emergency_type, [])
        
        for station in self.emergency_stations:
            if station.type in target_types:
                relevant_stations.append(station)
        
        # If location provided, sort by distance
        if lat and lon:
            for station in relevant_stations:
                if station.latitude and station.longitude:
                    station.distance_km = self._calculate_distance(lat, lon, station.latitude, station.longitude)
            relevant_stations.sort(key=lambda s: s.distance_km or float('inf'))
        
        return relevant_stations[:10]  # Return top 10 relevant stations
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in kilometers"""
        import math
        
        # Haversine formula
        R = 6371  # Earth's radius in kilometers
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (math.sin(dlat/2) * math.sin(dlat/2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon/2) * math.sin(dlon/2))
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        return distance
    
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
                (message_lower.count(' ') <= 3 and len(message_lower) < 50))
    
    def _needs_emergency_confirmation(self, message: str, ai_response: str) -> bool:
        """Check if emergency confirmation is needed"""
        emergency_keywords = ['fire', 'police', 'emergency', 'urgent', 'help', 'accident', 'crime', 'burning']
        message_lower = message.lower()
        
        # Check if message contains emergency keywords and AI response suggests emergency handling
        is_emergency = any(keyword in message_lower for keyword in emergency_keywords)
        ai_suggests_emergency = any(keyword in ai_response.lower() for keyword in ['emergency', 'dispatch', 'station', 'response'])
        
        return is_emergency and ai_suggests_emergency
    
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

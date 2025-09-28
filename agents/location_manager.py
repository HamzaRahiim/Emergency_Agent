import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
from models.location_schemas import (
    LocationRequest, LocationSource, LocationPermission, PhoneVerification,
    UserSession, LocationValidationResult, EmergencyRequirements, RequestType
)

class LocationManager:
    def __init__(self):
        """Initialize location manager for handling user location and permissions"""
        self.active_sessions: Dict[str, UserSession] = {}
        self.location_timeout = timedelta(hours=24)  # Session timeout
    
    def create_session(self) -> UserSession:
        """Create a new user session"""
        session_id = str(uuid.uuid4())
        session = UserSession(
            session_id=session_id,
            location_permission=LocationPermission(granted=False)
        )
        self.active_sessions[session_id] = session
        return session
    
    def update_location_permission(self, session_id: str, granted: bool, 
                                 denied_reason: Optional[str] = None) -> bool:
        """Update location permission status"""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        session.location_permission.granted = granted
        session.location_permission.denied_reason = denied_reason
        session.last_activity = datetime.now()
        return True
    
    def set_gps_location(self, session_id: str, latitude: float, longitude: float,
                        accuracy: Optional[float] = None, address: Optional[str] = None) -> bool:
        """Set GPS location for session"""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        session.location = LocationRequest(
            latitude=latitude,
            longitude=longitude,
            address=address,
            source=LocationSource.GPS,
            accuracy=accuracy
        )
        session.last_activity = datetime.now()
        return True
    
    def set_manual_location(self, session_id: str, address: str, 
                           latitude: Optional[float] = None, 
                           longitude: Optional[float] = None) -> bool:
        """Set manual location for session"""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        
        # Try to geocode the address if coordinates not provided
        if not latitude or not longitude:
            coordinates = self._geocode_address(address)
            if coordinates:
                latitude, longitude = coordinates
        
        session.location = LocationRequest(
            latitude=latitude,
            longitude=longitude,
            address=address,
            source=LocationSource.MANUAL
        )
        session.last_activity = datetime.now()
        return True
    
    def set_phone_verification(self, session_id: str, phone_number: str, 
                              country_code: str = "+92") -> bool:
        """Set phone verification for session"""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        session.phone_verification = PhoneVerification(
            phone_number=phone_number,
            country_code=country_code,
            verified=True,  # For now, assume verified
            verification_method="user_provided"
        )
        session.last_activity = datetime.now()
        return True
    
    def detect_request_type(self, message: str) -> RequestType:
        """Detect the type of user request from message"""
        message_lower = message.lower()
        
        # Emergency keywords
        emergency_keywords = [
            'emergency', 'urgent', 'critical', 'help', 'accident', 'injury',
            'pain', 'unconscious', 'bleeding', 'chest pain', 'heart attack',
            'stroke', 'breathing', 'asap', 'immediately'
        ]
        
        # Information keywords
        info_keywords = [
            'information', 'info', 'clinic', 'hospital', 'doctor', 'services',
            'symptoms', 'what', 'where', 'how', 'tell me', 'show me'
        ]
        
        # Appointment keywords
        appointment_keywords = [
            'appointment', 'book', 'schedule', 'visit', 'consultation',
            'checkup', 'examination'
        ]
        
        if any(keyword in message_lower for keyword in emergency_keywords):
            return RequestType.EMERGENCY
        elif any(keyword in message_lower for keyword in appointment_keywords):
            return RequestType.APPOINTMENT
        elif any(keyword in message_lower for keyword in info_keywords):
            return RequestType.INFORMATION
        else:
            return RequestType.OTHER
    
    def validate_location(self, session_id: str) -> LocationValidationResult:
        """Validate location data for session"""
        if session_id not in self.active_sessions:
            return LocationValidationResult(
                is_valid=False,
                is_complete=False,
                missing_fields=["session"],
                error_message="Session not found"
            )
        
        session = self.active_sessions[session_id]
        missing_fields = []
        
        if not session.location:
            missing_fields.append("location")
            return LocationValidationResult(
                is_valid=False,
                is_complete=False,
                missing_fields=missing_fields,
                error_message="Location is required but not provided"
            )
        
        location = session.location
        if location.source == LocationSource.DENIED:
            return LocationValidationResult(
                is_valid=False,
                is_complete=False,
                missing_fields=["location_access"],
                error_message="Location access was denied. Please provide manual location.",
                suggestions=["Enter your address manually", "Provide your area in Karachi"]
            )
        
        if location.source == LocationSource.MANUAL and not location.address:
            missing_fields.append("address")
        
        if not location.latitude or not location.longitude:
            missing_fields.append("coordinates")
        
        is_valid = len(missing_fields) == 0
        is_complete = bool(location.address and location.latitude and location.longitude)
        
        return LocationValidationResult(
            is_valid=is_valid,
            is_complete=is_complete,
            missing_fields=missing_fields,
            suggestions=self._get_location_suggestions(missing_fields)
        )
    
    def check_emergency_requirements(self, session_id: str) -> EmergencyRequirements:
        """Check if emergency requirements are met"""
        if session_id not in self.active_sessions:
            return EmergencyRequirements(
                location_required=True,
                phone_required=True,
                missing_requirements=["session", "location", "phone"]
            )
        
        session = self.active_sessions[session_id]
        missing_requirements = []
        
        # Check location
        location_valid = session.location and session.location.source != LocationSource.DENIED
        if not location_valid:
            missing_requirements.append("location")
        
        # Check phone for emergency
        phone_provided = session.phone_verification is not None
        if not phone_provided:
            missing_requirements.append("phone")
        
        can_proceed = len(missing_requirements) == 0
        
        return EmergencyRequirements(
            location_required=True,
            phone_required=True,
            location_provided=bool(location_valid),
            phone_provided=bool(phone_provided),
            can_proceed=can_proceed,
            missing_requirements=missing_requirements
        )
    
    def get_session(self, session_id: str) -> Optional[UserSession]:
        """Get session by ID"""
        return self.active_sessions.get(session_id)
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session in self.active_sessions.items():
            if current_time - session.last_activity > self.location_timeout:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.active_sessions[session_id]
    
    def _geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """Geocode address to coordinates (simplified for Karachi)"""
        # Simplified geocoding for Karachi areas
        karachi_locations = {
            'saddar': (24.8607, 67.0011),
            'clifton': (24.8123, 66.9967),
            'defence': (24.8047, 67.0281),
            'gulshan': (24.8918, 67.0281),
            'north nazimabad': (24.9056, 67.0822),
            'federal b area': (24.9142, 67.0810),
            'pecs': (24.8738, 67.0378),
            'gulberg': (24.9167, 67.0667),
            'malir': (24.9000, 67.1000),
            'korangi': (24.8500, 67.0833),
            'landhi': (24.8833, 67.0667),
            'orangi': (24.9333, 67.0333)
        }
        
        address_lower = address.lower()
        for area, coordinates in karachi_locations.items():
            if area in address_lower:
                return coordinates
        
        # Default to Karachi center if no specific area found
        return (24.8607, 67.0011)
    
    def _get_location_suggestions(self, missing_fields: List[str]) -> List[str]:
        """Get suggestions for missing location fields"""
        suggestions = []
        
        if "location_access" in missing_fields:
            suggestions.append("Allow location access or provide manual address")
        
        if "address" in missing_fields:
            suggestions.append("Enter your complete address including area")
        
        if "coordinates" in missing_fields:
            suggestions.append("Provide area name in Karachi (e.g., 'Saddar', 'Clifton')")
        
        return suggestions

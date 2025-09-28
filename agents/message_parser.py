import re
from typing import Dict, Any, Optional, List
from models.schemas import EmergencyType, Priority, Location
import json

class EmergencyMessageParser:
    def __init__(self):
        """Initialize message parser for natural language emergency requests"""
        self.emergency_keywords = {
            EmergencyType.MEDICAL: ['sick', 'pain', 'fever', 'cough', 'headache', 'nausea', 'dizzy', 'weakness'],
            EmergencyType.CARDIAC: ['chest pain', 'heart', 'cardiac', 'heart attack', 'chest tightness', 'breathing difficulty'],
            EmergencyType.TRAUMA: ['accident', 'fall', 'injury', 'bleeding', 'cut', 'fracture', 'bruise', 'wound'],
            EmergencyType.STROKE: ['stroke', 'paralysis', 'slurred speech', 'numb', 'face droop', 'weakness'],
            EmergencyType.ACCIDENT: ['car accident', 'road accident', 'collision', 'crash', 'hit']
        }
        
        self.priority_keywords = {
            Priority.CRITICAL: ['critical', 'urgent', 'emergency', 'dying', 'unconscious', 'not breathing'],
            Priority.HIGH: ['serious', 'severe', 'bad', 'worse', 'immediately', 'asap'],
            Priority.MEDIUM: ['moderate', 'ok', 'manageable', 'stable'],
            Priority.LOW: ['minor', 'small', 'not urgent', 'later']
        }
        
        # Karachi area patterns
        self.karachi_areas = [
            'saddar', 'clifton', 'defence', 'gulshan', 'north nazimabad', 'federal b area',
            'pecs', 'gulberg', 'malir', 'korangi', 'landhi', 'orangi', 'new karachi',
            'johar', 'gulistan', 'airport', 'baldia', 'lyari', 'old city'
        ]
    
    def parse_message(self, message: str, user_location: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Parse natural language message to extract emergency information
        """
        message_lower = message.lower()
        
        # Extract emergency type
        emergency_type = self._extract_emergency_type(message_lower)
        
        # Extract priority
        priority = self._extract_priority(message_lower)
        
        # Extract location information
        location_info = self._extract_location(message_lower, user_location)
        
        # Extract patient information
        patient_info = self._extract_patient_info(message_lower)
        
        # Extract contact information
        contact_info = self._extract_contact_info(message_lower)
        
        # Check if we need confirmation
        needs_confirmation = self._needs_confirmation(emergency_type, priority, location_info)
        
        return {
            "emergency_type": emergency_type,
            "priority": priority,
            "location": location_info,
            "patient_info": patient_info,
            "contact_info": contact_info,
            "original_message": message,
            "needs_confirmation": needs_confirmation,
            "confidence_score": self._calculate_confidence(emergency_type, priority, location_info)
        }
    
    def _extract_emergency_type(self, message: str) -> Optional[EmergencyType]:
        """Extract emergency type from message"""
        for emergency_type, keywords in self.emergency_keywords.items():
            for keyword in keywords:
                if keyword in message:
                    return emergency_type
        
        # Check for specific emergency patterns
        if any(word in message for word in ['chest pain', 'breathing difficulty', 'heart']):
            return EmergencyType.CARDIAC
        elif any(word in message for word in ['accident', 'crash', 'collision']):
            return EmergencyType.TRAUMA
        elif any(word in message for word in ['stroke', 'paralysis', 'slurred speech']):
            return EmergencyType.STROKE
        
        # Default to medical if no specific type found
        if any(word in message for word in ['help', 'emergency', 'medical', 'doctor', 'hospital']):
            return EmergencyType.MEDICAL
        
        return None
    
    def _extract_priority(self, message: str) -> Priority:
        """Extract priority level from message"""
        for priority, keywords in self.priority_keywords.items():
            for keyword in keywords:
                if keyword in message:
                    return priority
        
        # Default priority based on emergency type keywords
        if any(word in message for word in ['critical', 'urgent', 'emergency', 'dying', 'unconscious']):
            return Priority.CRITICAL
        elif any(word in message for word in ['serious', 'severe', 'bad', 'immediately']):
            return Priority.HIGH
        else:
            return Priority.MEDIUM
    
    def _extract_location(self, message: str, user_location: Optional[Dict] = None) -> Optional[Dict]:
        """Extract location information from message"""
        # Check for Karachi areas mentioned
        mentioned_area = None
        for area in self.karachi_areas:
            if area in message:
                mentioned_area = area
                break
        
        # Use user location if available, otherwise use mentioned area
        if user_location:
            return {
                "latitude": user_location.get("latitude", 24.8607),
                "longitude": user_location.get("longitude", 67.0011),
                "address": user_location.get("address", f"{mentioned_area.title()}, Karachi" if mentioned_area else "Karachi, Pakistan"),
                "source": "user_provided"
            }
        
        # Default Karachi locations based on mentioned area
        default_locations = {
            'saddar': {"lat": 24.8607, "lon": 67.0011, "address": "Saddar, Karachi"},
            'clifton': {"lat": 24.8123, "lon": 66.9967, "address": "Clifton, Karachi"},
            'defence': {"lat": 24.8047, "lon": 67.0281, "address": "Defence Housing Authority, Karachi"},
            'gulshan': {"lat": 24.8918, "lon": 67.0281, "address": "Gulshan-e-Iqbal, Karachi"},
            'north nazimabad': {"lat": 24.9056, "lon": 67.0822, "address": "North Nazimabad, Karachi"},
            'federal b area': {"lat": 24.9142, "lon": 67.0810, "address": "Federal B Area, Karachi"},
            'pecs': {"lat": 24.8738, "lon": 67.0378, "address": "PECHS, Karachi"},
            'gulberg': {"lat": 24.9167, "lon": 67.0667, "address": "Gulberg, Karachi"}
        }
        
        if mentioned_area and mentioned_area in default_locations:
            loc = default_locations[mentioned_area]
            return {
                "latitude": loc["lat"],
                "longitude": loc["lon"],
                "address": loc["address"],
                "source": "area_mentioned"
            }
        
        # Default to Saddar if no location found
        return {
            "latitude": 24.8607,
            "longitude": 67.0011,
            "address": "Saddar, Karachi",
            "source": "default"
        }
    
    def _extract_patient_info(self, message: str) -> Dict[str, Any]:
        """Extract patient information from message"""
        info = {}
        
        # Extract age
        age_pattern = r'(\d+)\s*(?:years?|yrs?|old)'
        age_match = re.search(age_pattern, message)
        if age_match:
            info["age"] = int(age_match.group(1))
        
        # Extract gender
        if any(word in message for word in ['male', 'man', 'boy', 'he', 'him']):
            info["gender"] = "male"
        elif any(word in message for word in ['female', 'woman', 'girl', 'she', 'her']):
            info["gender"] = "female"
        
        # Extract name (simple pattern)
        name_patterns = [
            r'(?:my name is|i am|call me)\s+([a-zA-Z\s]+)',
            r'(?:patient name|name)\s*:?\s*([a-zA-Z\s]+)'
        ]
        for pattern in name_patterns:
            name_match = re.search(pattern, message)
            if name_match:
                info["name"] = name_match.group(1).strip()
                break
        
        return info
    
    def _extract_contact_info(self, message: str) -> Optional[str]:
        """Extract contact number from message"""
        # Pakistani phone number patterns
        phone_patterns = [
            r'\+92[-\s]?\d{3}[-\s]?\d{7}',
            r'0\d{3}[-\s]?\d{7}',
            r'\d{4}[-\s]?\d{7}'
        ]
        
        for pattern in phone_patterns:
            phone_match = re.search(pattern, message)
            if phone_match:
                return phone_match.group(0)
        
        return None
    
    def _needs_confirmation(self, emergency_type: Optional[EmergencyType], 
                          priority: Priority, location_info: Optional[Dict]) -> bool:
        """Determine if we need confirmation before proceeding"""
        # Need confirmation if:
        # 1. Emergency type is unclear
        # 2. Location is default/unknown
        # 3. Priority seems too low for urgent keywords
        
        if emergency_type is None:
            return True
        
        if location_info and location_info.get("source") == "default":
            return True
        
        return False
    
    def _calculate_confidence(self, emergency_type: Optional[EmergencyType], 
                            priority: Priority, location_info: Optional[Dict]) -> float:
        """Calculate confidence score for parsed information"""
        confidence = 0.5  # Base confidence
        
        if emergency_type is not None:
            confidence += 0.3
        
        if location_info and location_info.get("source") != "default":
            confidence += 0.2
        
        if priority in [Priority.HIGH, Priority.CRITICAL]:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def generate_confirmation_message(self, parsed_data: Dict[str, Any]) -> str:
        """Generate confirmation message for unclear requests"""
        emergency_type = parsed_data.get("emergency_type")
        priority = parsed_data.get("priority")
        location = parsed_data.get("location")
        
        message_parts = []
        
        if emergency_type is None:
            message_parts.append("I understand you need emergency help. Could you please specify what type of emergency? (medical, accident, cardiac, etc.)")
        
        if location and location.get("source") == "default":
            message_parts.append("I couldn't determine your exact location. Please tell me which area of Karachi you're in.")
        
        if not message_parts:
            # If everything is clear, just confirm
            return f"I understand you have a {emergency_type.value if emergency_type else 'medical'} emergency with {priority.value} priority. Shall I proceed with getting help?"
        
        return " ".join(message_parts) + " Then I can help you immediately."

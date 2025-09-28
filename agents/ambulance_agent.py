import json
import uuid
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from models.schemas import Ambulance, Location

class AmbulanceAgent:
    def __init__(self):
        """Initialize ambulance agent with mock ambulance fleet"""
        self.ambulances_file = "data/ambulances.json"
        self.ambulances = self._load_ambulances()
        self._initialize_mock_fleet()
    
    def _load_ambulances(self) -> Dict[str, Ambulance]:
        """Load existing ambulances from file"""
        try:
            with open(self.ambulances_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                ambulances = {}
                for ambulance_id, ambulance_data in data.items():
                    ambulances[ambulance_id] = Ambulance(**ambulance_data)
                return ambulances
        except FileNotFoundError:
            return {}
    
    def _save_ambulances(self):
        """Save ambulances to file"""
        import os
        os.makedirs(os.path.dirname(self.ambulances_file), exist_ok=True)
        
        data = {}
        for ambulance_id, ambulance in self.ambulances.items():
            data[ambulance_id] = ambulance.dict()
        
        with open(self.ambulances_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _initialize_mock_fleet(self):
        """Initialize mock ambulance fleet for Karachi"""
        if not self.ambulances:
            # Mock ambulance locations around Karachi
            karachi_locations = [
                {"lat": 24.8607, "lon": 67.0011, "area": "Saddar"},
                {"lat": 24.8918, "lon": 67.0281, "area": "Gulshan-e-Iqbal"},
                {"lat": 24.9056, "lon": 67.0822, "area": "North Nazimabad"},
                {"lat": 24.9142, "lon": 67.0810, "area": "Federal B Area"},
                {"lat": 24.8428, "lon": 67.0042, "area": "Clifton"},
                {"lat": 24.8738, "lon": 67.0378, "area": "PECHS"},
                {"lat": 24.8920, "lon": 67.0290, "area": "Defence"},
                {"lat": 24.9167, "lon": 67.0667, "area": "Gulberg"}
            ]
            
            drivers = [
                "Ali Ahmed", "Mohammad Hassan", "Usman Khan", "Ahmed Ali",
                "Hassan Sheikh", "Khalid Malik", "Omar Khan", "Yusuf Ahmed"
            ]
            
            contact_numbers = [
                "+92-300-1234567", "+92-301-2345678", "+92-302-3456789", "+92-303-4567890",
                "+92-304-5678901", "+92-305-6789012", "+92-306-7890123", "+92-307-8901234"
            ]
            
            specialities = ["general", "cardiac", "trauma", "pediatric"]
            
            for i, location in enumerate(karachi_locations):
                ambulance_id = f"AMB_{i+1:03d}"
                ambulance = Ambulance(
                    ambulance_id=ambulance_id,
                    driver_name=drivers[i % len(drivers)],
                    contact_number=contact_numbers[i % len(contact_numbers)],
                    location=Location(
                        latitude=location["lat"],
                        longitude=location["lon"],
                        address=f"{location['area']}, Karachi"
                    ),
                    status="available",
                    speciality=random.choice(specialities)
                )
                self.ambulances[ambulance_id] = ambulance
            
            self._save_ambulances()
    
    def dispatch_ambulance(self, emergency_location: Location, speciality: str = "general", 
                          urgency: str = "medium") -> Optional[Ambulance]:
        """Dispatch nearest available ambulance"""
        available_ambulances = [amb for amb in self.ambulances.values() 
                               if amb.status == "available"]
        
        if not available_ambulances:
            return None
        
        # Filter by speciality if needed
        if speciality != "general":
            available_ambulances = [amb for amb in available_ambulances 
                                   if amb.speciality == speciality]
        
        if not available_ambulances:
            # Fallback to general ambulances
            available_ambulances = [amb for amb in self.ambulances.values() 
                                   if amb.status == "available"]
        
        # Find nearest ambulance (mock distance calculation)
        nearest_ambulance = min(available_ambulances, 
                               key=lambda amb: self._calculate_distance(
                                   emergency_location.latitude, emergency_location.longitude,
                                   amb.location.latitude, amb.location.longitude))
        
        # Update ambulance status
        nearest_ambulance.status = "dispatched"
        
        # Calculate ETA based on urgency and distance
        base_eta = random.randint(8, 15)  # 8-15 minutes base
        if urgency == "critical":
            nearest_ambulance.eta_minutes = max(5, base_eta - 3)
        elif urgency == "high":
            nearest_ambulance.eta_minutes = base_eta
        else:
            nearest_ambulance.eta_minutes = base_eta + 2
        
        self._save_ambulances()
        return nearest_ambulance
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula"""
        import math
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of earth in kilometers
        r = 6371
        return c * r
    
    def update_ambulance_status(self, ambulance_id: str, status: str, 
                               new_location: Location = None) -> bool:
        """Update ambulance status"""
        if ambulance_id in self.ambulances:
            self.ambulances[ambulance_id].status = status
            if new_location:
                self.ambulances[ambulance_id].location = new_location
            
            # Update ETA based on status
            if status == "on_route":
                self.ambulances[ambulance_id].eta_minutes = random.randint(5, 10)
            elif status == "arrived":
                self.ambulances[ambulance_id].eta_minutes = 0
            elif status == "available":
                self.ambulances[ambulance_id].eta_minutes = None
            
            self._save_ambulances()
            return True
        return False
    
    def get_ambulance_status(self, ambulance_id: str) -> Optional[Ambulance]:
        """Get current status of an ambulance"""
        return self.ambulances.get(ambulance_id)
    
    def get_available_ambulances(self) -> List[Ambulance]:
        """Get all available ambulances"""
        return [amb for amb in self.ambulances.values() if amb.status == "available"]
    
    def get_all_ambulances(self) -> List[Ambulance]:
        """Get all ambulances"""
        return list(self.ambulances.values())

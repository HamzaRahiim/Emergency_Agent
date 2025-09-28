import json
import math
from typing import List, Dict, Any, Optional
from models.schemas import Hospital, Location

class HospitalFinder:
    def __init__(self):
        """Initialize hospital finder with data from JSON files"""
        self.hospitals = self._load_hospitals()
    
    def _load_hospitals(self) -> List[Hospital]:
        """Load hospitals from comprehensive data file"""
        hospitals = []
        
        # Load from comprehensive data file first
        try:
            with open('data/karachi_hospitals_comprehensive.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                for hospital_data in data:
                    hospital = Hospital(
                        id=hospital_data.get('id', f"kar_{len(hospitals) + 1}"),
                        name=hospital_data['name'],
                        address=hospital_data['address'],
                        latitude=hospital_data.get('latitude'),
                        longitude=hospital_data.get('longitude'),
                        telephone_numbers=hospital_data.get('telephone_numbers', []),
                        emergency_services=hospital_data.get('emergency_services', False),
                        speciality=', '.join(hospital_data.get('specialties', []))
                    )
                    hospitals.append(hospital)
                
                print(f"Loaded {len(hospitals)} hospitals from comprehensive data")
                return hospitals
                
        except FileNotFoundError:
            print("Warning: Comprehensive hospital data not found, loading from individual files...")
        
        # Fallback: Load from individual JSON files
        # Load from hospiatl_dataset.json (better structured data)
        try:
            with open('hospiatl_dataset.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                for hospital_data in data.get('hospitals', []):
                    hospital = Hospital(
                        id=f"karachi_{hospital_data['s_no']}",
                        name=hospital_data['name'],
                        address=hospital_data['address'],
                        telephone_numbers=hospital_data['telephone_numbers'],
                        emergency_services=True,
                        speciality=self._determine_speciality(hospital_data['name'])
                    )
                    hospitals.append(hospital)
        except FileNotFoundError:
            print("Warning: hospiatl_dataset.json not found")
        
        # Load from hospital data 2.json (has coordinates)
        try:
            with open('hospital data 2.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                for hospital_data in data:
                    if hospital_data.get('name'):
                        # Skip if we already have this hospital from the first file
                        if not any(h.name == hospital_data['name'] for h in hospitals):
                            hospital = Hospital(
                                id=f"osm_{hospital_data.get('uuid', hospital_data.get('osm_id'))}",
                                name=hospital_data['name'],
                                address="Karachi, Pakistan",  # Default address
                                telephone_numbers=[],
                                latitude=hospital_data.get('X'),
                                longitude=hospital_data.get('Y'),
                                emergency_services=hospital_data.get('amenity') == 'hospital',
                                speciality=self._determine_speciality(hospital_data['name'])
                            )
                            hospitals.append(hospital)
        except FileNotFoundError:
            print("Warning: hospital data 2.json not found")
        
        # Load from karachi_hospitals.json
        try:
            with open('karachi_hospitals.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                for hospital_data in data:
                    if hospital_data.get('HOSPITAL NAME'):
                        # Skip if we already have this hospital
                        if not any(h.name == hospital_data['HOSPITAL NAME'] for h in hospitals):
                            hospital = Hospital(
                                id=f"karachi_{len(hospitals) + 1}",
                                name=hospital_data['HOSPITAL NAME'],
                                address=hospital_data.get('Location', 'Karachi, Pakistan'),
                                telephone_numbers=[hospital_data.get('TELEPHONE NUMBER(S)', '')] if hospital_data.get('TELEPHONE NUMBER(S)') else [],
                                emergency_services=True,
                                speciality=self._determine_speciality(hospital_data['HOSPITAL NAME'])
                            )
                            hospitals.append(hospital)
        except FileNotFoundError:
            print("Warning: karachi_hospitals.json not found")
        
        return hospitals
    
    def _determine_speciality(self, name: str) -> Optional[str]:
        """Determine hospital speciality based on name"""
        name_lower = name.lower()
        if any(word in name_lower for word in ['cardiac', 'heart']):
            return 'cardiology'
        elif any(word in name_lower for word in ['dental']):
            return 'dentistry'
        elif any(word in name_lower for word in ['kidney', 'stone']):
            return 'nephrology'
        elif any(word in name_lower for word in ['children', 'pediatric']):
            return 'pediatrics'
        elif any(word in name_lower for word in ['gynaecologist', 'women']):
            return 'gynecology'
        else:
            return 'general'
    
    def find_nearby_hospitals(self, lat: float, lon: float, radius_km: float = 10.0) -> List[Hospital]:
        """Find hospitals within specified radius"""
        nearby_hospitals = []
        
        for hospital in self.hospitals:
            if hospital.latitude and hospital.longitude:
                # Simple distance calculation using Haversine formula approximation
                distance = self._calculate_distance(lat, lon, hospital.latitude, hospital.longitude)
                
                if distance <= radius_km:
                    hospital.distance_km = round(distance, 2)
                    nearby_hospitals.append(hospital)
        
        # Sort by distance
        nearby_hospitals.sort(key=lambda h: h.distance_km or float('inf'))
        return nearby_hospitals
    
    def find_hospitals_by_speciality(self, speciality: str, lat: float = None, lon: float = None) -> List[Hospital]:
        """Find hospitals by speciality, optionally filtered by location"""
        matching_hospitals = [h for h in self.hospitals if h.speciality == speciality]
        
        if lat and lon:
            # Calculate distances and sort
            for hospital in matching_hospitals:
                if hospital.latitude and hospital.longitude:
                    distance = self._calculate_distance(lat, lon, hospital.latitude, hospital.longitude)
                    hospital.distance_km = round(distance, 2)
            
            matching_hospitals.sort(key=lambda h: h.distance_km or float('inf'))
        
        return matching_hospitals
    
    def find_emergency_hospitals(self, emergency_type: str = None, lat: float = None, lon: float = None) -> List[Hospital]:
        """Find hospitals suitable for emergency type"""
        emergency_hospitals = []
        
        # Filter hospitals with emergency services
        for hospital in self.hospitals:
            if hospital.emergency_services:
                # Check if hospital specializes in the emergency type
                if emergency_type and self._is_relevant_specialty(hospital.speciality, emergency_type):
                    emergency_hospitals.append(hospital)
                elif not emergency_type:
                    emergency_hospitals.append(hospital)
        
        # If location provided, sort by distance
        if lat and lon:
            for hospital in emergency_hospitals:
                if hospital.latitude and hospital.longitude:
                    hospital.distance_km = self._calculate_distance(lat, lon, hospital.latitude, hospital.longitude)
            emergency_hospitals.sort(key=lambda h: h.distance_km or float('inf'))
        
        return emergency_hospitals[:10]  # Return top 10 emergency hospitals
    
    def _is_relevant_specialty(self, hospital_specialty: str, emergency_type: str) -> bool:
        """Check if hospital specialty is relevant to emergency type"""
        emergency_type = emergency_type.lower()
        specialty = hospital_specialty.lower()
        
        # Map emergency types to relevant specialties
        specialty_mapping = {
            'cardiac': ['cardiology', 'heart', 'cardiac', 'coronary'],
            'trauma': ['trauma', 'emergency', 'orthopedics', 'surgery'],
            'pediatric': ['pediatric', 'children', 'child'],
            'neurological': ['neurology', 'neurosurgery', 'brain'],
            'respiratory': ['pulmonology', 'respiratory', 'lung'],
            'burn': ['burn', 'plastic surgery'],
            'maternity': ['maternity', 'obstetrics', 'gynecology']
        }
        
        if emergency_type in specialty_mapping:
            for keyword in specialty_mapping[emergency_type]:
                if keyword in specialty:
                    return True
        
        return False
    
    def get_all_hospitals(self) -> List[Hospital]:
        """Get all available hospitals"""
        return self.hospitals
    
    def get_emergency_hospitals(self, lat: float = None, lon: float = None) -> List[Hospital]:
        """Get hospitals with emergency services"""
        emergency_hospitals = [h for h in self.hospitals if h.emergency_services]
        
        if lat and lon:
            for hospital in emergency_hospitals:
                if hospital.latitude and hospital.longitude:
                    distance = self._calculate_distance(lat, lon, hospital.latitude, hospital.longitude)
                    hospital.distance_km = round(distance, 2)
            
            emergency_hospitals.sort(key=lambda h: h.distance_km or float('inf'))
        
        return emergency_hospitals
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula"""
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

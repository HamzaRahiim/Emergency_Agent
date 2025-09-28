import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from models.schemas import EmergencyRequest, EmergencyResponse, EmergencyType, Priority
from agents.hospital_finder import HospitalFinder
from agents.appointment_agent import AppointmentAgent
from agents.ambulance_agent import AmbulanceAgent
from agents.gemini_client import GeminiClient

class MedicalCoordinator:
    def __init__(self):
        """Initialize medical coordinator with all sub-agents"""
        self.hospital_finder = HospitalFinder()
        self.appointment_agent = AppointmentAgent()
        self.ambulance_agent = AmbulanceAgent()
        self.gemini_client = GeminiClient()
    
    async def process_emergency(self, request: EmergencyRequest) -> EmergencyResponse:
        """
        Main method to process emergency requests
        Optimized for cost - single Gemini call with comprehensive analysis
        """
        request_id = str(uuid.uuid4())
        actions_taken = []
        nearby_hospitals = []
        dispatched_ambulance = None
        booked_appointment = None
        ai_analysis = None
        
        try:
            # Prepare data for AI analysis
            emergency_data = {
                "emergency_type": request.emergency_type.value,
                "description": request.description,
                "location": {
                    "latitude": request.location.latitude,
                    "longitude": request.location.longitude,
                    "address": request.location.address
                },
                "patient_age": request.patient_age,
                "priority": request.priority.value
            }
            
            # Single comprehensive AI analysis call
            ai_insights = await self.gemini_client.analyze_emergency(emergency_data)
            ai_analysis = ai_insights.get("ai_reasoning", "AI analysis completed")
            
            # Find nearby hospitals
            nearby_hospitals = self.hospital_finder.find_nearby_hospitals(
                request.location.latitude, 
                request.location.longitude, 
                radius_km=15.0
            )
            actions_taken.append("Located nearby hospitals")
            
            # Determine if ambulance is needed based on AI analysis
            ambulance_needed = ai_insights.get("ambulance_needed", 
                                             request.priority in [Priority.HIGH, Priority.CRITICAL])
            
            if ambulance_needed:
                # Determine ambulance speciality
                ambulance_speciality = self._map_emergency_to_ambulance_speciality(
                    request.emergency_type, ai_insights.get("hospital_speciality"))
                
                # Dispatch ambulance
                dispatched_ambulance = self.ambulance_agent.dispatch_ambulance(
                    request.location, 
                    speciality=ambulance_speciality,
                    urgency=request.priority.value
                )
                
                if dispatched_ambulance:
                    actions_taken.append(f"Dispatched {ambulance_speciality} ambulance")
                else:
                    actions_taken.append("Ambulance dispatch attempted - no available units")
            
            # Book appointment if not critical emergency
            if request.priority not in [Priority.CRITICAL] and not ambulance_needed:
                # Find best hospital for the emergency type
                recommended_speciality = ai_insights.get("hospital_speciality", "general")
                suitable_hospitals = self.hospital_finder.find_hospitals_by_speciality(
                    recommended_speciality,
                    request.location.latitude,
                    request.location.longitude
                )
                
                if suitable_hospitals:
                    best_hospital = suitable_hospitals[0]
                    booked_appointment = self.appointment_agent.book_appointment(
                        hospital_id=best_hospital.id,
                        hospital_name=best_hospital.name,
                        patient_name=request.patient_name or "Emergency Patient",
                        speciality=recommended_speciality,
                        urgency=request.priority.value
                    )
                    actions_taken.append(f"Booked appointment at {best_hospital.name}")
            
            # Generate recommendations from AI insights
            recommendations = ai_insights.get("first_aid", [])
            follow_up_instructions = ai_insights.get("follow_up", [])
            
            # Add hospital contact information to recommendations
            if nearby_hospitals:
                recommendations.append(f"Nearest hospital: {nearby_hospitals[0].name} - {nearby_hospitals[0].telephone_numbers[0] if nearby_hospitals[0].telephone_numbers else 'Contact through emergency services'}")
            
        except Exception as e:
            # Fallback handling if AI analysis fails
            ai_analysis = f"Emergency processing completed with basic protocols. Error: {str(e)}"
            nearby_hospitals = self.hospital_finder.find_nearby_hospitals(
                request.location.latitude, 
                request.location.longitude, 
                radius_km=10.0
            )
            actions_taken.append("Basic emergency protocols activated")
            
            # Basic ambulance dispatch for high priority
            if request.priority in [Priority.HIGH, Priority.CRITICAL]:
                dispatched_ambulance = self.ambulance_agent.dispatch_ambulance(
                    request.location, urgency=request.priority.value)
                if dispatched_ambulance:
                    actions_taken.append("Emergency ambulance dispatched")
        
        return EmergencyResponse(
            request_id=request_id,
            emergency_type=request.emergency_type,
            priority=request.priority,
            actions_taken=actions_taken,
            nearby_hospitals=nearby_hospitals[:5],  # Limit to top 5
            dispatched_ambulance=dispatched_ambulance,
            booked_appointment=booked_appointment,
            recommendations=recommendations,
            follow_up_instructions=follow_up_instructions,
            ai_analysis=ai_analysis,
            timestamp=datetime.now()
        )
    
    def _map_emergency_to_ambulance_speciality(self, emergency_type: EmergencyType, 
                                              hospital_speciality: str = None) -> str:
        """Map emergency type to ambulance speciality"""
        if emergency_type == EmergencyType.CARDIAC:
            return "cardiac"
        elif emergency_type == EmergencyType.TRAUMA:
            return "trauma"
        elif emergency_type == EmergencyType.MEDICAL and hospital_speciality == "pediatrics":
            return "pediatric"
        else:
            return "general"


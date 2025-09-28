from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class EmergencyType(str, Enum):
    MEDICAL = "medical"
    TRAUMA = "trauma"
    CARDIAC = "cardiac"
    STROKE = "stroke"
    ACCIDENT = "accident"
    OTHER = "other"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Location(BaseModel):
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    address: Optional[str] = Field(None, description="Human-readable address")

class EmergencyRequest(BaseModel):
    emergency_type: EmergencyType = Field(..., description="Type of emergency")
    description: str = Field(..., description="Description of the emergency")
    location: Location = Field(..., description="Location of the emergency")
    patient_name: Optional[str] = Field(None, description="Name of the patient")
    patient_age: Optional[int] = Field(None, description="Age of the patient")
    contact_number: Optional[str] = Field(None, description="Contact number")
    priority: Priority = Field(Priority.MEDIUM, description="Priority level")
    additional_info: Optional[str] = Field(None, description="Additional information")

class Hospital(BaseModel):
    id: str
    name: str
    address: str
    telephone_numbers: List[str]
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    speciality: Optional[str] = None
    beds: Optional[int] = None
    emergency_services: bool = True
    distance_km: Optional[float] = None

class Appointment(BaseModel):
    appointment_id: str
    hospital_id: str
    hospital_name: str
    patient_name: str
    appointment_time: datetime
    doctor_name: Optional[str] = None
    speciality: Optional[str] = None
    status: str = "scheduled"

class Ambulance(BaseModel):
    ambulance_id: str
    driver_name: str
    contact_number: str
    location: Location
    status: str = "available"  # available, dispatched, on_route, arrived
    eta_minutes: Optional[int] = None
    speciality: Optional[str] = None

class EmergencyResponse(BaseModel):
    request_id: str
    emergency_type: EmergencyType
    priority: Priority
    actions_taken: List[str] = Field(default_factory=list)
    nearby_hospitals: List[Hospital] = Field(default_factory=list)
    dispatched_ambulance: Optional[Ambulance] = None
    booked_appointment: Optional[Appointment] = None
    recommendations: List[str] = Field(default_factory=list)
    follow_up_instructions: List[str] = Field(default_factory=list)
    ai_analysis: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


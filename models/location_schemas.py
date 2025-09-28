from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class LocationSource(str, Enum):
    GPS = "gps"
    MANUAL = "manual"
    DENIED = "denied"

class RequestType(str, Enum):
    EMERGENCY = "emergency"
    INFORMATION = "information"
    APPOINTMENT = "appointment"
    OTHER = "other"

class LocationRequest(BaseModel):
    latitude: Optional[float] = Field(None, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, description="Longitude coordinate")
    address: Optional[str] = Field(None, description="Manual address input")
    source: LocationSource = Field(..., description="How location was obtained")
    accuracy: Optional[float] = Field(None, description="GPS accuracy in meters")
    timestamp: datetime = Field(default_factory=datetime.now)

class LocationPermission(BaseModel):
    granted: bool = Field(..., description="Whether location permission was granted")
    denied_reason: Optional[str] = Field(None, description="Reason for denial")
    requested_at: datetime = Field(default_factory=datetime.now)

class PhoneVerification(BaseModel):
    phone_number: str = Field(..., description="Phone number for verification")
    country_code: str = Field("+92", description="Country code")
    verified: bool = Field(False, description="Whether phone is verified")
    verification_method: Optional[str] = Field(None, description="How phone was verified")

class UserSession(BaseModel):
    session_id: str = Field(..., description="Unique session ID")
    location_permission: LocationPermission = Field(..., description="Location permission status")
    location: Optional[LocationRequest] = Field(None, description="User location data")
    phone_verification: Optional[PhoneVerification] = Field(None, description="Phone verification data")
    request_type: Optional[RequestType] = Field(None, description="Type of user request")
    emergency_detected: bool = Field(False, description="Whether emergency was detected")
    created_at: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)

class LocationValidationResult(BaseModel):
    is_valid: bool = Field(..., description="Whether location is valid")
    is_complete: bool = Field(..., description="Whether location data is complete")
    missing_fields: List[str] = Field(default_factory=list, description="Missing required fields")
    error_message: Optional[str] = Field(None, description="Error message if invalid")
    suggestions: List[str] = Field(default_factory=list, description="Suggestions for improvement")

class EmergencyRequirements(BaseModel):
    location_required: bool = Field(True, description="Location is required for emergency")
    phone_required: bool = Field(True, description="Phone is required for emergency")
    location_provided: bool = Field(False, description="Whether location is provided")
    phone_provided: bool = Field(False, description="Whether phone is provided")
    can_proceed: bool = Field(False, description="Whether emergency can proceed")
    missing_requirements: List[str] = Field(default_factory=list, description="Missing requirements")

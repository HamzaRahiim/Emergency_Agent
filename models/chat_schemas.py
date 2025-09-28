from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class MessageType(str, Enum):
    USER = "user"
    SYSTEM = "system"
    CONFIRMATION = "confirmation"
    RESPONSE = "response"

class ChatMessage(BaseModel):
    id: str = Field(..., description="Unique message ID")
    type: MessageType = Field(..., description="Type of message")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional message metadata")

class ChatRequest(BaseModel):
    message: str = Field(..., description="User's chat message")
    user_location: Optional[Dict[str, Any]] = Field(None, description="User's location if available")
    session_id: Optional[str] = Field(None, description="Chat session ID")
    previous_context: Optional[List[ChatMessage]] = Field(None, description="Previous chat context")

class ChatResponse(BaseModel):
    message_id: str = Field(..., description="Response message ID")
    type: MessageType = Field(..., description="Response type")
    content: str = Field(..., description="Response content")
    needs_confirmation: bool = Field(False, description="Whether confirmation is needed")
    parsed_emergency: Optional[Dict[str, Any]] = Field(None, description="Parsed emergency data")
    actions_taken: Optional[List[str]] = Field(None, description="Actions taken by the system")
    timestamp: datetime = Field(default_factory=datetime.now)

class ConfirmationRequest(BaseModel):
    message_id: str = Field(..., description="Message ID to confirm")
    confirmed: bool = Field(..., description="Whether user confirmed")
    additional_info: Optional[str] = Field(None, description="Additional information provided")

class EmergencyChatSession(BaseModel):
    session_id: str = Field(..., description="Unique session ID")
    user_messages: List[ChatMessage] = Field(default_factory=list)
    system_responses: List[ChatMessage] = Field(default_factory=list)
    current_emergency: Optional[Dict[str, Any]] = Field(None, description="Current emergency being processed")
    status: str = Field("active", description="Session status")
    created_at: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)


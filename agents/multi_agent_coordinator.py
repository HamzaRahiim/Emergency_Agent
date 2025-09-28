import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from models.chat_schemas import ChatMessage, MessageType, ChatResponse
from agents.gemini_client import GeminiClient
from agents.location_manager import LocationManager
from agents.ip_location_service import IPLocationService
from agents.ai_chat_coordinator import AIChatCoordinator
from agents.fire_emergency_coordinator import FireEmergencyCoordinator
from agents.police_emergency_coordinator import PoliceEmergencyCoordinator

class MultiAgentCoordinator:
    def __init__(self):
        """Initialize Master Multi-Agent Coordinator"""
        self.gemini_client = GeminiClient()
        self.location_manager = LocationManager()
        self.ip_location_service = IPLocationService()
        
        # Initialize all sub-agents
        self.medical_agent = AIChatCoordinator()
        self.fire_agent = FireEmergencyCoordinator()
        self.police_agent = PoliceEmergencyCoordinator()
        
        # Chat memory for the master agent
        self.chat_memory = {}
    
    async def process_emergency_request(self, message: str, user_ip: str = None, 
                                      session_id: Optional[str] = None) -> ChatResponse:
        """
        Master method to process any emergency request
        """
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Get or create session
        session = self.location_manager.get_session(session_id)
        if not session:
            session = self.location_manager.create_session()
            session_id = session.session_id
        
        # Add current message to master agent history
        self._add_to_chat_history(session_id, "user", message)
        
        # Step 1: Analyze the query to determine emergency type and target agent
        chat_history = self._get_chat_history(session_id)
        emergency_analysis = await self._analyze_emergency_query(message, chat_history)
        
        # Step 2: Route to appropriate sub-agent with chat history
        chat_history = self._get_chat_history(session_id)
        sub_agent_response = await self._route_to_sub_agent(
            emergency_analysis, message, user_ip, session_id, chat_history
        )
        
        # Step 3: Process and format the response
        final_response = await self._process_sub_agent_response(
            sub_agent_response, emergency_analysis, message
        )
        
        # Step 4: Add response to master agent history
        self._add_to_chat_history(session_id, "assistant", final_response.content)
        
        return final_response
    
    async def _analyze_emergency_query(self, message: str, chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Analyze user query to determine emergency type and target agent(s)
        Now supports multi-service emergencies requiring multiple agents
        """
        try:
            # Prepare chat history context
            history_context = ""
            if chat_history and len(chat_history) > 1:
                history_context = "\n\n📝 **CONVERSATION HISTORY** (for context):\n"
                for msg in chat_history[:-1]:  # Exclude current message
                    role = "👤 User" if msg['role'] == 'user' else "🤖 Agent"
                    content = msg['content'][:150] + "..." if len(msg['content']) > 150 else msg['content']
                    history_context += f"{role}: {content}\n"
                history_context += "\n💡 **Use this history to understand the conversation flow and provide context-aware routing.**\n"
            
            # Prepare analysis prompt
            prompt = f"""
            You are an intelligent Emergency Query Analyzer for Karachi, Pakistan.
            Analyze the user's emergency message and determine:
            1. Emergency type(s) - can be multiple for complex emergencies
            2. Urgency level (critical, high, medium, low)
            3. Target agent(s) - can be multiple agents for multi-service emergencies
            4. Key emergency keywords
            5. Confidence level (0-100)
            
            Emergency Categories:
            - MEDICAL: Health issues, injuries, medical emergencies, ambulance needed, hospital, doctor, medical help, people injured, casualties
            - FIRE: Fire, burning, smoke, fire brigade, rescue, building collapse, gas leak, chemical spill, utility emergency, warehouse fire
            - POLICE: Crime, robbery, theft, violence, traffic accident, domestic violence, cyber crime, police needed, law enforcement, security
            - GENERAL: Non-emergency queries, information requests, general help
            
            MULTI-SERVICE EMERGENCY EXAMPLES:
            - Fire with injuries: Requires both FIRE and MEDICAL agents
            - Traffic accident with injuries: Requires both POLICE and MEDICAL agents  
            - Building collapse with casualties: Requires FIRE, MEDICAL, and POLICE agents
            - Crime with injuries: Requires both POLICE and MEDICAL agents
            - Gas leak with people affected: Requires FIRE and MEDICAL agents
            
            {history_context}
            
            Current message to analyze: "{message}"
            
            Respond ONLY with a JSON object in this exact format:
            {{
                "emergency_types": ["medical", "fire", "police", "general"],
                "urgency_level": "critical|high|medium|low", 
                "target_agents": ["medical_agent", "fire_agent", "police_agent"],
                "is_multi_service": true|false,
                "confidence": 85,
                "keywords": ["keyword1", "keyword2", "keyword3"],
                "reasoning": "Brief explanation of classification and why multiple agents needed"
            }}
            """
            
            response = self.gemini_client.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Try to parse JSON response
            try:
                analysis = json.loads(response_text)
                return analysis
            except json.JSONDecodeError:
                # Fallback to keyword-based analysis
                return self._fallback_emergency_analysis(message)
                
        except Exception as e:
            print(f"Error in emergency analysis: {e}")
            # Fallback to keyword-based analysis
            return self._fallback_emergency_analysis(message)
    
    def _fallback_emergency_analysis(self, message: str) -> Dict[str, Any]:
        """
        Fallback emergency analysis using keyword matching with multi-service support
        """
        message_lower = message.lower()
        
        # Medical emergency keywords
        medical_keywords = [
            'hospital', 'doctor', 'ambulance', 'medical', 'health', 'sick', 'injured', 'wound',
            'bleeding', 'pain', 'heart', 'chest', 'breathing', 'unconscious', 'emergency medical',
            'medicine', 'treatment', 'clinic', 'nurse', 'patient', 'illness', 'disease', 'casualties',
            'people injured', 'victims', 'hurt', 'wounded'
        ]
        
        # Fire emergency keywords
        fire_keywords = [
            'fire', 'burning', 'smoke', 'flame', 'blaze', 'fire brigade', 'rescue', 'building collapse',
            'gas leak', 'chemical', 'explosion', 'utility', 'power outage', 'water leak', 'emergency services',
            'warehouse fire', 'industrial fire', 'structural fire'
        ]
        
        # Police emergency keywords
        police_keywords = [
            'police', 'crime', 'robbery', 'theft', 'burglary', 'mugging', 'violence', 'fight', 'attack',
            'traffic accident', 'car crash', 'hit and run', 'domestic violence', 'harassment', 'threat',
            'cyber crime', 'fraud', 'scam', 'kidnapping', 'missing', 'stolen', 'criminal', 'law enforcement',
            'security', 'investigation'
        ]
        
        # Count keyword matches
        medical_score = sum(1 for keyword in medical_keywords if keyword in message_lower)
        fire_score = sum(1 for keyword in fire_keywords if keyword in message_lower)
        police_score = sum(1 for keyword in police_keywords if keyword in message_lower)
        
        # Multi-service detection
        emergency_types = []
        target_agents = []
        is_multi_service = False
        
        # Determine which services are needed
        if medical_score > 0:
            emergency_types.append("medical")
            target_agents.append("medical_agent")
        if fire_score > 0:
            emergency_types.append("fire")
            target_agents.append("fire_agent")
        if police_score > 0:
            emergency_types.append("police")
            target_agents.append("police_agent")
        
        # Check for multi-service scenarios
        if len(emergency_types) > 1:
            is_multi_service = True
            confidence = min(95, (medical_score + fire_score + police_score) * 10)
        elif len(emergency_types) == 1:
            confidence = min(90, (medical_score + fire_score + police_score) * 15)
        else:
            emergency_types = ["general"]
            target_agents = ["medical_agent"]
            confidence = 50
        
        # Determine urgency
        urgent_keywords = ['emergency', 'urgent', 'help', 'immediately', 'critical', 'serious', 'injured', 'casualties']
        urgency_level = "critical" if any(keyword in message_lower for keyword in urgent_keywords) else "medium"
        
        reasoning = f"Classified as {', '.join(emergency_types)} based on keyword analysis"
        if is_multi_service:
            reasoning += f" - Multi-service emergency requiring {', '.join(target_agents)}"
        
        return {
            "emergency_types": emergency_types,
            "urgency_level": urgency_level,
            "target_agents": target_agents,
            "is_multi_service": is_multi_service,
            "confidence": confidence,
            "keywords": [word for word in message_lower.split() if len(word) > 3],
            "reasoning": reasoning
        }
    
    async def _route_to_sub_agent(self, analysis: Dict[str, Any], message: str, 
                                user_ip: str, session_id: str, chat_history: List[Dict[str, str]]) -> ChatResponse:
        """
        Route the request to the appropriate sub-agent(s) with chat history
        Now supports multi-service emergencies requiring multiple agents
        """
        # Handle both old and new analysis formats
        target_agents = analysis.get("target_agents", [])
        if not target_agents:
            # Fallback for old format
            target_agent = analysis.get("target_agent", "medical_agent")
            target_agents = [target_agent]
        
        is_multi_service = analysis.get("is_multi_service", False)
        
        try:
            # Add chat history to each sub-agent's memory before processing
            self._sync_chat_history_to_sub_agents(session_id, chat_history)
            
            if is_multi_service and len(target_agents) > 1:
                # Multi-service emergency - coordinate multiple agents
                return await self._handle_multi_service_emergency(
                    target_agents, message, user_ip, session_id, analysis
                )
            else:
                # Single service emergency - route to primary agent
                primary_agent = target_agents[0] if target_agents else "medical_agent"
                return await self._route_to_single_agent(primary_agent, message, user_ip, session_id)
                
        except Exception as e:
            # Return error response if sub-agent fails
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.SYSTEM,
                content=f"[ERROR] **Emergency Service Error**: {str(e)}\n\nPlease try again or contact emergency services directly.",
                needs_confirmation=False,
                timestamp=datetime.now()
            )
    
    async def _process_sub_agent_response(self, sub_response: ChatResponse, 
                                        analysis: Dict[str, Any], original_message: str) -> ChatResponse:
        """
        Process and enhance the sub-agent response
        """
        try:
            # Return the original sub-agent response without modification
            # No routing notes or confidence warnings
            enhanced_response = ChatResponse(
                message_id=str(uuid.uuid4()),
                type=sub_response.type,
                content=sub_response.content,
                needs_confirmation=sub_response.needs_confirmation,
                timestamp=datetime.now()
            )
            
            return enhanced_response
            
        except Exception as e:
            # Return original response if enhancement fails
            return sub_response
    
    async def _handle_multi_service_emergency(self, target_agents: List[str], message: str, 
                                            user_ip: str, session_id: str, analysis: Dict[str, Any]) -> ChatResponse:
        """
        Handle multi-service emergency by coordinating multiple agents
        """
        try:
            agent_responses = []
            
            # Process each required agent
            for agent_name in target_agents:
                agent_response = await self._route_to_single_agent(agent_name, message, user_ip, session_id)
                agent_responses.append({
                    "agent": agent_name,
                    "response": agent_response
                })
            
            # Combine responses into a coordinated response
            return self._combine_multi_agent_responses(agent_responses, analysis)
            
        except Exception as e:
            # Fallback to single agent if multi-agent coordination fails
            primary_agent = target_agents[0] if target_agents else "medical_agent"
            return await self._route_to_single_agent(primary_agent, message, user_ip, session_id)
    
    async def _route_to_single_agent(self, agent_name: str, message: str, user_ip: str, session_id: str) -> ChatResponse:
        """
        Route to a single specific agent
        """
        if agent_name == "medical_agent":
            return await self.medical_agent.process_user_message(message, user_ip, session_id)
        elif agent_name == "fire_agent":
            return await self.fire_agent.process_fire_emergency_request(message, user_ip, session_id)
        elif agent_name == "police_agent":
            return await self.police_agent.process_police_emergency_request(message, user_ip, session_id)
        else:
            # Default to medical agent
            return await self.medical_agent.process_user_message(message, user_ip, session_id)
    
    def _combine_multi_agent_responses(self, agent_responses: List[Dict], analysis: Dict[str, Any]) -> ChatResponse:
        """
        Combine multiple agent responses into a coordinated response
        """
        try:
            emergency_types = analysis.get("emergency_types", [])
            urgency_level = analysis.get("urgency_level", "medium")
            
            # Create coordinated response
            coordinated_content = f"🚨 **MULTI-SERVICE EMERGENCY RESPONSE** 🚨\n\n"
            coordinated_content += f"**Emergency Type**: {', '.join(emergency_types).title()}\n"
            coordinated_content += f"**Urgency Level**: {urgency_level.upper()}\n\n"
            
            # Add each agent's response
            for i, agent_data in enumerate(agent_responses, 1):
                agent_name = agent_data["agent"]
                response = agent_data["response"]
                
                # Format agent name for display
                if agent_name == "medical_agent":
                    agent_display = "🏥 MEDICAL SERVICES"
                elif agent_name == "fire_agent":
                    agent_display = "🚨 FIRE & EMERGENCY SERVICES"
                elif agent_name == "police_agent":
                    agent_display = "👮 POLICE SERVICES"
                else:
                    agent_display = agent_name.replace("_", " ").title()
                
                coordinated_content += f"**{agent_display}:**\n"
                coordinated_content += f"{response.content}\n\n"
            
            # Add coordination note
            coordinated_content += "---\n"
            coordinated_content += "[OK] **All emergency services have been coordinated and dispatched.**\n"
            coordinated_content += "📞 **Stay on the line for updates and follow instructions from emergency responders.**"
            
            return ChatResponse(
                message_id=str(uuid.uuid4()),
                type=MessageType.SYSTEM,
                content=coordinated_content,
                needs_confirmation=True,  # Multi-service emergencies need confirmation
                timestamp=datetime.now()
            )
            
        except Exception as e:
            # Fallback to first agent's response if coordination fails
            if agent_responses:
                return agent_responses[0]["response"]
            else:
                return ChatResponse(
                    message_id=str(uuid.uuid4()),
                    type=MessageType.SYSTEM,
                    content="[ERROR] **Emergency Service Coordination Error**\n\nPlease contact emergency services directly.",
                    needs_confirmation=False,
                    timestamp=datetime.now()
                )
    
    def _sync_chat_history_to_sub_agents(self, session_id: str, chat_history: List[Dict[str, str]]):
        """
        Sync chat history to all sub-agents so they remember previous conversations
        """
        try:
            # Sync to medical agent
            if session_id not in self.medical_agent.chat_memory:
                self.medical_agent.chat_memory[session_id] = []
            
            # Update medical agent's chat history with master agent's history
            self.medical_agent.chat_memory[session_id] = chat_history[-10:]  # Last 10 messages
            
            # Sync to fire agent
            if session_id not in self.fire_agent.chat_memory:
                self.fire_agent.chat_memory[session_id] = []
            
            # Update fire agent's chat history with master agent's history
            self.fire_agent.chat_memory[session_id] = chat_history[-10:]  # Last 10 messages
            
            # Sync to police agent
            if session_id not in self.police_agent.chat_memory:
                self.police_agent.chat_memory[session_id] = []
            
            # Update police agent's chat history with master agent's history
            self.police_agent.chat_memory[session_id] = chat_history[-10:]  # Last 10 messages
            
        except Exception as e:
            print(f"Warning: Could not sync chat history to sub-agents: {e}")
    
    def _add_to_chat_history(self, session_id: str, role: str, content: str):
        """Add message to master agent chat history"""
        if session_id not in self.chat_memory:
            self.chat_memory[session_id] = []
        
        self.chat_memory[session_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 30 messages
        if len(self.chat_memory[session_id]) > 30:
            self.chat_memory[session_id] = self.chat_memory[session_id][-30:]
    
    def _get_chat_history(self, session_id: str) -> List[Dict[str, str]]:
        """Get chat history for a session"""
        if session_id not in self.chat_memory:
            self.chat_memory[session_id] = []
        return self.chat_memory[session_id][-15:]  # Last 15 messages
    
    def get_session_chat_history(self, session_id: str) -> Dict[str, Any]:
        """Get detailed chat history for a session"""
        session_info = {
            "session_id": session_id,
            "total_messages": 0,
            "chat_history": [],
            "has_location": False,
            "has_phone": False,
            "agent_type": "multi_agent_coordinator"
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
    
    async def get_emergency_services_summary(self) -> Dict[str, Any]:
        """Get summary of all available emergency services including multi-service capabilities"""
        try:
            return {
                "medical_services": {
                    "hospitals_loaded": len(self.medical_agent.hospital_finder.hospitals),
                    "ambulances_loaded": len(getattr(self.medical_agent, 'ambulances', [])),
                    "services": ["Emergency Medical Response", "Ambulance Dispatch", "Hospital Information", "Medical Guidance"]
                },
                "fire_services": {
                    "stations_loaded": len(self.fire_agent.emergency_stations),
                    "services": ["Fire Rescue", "Building Collapse", "Gas Leak Response", "Utility Emergencies", "Rescue Operations"]
                },
                "police_services": {
                    "stations_loaded": len(self.police_agent.police_stations),
                    "services": ["Crime Response", "Traffic Control", "Domestic Violence", "Cyber Crime", "Law Enforcement"]
                },
                "multi_service_emergencies": {
                    "enabled": True,
                    "description": "Automatically detects and coordinates multiple services for complex emergencies",
                    "examples": [
                        "Fire with injuries → Fire + Medical services",
                        "Traffic accident with casualties → Police + Medical services",
                        "Building collapse → Fire + Medical + Police services",
                        "Crime with injuries → Police + Medical services",
                        "Gas leak with people affected → Fire + Medical services"
                    ],
                    "coordination": "Real-time multi-agent coordination with unified response"
                },
                "features": {
                    "multi_agent_coordination": True,
                    "chat_memory": True,
                    "location_services": True,
                    "phone_verification": True,
                    "context_aware_routing": True,
                    "emergency_type_detection": True,
                    "multi_service_detection": True
                },
                "total_agents": 3,
                "status": "All systems operational with multi-service coordination"
            }
        except Exception as e:
            return {"error": str(e), "status": "System error"}

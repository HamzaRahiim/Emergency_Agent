import google.generativeai as genai
import os
from typing import Dict, Any, List
import json
from dotenv import load_dotenv

class GeminiClient:
    def __init__(self):
        """Initialize Gemini client with API key"""
        # Load environment variables from .env file
        load_dotenv()
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            raise ValueError("GEMINI_API_KEY environment variable is required. Please set your Google Gemini API key in the .env file.")
        
        genai.configure(api_key=api_key)
        
        # Use the current available models (based on your API access)
        model_names = [
            'gemini-2.0-flash',           # Latest and fastest
            'gemini-2.5-flash',           # Alternative fast model
            'gemini-flash-latest',        # Latest flash model
            'gemini-2.0-flash-001',       # Stable version
            'gemini-pro-latest'           # Latest pro model
        ]
        
        self.model = None
        for model_name in model_names:
            try:
                self.model = genai.GenerativeModel(model_name)
                # Test the model with a simple request
                test_response = self.model.generate_content("test")
                print(f"✅ Using model: {model_name}")
                break
            except Exception as e:
                print(f"❌ Model {model_name} failed: {str(e)[:100]}...")
                continue
        
        if not self.model:
            raise ValueError("No working Gemini models found. Please check your API key permissions.")
    
    async def analyze_emergency(self, emergency_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze emergency situation and provide AI insights
        Optimized for cost - single comprehensive call
        """
        prompt = f"""
        You are an expert emergency medical coordinator for Karachi, Pakistan. 
        Analyze this emergency situation and provide comprehensive guidance:

        Emergency Details:
        - Type: {emergency_data.get('emergency_type')}
        - Description: {emergency_data.get('description')}
        - Location: {emergency_data.get('location', {}).get('address', 'Not specified')}
        - Patient Age: {emergency_data.get('patient_age', 'Not specified')}
        - Priority: {emergency_data.get('priority')}

        Please provide:
        1. Immediate first aid recommendations
        2. Whether ambulance dispatch is needed
        3. Hospital type recommendations (general, cardiac, trauma, etc.)
        4. Urgency assessment
        5. Follow-up care instructions

        Respond in JSON format:
        {{
            "first_aid": ["instruction1", "instruction2"],
            "ambulance_needed": true/false,
            "hospital_speciality": "recommended_speciality",
            "urgency_level": "low/medium/high/critical",
            "follow_up": ["instruction1", "instruction2"],
            "ai_reasoning": "brief explanation of recommendations"
        }}
        """

        try:
            response = self.model.generate_content(prompt)
            # Parse JSON response
            response_text = response.text.strip()
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            return json.loads(response_text)
        except Exception as e:
            raise Exception(f"Error with Gemini API: {e}")
    
    
    async def generate_response_message(self, response_data: Dict[str, Any]) -> str:
        """
        Generate a human-readable response message
        """
        prompt = f"""
        Generate a compassionate, professional emergency response message for a patient in Karachi.
        
        Response Data: {json.dumps(response_data, indent=2)}
        
        The message should:
        - Be reassuring and professional
        - Include clear next steps
        - Be appropriate for the emergency type
        - Include relevant contact information
        - Be concise but comprehensive
        
        Write as if speaking directly to the patient or their family.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error with Gemini API: {e}")
    
    async def chat_with_user(self, message: str, context: Dict[str, Any] = None, 
                           hospitals: List[Dict] = None, chat_history: List[Dict[str, str]] = None) -> str:
        """
        Direct chat with user using Gemini AI - User-friendly conversation
        """
        try:
            # Prepare hospital context with detailed information
            hospital_context = ""
            if hospitals:
                hospital_context = "\n\n🏥 **KARACHI EMERGENCY HOSPITALS** (Use these for emergency responses):\n"
                for i, hospital in enumerate(hospitals[:5], 1):
                    hospital_context += f"**{i}. {hospital.get('name', 'Unknown')}**\n"
                    hospital_context += f"📍 {hospital.get('address', 'Unknown')}\n"
                    if hospital.get('telephone_numbers'):
                        hospital_context += f"📞 {hospital['telephone_numbers'][0]}\n"
                    if hospital.get('specialities'):
                        hospital_context += f"🏥 Specialties: {', '.join(hospital['specialities'][:3])}\n"
                    if hospital.get('distance_km'):
                        hospital_context += f"📏 {hospital['distance_km']:.1f} km away\n"
                    hospital_context += "\n"
            
            # Prepare context information
            context_info = ""
            if context:
                if context.get('location'):
                    context_info += f"User Location: {context['location']}\n"
                if context.get('emergency_detected'):
                    context_info += f"Emergency Status: {context['emergency_detected']}\n"
                if context.get('phone_verified'):
                    context_info += f"Phone Verified: {context['phone_verified']}\n"
            
            # Prepare chat history context
            history_context = ""
            if chat_history and len(chat_history) > 1:  # More than just current message
                history_context = "\n\n📝 **CONVERSATION HISTORY** (for context):\n"
                for msg in chat_history[:-1]:  # Exclude current message
                    role = "👤 User" if msg['role'] == 'user' else "🤖 Assistant"
                    # Truncate very long messages to keep context clean
                    content = msg['content'][:200] + "..." if len(msg['content']) > 200 else msg['content']
                    history_context += f"{role}: {content}\n"
                history_context += "\n💡 **Use this history to understand the conversation flow and provide relevant responses.**\n"
            
            prompt = f"""
            You are a professional, friendly, and empathetic Emergency Medical Assistant for Karachi, Pakistan. 
            You help people with medical emergencies, hospital information, and medical guidance.
            
            IMPORTANT GUIDELINES:
            1. **KEEP RESPONSES SHORT AND DIRECT** - Maximum 2-3 sentences
            2. For emergencies: Be serious, direct, and action-oriented
            3. Use emojis sparingly (only for emergencies: 🚑, ⚠️, 🏥)
            4. Speak in simple, clear language
            5. **EMERGENCY PROTOCOL**: If emergency detected:
               - Immediately provide relevant hospital names from the list below
               - Mention ambulance dispatch with ETA
               - Give direct, urgent instructions
            6. For general queries: Be helpful but brief
            7. Reference conversation history when relevant
            8. **RESPONSE LENGTH**: Keep under 100 words unless it's a complex emergency
            
            Current Context:
            {context_info}
            
            {hospital_context}
            
            {history_context}
            
            **RESPONSE RULES**:
            - **EMERGENCY**: Be serious, direct. Provide hospital names, ambulance ETA (10-15 mins), urgent instructions
            - **GENERAL**: Keep responses under 50 words, be helpful but brief
            - **HOSPITALS**: Always use the hospital list above for emergency responses
            - **AMBULANCE**: Mention "Ambulance dispatched, ETA 10-15 minutes" for emergencies
            - **TONE**: Professional for emergencies, friendly for general queries
            
            User Message: "{message}"
            
            Respond directly and concisely. For emergencies, prioritize immediate action and hospital information.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
                
        except Exception as e:
            raise Exception(f"Error with Gemini API: {e}")
    
    async def chat_with_police_emergency(self, message: str, context: Dict[str, Any] = None, 
                                       stations: List[Dict] = None, chat_history: List[Dict[str, str]] = None,
                                       emergency_type: str = None) -> str:
        """
        Chat with user for police/emergency services - Specialized for law enforcement
        """
        try:
            # Prepare police stations context
            stations_context = ""
            if stations:
                stations_context = "\n\n👮 **KARACHI POLICE SERVICES** (Use these for emergency responses):\n"
                for i, station in enumerate(stations[:5], 1):
                    stations_context += f"**{i}. {station.get('name', 'Unknown')}**\n"
                    stations_context += f"📍 {station.get('address', 'Unknown')}\n"
                    stations_context += f"👮 Type: {station.get('type', 'Unknown').replace('_', ' ').title()}\n"
                    if station.get('emergency_number'):
                        stations_context += f"📞 Emergency: {station['emergency_number']}\n"
                    if station.get('contact_numbers'):
                        stations_context += f"📞 Contact: {station['contact_numbers'][0]}\n"
                    if station.get('services'):
                        stations_context += f"🛠️ Services: {', '.join(station['services'][:3])}\n"
                    if station.get('response_time_minutes'):
                        stations_context += f"⏱️ ETA: {station['response_time_minutes']} minutes\n"
                    if station.get('distance_km'):
                        stations_context += f"📏 {station['distance_km']:.1f} km away\n"
                    stations_context += "\n"
            
            # Prepare context information
            context_info = ""
            if context:
                if context.get('location'):
                    context_info += f"User Location: {context['location']}\n"
                if context.get('emergency_detected'):
                    context_info += f"Emergency Status: {context['emergency_detected']}\n"
                if context.get('phone_verified'):
                    context_info += f"Phone Verified: {context['phone_verified']}\n"
            
            # Prepare chat history context
            history_context = ""
            if chat_history and len(chat_history) > 1:  # More than just current message
                history_context = "\n\n📝 **CONVERSATION HISTORY** (for context):\n"
                for msg in chat_history[:-1]:  # Exclude current message
                    role = "👤 User" if msg['role'] == 'user' else "👮 Police Coordinator"
                    # Truncate very long messages to keep context clean
                    content = msg['content'][:200] + "..." if len(msg['content']) > 200 else msg['content']
                    history_context += f"{role}: {content}\n"
                history_context += "\n💡 **Use this history to understand the conversation flow and provide relevant responses.**\n"
            
            prompt = f"""
            You are a professional, authoritative, and efficient Police Emergency Coordinator for Karachi, Pakistan. 
            You handle crime emergencies, traffic incidents, domestic violence, cyber crimes, and law enforcement situations.
            
            IMPORTANT GUIDELINES:
            1. **KEEP RESPONSES SHORT AND DIRECT** - Maximum 2-3 sentences
            2. For emergencies: Be serious, authoritative, and action-oriented
            3. Use emojis sparingly (only for emergencies: 👮, 🚨, ⚠️, 🔒)
            4. Speak in clear, professional language
            5. **EMERGENCY PROTOCOL**: If emergency detected:
               - Immediately provide relevant police station names from the list below
               - Mention police dispatch with ETA
               - Give direct, urgent instructions
            6. For general queries: Be helpful but brief
            7. Reference conversation history when relevant
            8. **RESPONSE LENGTH**: Keep under 100 words unless it's a complex emergency
            
            Current Context:
            {context_info}
            
            {stations_context}
            
            {history_context}
            
            **RESPONSE RULES**:
            - **EMERGENCY**: Be serious, direct. Provide station names, police dispatch ETA, urgent instructions
            - **GENERAL**: Keep responses under 50 words, be helpful but brief
            - **STATIONS**: Always use the police station list above for emergency responses
            - **DISPATCH**: Mention "Police dispatched, ETA X minutes" for emergencies
            - **TONE**: Professional and authoritative for emergencies, helpful for general queries
            
            User Message: "{message}"
            
            Respond directly and concisely. For emergencies, prioritize immediate action and police station information.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
                
        except Exception as e:
            raise Exception(f"Error with Gemini API: {e}")
    
    async def chat_with_fire_emergency(self, message: str, context: Dict[str, Any] = None, 
                                     stations: List[Dict] = None, chat_history: List[Dict[str, str]] = None,
                                     emergency_type: str = None) -> str:
        """
        Chat with user for fire/emergency services - Specialized for emergency services
        """
        try:
            # Prepare emergency stations context
            stations_context = ""
            if stations:
                stations_context = "\n\n🚨 **KARACHI EMERGENCY SERVICES** (Use these for emergency responses):\n"
                for i, station in enumerate(stations[:5], 1):
                    stations_context += f"**{i}. {station.get('name', 'Unknown')}**\n"
                    stations_context += f"📍 {station.get('address', 'Unknown')}\n"
                    stations_context += f"🚨 Type: {station.get('type', 'Unknown').replace('_', ' ').title()}\n"
                    if station.get('emergency_number'):
                        stations_context += f"📞 Emergency: {station['emergency_number']}\n"
                    if station.get('contact_numbers'):
                        stations_context += f"📞 Contact: {station['contact_numbers'][0]}\n"
                    if station.get('services'):
                        stations_context += f"🛠️ Services: {', '.join(station['services'][:3])}\n"
                    if station.get('response_time_minutes'):
                        stations_context += f"⏱️ ETA: {station['response_time_minutes']} minutes\n"
                    if station.get('distance_km'):
                        stations_context += f"📏 {station['distance_km']:.1f} km away\n"
                    stations_context += "\n"
            
            # Prepare context information
            context_info = ""
            if context:
                if context.get('location'):
                    context_info += f"User Location: {context['location']}\n"
                if context.get('emergency_detected'):
                    context_info += f"Emergency Status: {context['emergency_detected']}\n"
                if context.get('phone_verified'):
                    context_info += f"Phone Verified: {context['phone_verified']}\n"
            
            # Prepare chat history context
            history_context = ""
            if chat_history and len(chat_history) > 1:  # More than just current message
                history_context = "\n\n📝 **CONVERSATION HISTORY** (for context):\n"
                for msg in chat_history[:-1]:  # Exclude current message
                    role = "👤 User" if msg['role'] == 'user' else "🚨 Emergency Assistant"
                    # Truncate very long messages to keep context clean
                    content = msg['content'][:200] + "..." if len(msg['content']) > 200 else msg['content']
                    history_context += f"{role}: {content}\n"
                history_context += "\n💡 **Use this history to understand the conversation flow and provide relevant responses.**\n"
            
            prompt = f"""
            You are a professional, serious, and efficient Emergency Services Coordinator for Karachi, Pakistan. 
            You handle fire emergencies, police situations, rescue operations, and utility emergencies.
            
            IMPORTANT GUIDELINES:
            1. **KEEP RESPONSES SHORT AND DIRECT** - Maximum 2-3 sentences
            2. For emergencies: Be serious, direct, and action-oriented
            3. Use emojis sparingly (only for emergencies: 🚨, 🔥, 👮, 🚑)
            4. Speak in simple, clear language
            5. **EMERGENCY PROTOCOL**: If emergency detected:
               - Immediately provide relevant station names from the list below
               - Mention emergency dispatch with ETA
               - Give direct, urgent instructions
            6. For general queries: Be helpful but brief
            7. Reference conversation history when relevant
            8. **RESPONSE LENGTH**: Keep under 100 words unless it's a complex emergency
            
            Current Context:
            {context_info}
            
            {stations_context}
            
            {history_context}
            
            **RESPONSE RULES**:
            - **EMERGENCY**: Be serious, direct. Provide station names, dispatch ETA, urgent instructions
            - **GENERAL**: Keep responses under 50 words, be helpful but brief
            - **STATIONS**: Always use the station list above for emergency responses
            - **DISPATCH**: Mention "Emergency dispatched, ETA X minutes" for emergencies
            - **TONE**: Professional and urgent for emergencies, helpful for general queries
            
            User Message: "{message}"
            
            Respond directly and concisely. For emergencies, prioritize immediate action and station information.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
                
        except Exception as e:
            raise Exception(f"Error with Gemini API: {e}")
    
    async def chat_with_police_emergency(self, message: str, context: Dict[str, Any] = None, 
                                       stations: List[Dict] = None, chat_history: List[Dict[str, str]] = None,
                                       emergency_type: str = None) -> str:
        """
        Chat with user for police/emergency services - Specialized for law enforcement
        """
        try:
            # Prepare police stations context
            stations_context = ""
            if stations:
                stations_context = "\n\n👮 **KARACHI POLICE SERVICES** (Use these for emergency responses):\n"
                for i, station in enumerate(stations[:5], 1):
                    stations_context += f"**{i}. {station.get('name', 'Unknown')}**\n"
                    stations_context += f"📍 {station.get('address', 'Unknown')}\n"
                    stations_context += f"👮 Type: {station.get('type', 'Unknown').replace('_', ' ').title()}\n"
                    if station.get('emergency_number'):
                        stations_context += f"📞 Emergency: {station['emergency_number']}\n"
                    if station.get('contact_numbers'):
                        stations_context += f"📞 Contact: {station['contact_numbers'][0]}\n"
                    if station.get('services'):
                        stations_context += f"🛠️ Services: {', '.join(station['services'][:3])}\n"
                    if station.get('response_time_minutes'):
                        stations_context += f"⏱️ ETA: {station['response_time_minutes']} minutes\n"
                    if station.get('distance_km'):
                        stations_context += f"📏 {station['distance_km']:.1f} km away\n"
                    stations_context += "\n"
            
            # Prepare context information
            context_info = ""
            if context:
                if context.get('location'):
                    context_info += f"User Location: {context['location']}\n"
                if context.get('emergency_detected'):
                    context_info += f"Emergency Status: {context['emergency_detected']}\n"
                if context.get('phone_verified'):
                    context_info += f"Phone Verified: {context['phone_verified']}\n"
            
            # Prepare chat history context
            history_context = ""
            if chat_history and len(chat_history) > 1:  # More than just current message
                history_context = "\n\n📝 **CONVERSATION HISTORY** (for context):\n"
                for msg in chat_history[:-1]:  # Exclude current message
                    role = "👤 User" if msg['role'] == 'user' else "👮 Police Coordinator"
                    # Truncate very long messages to keep context clean
                    content = msg['content'][:200] + "..." if len(msg['content']) > 200 else msg['content']
                    history_context += f"{role}: {content}\n"
                history_context += "\n💡 **Use this history to understand the conversation flow and provide relevant responses.**\n"
            
            prompt = f"""
            You are a professional, authoritative, and efficient Police Emergency Coordinator for Karachi, Pakistan. 
            You handle crime emergencies, traffic incidents, domestic violence, cyber crimes, and law enforcement situations.
            
            IMPORTANT GUIDELINES:
            1. **KEEP RESPONSES SHORT AND DIRECT** - Maximum 2-3 sentences
            2. For emergencies: Be serious, authoritative, and action-oriented
            3. Use emojis sparingly (only for emergencies: 👮, 🚨, ⚠️, 🔒)
            4. Speak in clear, professional language
            5. **EMERGENCY PROTOCOL**: If emergency detected:
               - Immediately provide relevant police station names from the list below
               - Mention police dispatch with ETA
               - Give direct, urgent instructions
            6. For general queries: Be helpful but brief
            7. Reference conversation history when relevant
            8. **RESPONSE LENGTH**: Keep under 100 words unless it's a complex emergency
            
            Current Context:
            {context_info}
            
            {stations_context}
            
            {history_context}
            
            **RESPONSE RULES**:
            - **EMERGENCY**: Be serious, direct. Provide station names, police dispatch ETA, urgent instructions
            - **GENERAL**: Keep responses under 50 words, be helpful but brief
            - **STATIONS**: Always use the police station list above for emergency responses
            - **DISPATCH**: Mention "Police dispatched, ETA X minutes" for emergencies
            - **TONE**: Professional and authoritative for emergencies, helpful for general queries
            
            User Message: "{message}"
            
            Respond directly and concisely. For emergencies, prioritize immediate action and police station information.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
                
        except Exception as e:
            raise Exception(f"Error with Gemini API: {e}")
    

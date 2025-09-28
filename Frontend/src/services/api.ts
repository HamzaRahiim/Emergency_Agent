import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface ChatMessage {
  message_id: string
  type: 'user' | 'assistant' | 'system'
  content: string
  timestamp: string
  needs_confirmation?: boolean
}

export interface ChatResponse {
  message_id: string
  type: string
  content: string
  timestamp: string
  needs_confirmation?: boolean
}

export interface EmergencyServices {
  medical_services: {
    hospitals_loaded: number
    services: string[]
  }
  fire_services: {
    stations_loaded: number
    services: string[]
  }
  police_services: {
    stations_loaded: number
    services: string[]
  }
  multi_service_emergencies: {
    enabled: boolean
    description: string
    examples: string[]
  }
  features: {
    multi_agent_coordination: boolean
    chat_memory: boolean
    location_services: boolean
    phone_verification: boolean
    context_aware_routing: boolean
    emergency_type_detection: boolean
    multi_service_detection: boolean
  }
  total_agents: number
  status: string
}

class EmergencyAgentAPI {
  // Medical Emergency Services
  async sendMedicalMessage(message: string, sessionId?: string): Promise<ChatResponse> {
    const response = await api.post('/ai/chat', {
      message,
      session_id: sessionId
    })
    return response.data
  }

  // Fire Emergency Services
  async sendFireMessage(message: string, sessionId?: string): Promise<ChatResponse> {
    const response = await api.post('/fire/chat', {
      message,
      session_id: sessionId
    })
    return response.data
  }

  // Police Emergency Services
  async sendPoliceMessage(message: string, sessionId?: string): Promise<ChatResponse> {
    const response = await api.post('/police/chat', {
      message,
      session_id: sessionId
    })
    return response.data
  }

  // Multi-Agent Hub
  async sendMultiAgentMessage(message: string, sessionId?: string): Promise<ChatResponse> {
    const response = await api.post('/multi-agent/chat', {
      message,
      session_id: sessionId
    })
    return response.data
  }

  // Get Emergency Services Summary
  async getEmergencyServicesSummary(): Promise<EmergencyServices> {
    const response = await api.get('/multi-agent/services')
    return response.data
  }

  // Get nearby hospitals
  async getNearbyHospitals(lat: number, lon: number, radius: number = 15.0) {
    const response = await api.get('/hospitals/nearby', {
      params: { lat, lon, radius }
    })
    return response.data
  }

  // Get nearby fire stations
  async getNearbyFireStations(lat: number, lon: number, radius: number = 15.0) {
    const response = await api.get('/fire/stations/nearby', {
      params: { lat, lon, radius }
    })
    return response.data
  }

  // Get nearby police stations
  async getNearbyPoliceStations(lat: number, lon: number, radius: number = 15.0) {
    const response = await api.get('/police/stations/nearby', {
      params: { lat, lon, radius }
    })
    return response.data
  }

  // Health check
  async healthCheck() {
    const response = await api.get('/health')
    return response.data
  }

  // Status check
  async statusCheck() {
    const response = await api.get('/status')
    return response.data
  }
}

export const emergencyAPI = new EmergencyAgentAPI()
export default api

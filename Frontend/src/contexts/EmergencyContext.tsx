import React, { createContext, useContext, useReducer, ReactNode } from 'react'
import { ChatMessage } from '../services/api'

interface EmergencyState {
  currentAgent: 'medical' | 'fire' | 'police' | 'multi-agent'
  chatHistory: ChatMessage[]
  isEmergency: boolean
  userLocation: { lat: number; lon: number } | null
  sessionId: string
  isLoading: boolean
  error: string | null
}

type EmergencyAction =
  | { type: 'SET_AGENT'; payload: 'medical' | 'fire' | 'police' | 'multi-agent' }
  | { type: 'ADD_MESSAGE'; payload: ChatMessage }
  | { type: 'SET_EMERGENCY'; payload: boolean }
  | { type: 'SET_LOCATION'; payload: { lat: number; lon: number } | null }
  | { type: 'SET_SESSION_ID'; payload: string }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'CLEAR_CHAT' }

const initialState: EmergencyState = {
  currentAgent: 'multi-agent',
  chatHistory: [],
  isEmergency: false,
  userLocation: null,
  sessionId: generateSessionId(),
  isLoading: false,
  error: null,
}

function generateSessionId(): string {
  return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

function emergencyReducer(state: EmergencyState, action: EmergencyAction): EmergencyState {
  switch (action.type) {
    case 'SET_AGENT':
      return { ...state, currentAgent: action.payload }
    case 'ADD_MESSAGE':
      return { ...state, chatHistory: [...state.chatHistory, action.payload] }
    case 'SET_EMERGENCY':
      return { ...state, isEmergency: action.payload }
    case 'SET_LOCATION':
      return { ...state, userLocation: action.payload }
    case 'SET_SESSION_ID':
      return { ...state, sessionId: action.payload }
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload }
    case 'SET_ERROR':
      return { ...state, error: action.payload }
    case 'CLEAR_CHAT':
      return { ...state, chatHistory: [] }
    default:
      return state
  }
}

interface EmergencyContextType {
  state: EmergencyState
  dispatch: React.Dispatch<EmergencyAction>
  sendMessage: (message: string) => Promise<void>
  getCurrentLocation: () => Promise<void>
  clearChat: () => void
}

const EmergencyContext = createContext<EmergencyContextType | undefined>(undefined)

export function EmergencyProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(emergencyReducer, initialState)

  const sendMessage = async (message: string) => {
    if (!message.trim()) return

    dispatch({ type: 'SET_LOADING', payload: true })
    dispatch({ type: 'SET_ERROR', payload: null })

    // Add user message to chat
    const userMessage: ChatMessage = {
      message_id: `msg_${Date.now()}`,
      type: 'user',
      content: message,
      timestamp: new Date().toISOString(),
    }
    dispatch({ type: 'ADD_MESSAGE', payload: userMessage })

    try {
      const { emergencyAPI } = await import('../services/api')
      
      let response
      switch (state.currentAgent) {
        case 'medical':
          response = await emergencyAPI.sendMedicalMessage(message, state.sessionId)
          break
        case 'fire':
          response = await emergencyAPI.sendFireMessage(message, state.sessionId)
          break
        case 'police':
          response = await emergencyAPI.sendPoliceMessage(message, state.sessionId)
          break
        case 'multi-agent':
        default:
          response = await emergencyAPI.sendMultiAgentMessage(message, state.sessionId)
          break
      }

      // Add agent response to chat
      const agentMessage: ChatMessage = {
        message_id: response.message_id,
        type: response.type as 'assistant' | 'system',
        content: response.content,
        timestamp: response.timestamp,
        needs_confirmation: response.needs_confirmation,
      }
      dispatch({ type: 'ADD_MESSAGE', payload: agentMessage })

      // Check if this is an emergency
      const isEmergency = response.content.toLowerCase().includes('emergency') ||
                         response.content.toLowerCase().includes('dispatch') ||
                         response.content.toLowerCase().includes('ambulance') ||
                         response.content.toLowerCase().includes('fire brigade') ||
                         response.content.toLowerCase().includes('police')
      
      dispatch({ type: 'SET_EMERGENCY', payload: isEmergency })

    } catch (error) {
      console.error('Error sending message:', error)
      dispatch({ type: 'SET_ERROR', payload: 'Failed to send message. Please try again.' })
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false })
    }
  }

  const getCurrentLocation = async () => {
    if (!navigator.geolocation) {
      dispatch({ type: 'SET_ERROR', payload: 'Geolocation is not supported by this browser.' })
      return
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const location = {
          lat: position.coords.latitude,
          lon: position.coords.longitude,
        }
        dispatch({ type: 'SET_LOCATION', payload: location })
      },
    )
  }

  const clearChat = () => {
    dispatch({ type: 'CLEAR_CHAT' })
    dispatch({ type: 'SET_SESSION_ID', payload: generateSessionId() })
  }

  return (
    <EmergencyContext.Provider value={{
      state,
      dispatch,
      sendMessage,
      getCurrentLocation,
      clearChat,
    }}>
      {children}
    </EmergencyContext.Provider>
  )
}

export function useEmergency() {
  const context = useContext(EmergencyContext)
  if (context === undefined) {
    throw new Error('useEmergency must be used within an EmergencyProvider')
  }
  return context
}

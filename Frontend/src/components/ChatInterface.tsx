import React, { useState, useRef, useEffect } from 'react'
import { Send, MapPin, AlertTriangle } from 'lucide-react'
import { useEmergency } from '../contexts/EmergencyContext'

interface ChatInterfaceProps {
  agentType: 'medical' | 'fire' | 'police' | 'multi-agent'
  title: string
  description: string
  gradientClass: string
  icon: React.ReactNode
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({
  title,
  gradientClass,
  icon
}) => {
  const [message, setMessage] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const { state, sendMessage, getCurrentLocation, clearChat } = useEmergency()

  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ 
        behavior: 'smooth',
        block: 'end',
        inline: 'nearest'
      })
    }
  }

  useEffect(() => {
    scrollToBottom()
  }, [state.chatHistory])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!message.trim() || state.isLoading) return

    await sendMessage(message)
    setMessage('')
    
    // Reset textarea height after sending message
    if (textareaRef.current) {
      textareaRef.current.style.height = '48px'
    }
    
    // Keep focus on textarea after sending message
    setTimeout(() => {
      if (textareaRef.current) {
        textareaRef.current.focus()
      }
    }, 100)
  }

  const handleLocationClick = () => {
    getCurrentLocation()
  }


  const formatMessage = (content: string) => {
    // Simple formatting for emergency responses
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br/>')
  }

  return (
    <div className="w-full">
      {/* Modern Chat Header */}
      <div className="bg-white rounded-t-3xl shadow-lg border-b border-gray-200">
        <div className={`${gradientClass} p-8 text-white rounded-t-3xl`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center shadow-lg">
                {icon}
              </div>
              <div>
                <h1 className="text-2xl font-bold">{title}</h1>
                <div className="flex items-center space-x-2 text-sm text-white/90">
                  <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                  <span className="font-medium">Active • Response ready</span>
                </div>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <button 
                onClick={handleLocationClick} 
                className="p-3 rounded-full hover:bg-white/20 transition-colors"
                title="Share Location"
              >
                <MapPin className="w-6 h-6 text-white/90" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Chat Container */}
      <div className="bg-white rounded-b-3xl shadow-lg">
        {/* Chat Messages */}
        <div className="h-[500px] overflow-y-auto p-6 space-y-6 bg-gradient-to-b from-gray-50 to-white custom-scrollbar scroll-smooth">
          {state.chatHistory.length === 0 ? (
            <div className="text-center text-gray-500 py-12">
              <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-r from-emergency-red to-emergency-orange rounded-full flex items-center justify-center shadow-lg">
                {icon}
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-3">Welcome to {title}</h3>
              <p className="text-lg text-gray-600 max-w-md mx-auto leading-relaxed">
                Describe your emergency and I'll help you get the assistance you need. Our AI will automatically coordinate the appropriate services.
              </p>
            </div>
          ) : (
            state.chatHistory.map((msg) => (
              <div
                key={msg.message_id}
                className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-2xl ${msg.type === 'user' ? 'order-2' : 'order-1'}`}>
                  {msg.type === 'assistant' || msg.type === 'system' ? (
                    <div className="bg-white rounded-2xl rounded-tl-sm p-4 shadow-lg border border-gray-200">
                      <div
                        className="text-base leading-relaxed"
                        dangerouslySetInnerHTML={{
                          __html: formatMessage(msg.content)
                        }}
                      />
                      <div className="text-xs mt-2 text-gray-500">
                        {new Date(msg.timestamp).toLocaleTimeString()}
                      </div>
                    </div>
                  ) : (
                    <div className="bg-gradient-to-r from-emergency-blue to-blue-600 text-white rounded-2xl rounded-tr-sm p-4 shadow-lg">
                      <div
                        className="text-base leading-relaxed"
                        dangerouslySetInnerHTML={{
                          __html: formatMessage(msg.content)
                        }}
                      />
                      <div className="text-xs mt-2 text-blue-100">
                        {new Date(msg.timestamp).toLocaleTimeString()}
                      </div>
                    </div>
                  )}
                </div>
                {msg.type === 'user' && (
                  <div className="w-10 h-10 bg-gradient-to-r from-emergency-blue to-blue-600 rounded-full flex items-center justify-center mr-3 order-1 shadow-md">
                    <span className="text-sm font-bold text-white">U</span>
                  </div>
                )}
              </div>
            ))
          )}
          
          {state.isLoading && (
            <div className="flex justify-start">
              <div className="bg-white rounded-2xl rounded-tl-sm p-4 shadow-lg border border-gray-200">
                <div className="flex items-center space-x-3">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-emergency-blue rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-emergency-blue rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                    <div className="w-2 h-2 bg-emergency-blue rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                  </div>
                  <span className="text-sm text-gray-600 font-medium">AI is analyzing your request...</span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Error Display */}
        {state.error && (
          <div className="mx-4 mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center space-x-2 text-red-800">
              <AlertTriangle className="w-4 h-4" />
              <span className="text-sm">{state.error}</span>
            </div>
          </div>
        )}

      

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="p-6 bg-white border-t border-gray-200">
          <div className="flex items-end space-x-3">
            <div className="flex-1 relative">
              <textarea
                ref={textareaRef}
                value={message}
                onChange={(e) => {
                  setMessage(e.target.value)
                  // Auto-resize textarea without causing screen jump
                  const textarea = e.target
                  textarea.style.height = 'auto'
                  const newHeight = Math.min(textarea.scrollHeight, 120)
                  textarea.style.height = newHeight + 'px'
                  
                  // Don't scroll during typing - only when needed
                  // Removed automatic scroll to prevent focus jumping
                }}
                placeholder="Type your emergency details or ask for help..."
                className="w-full px-4 py-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-emergency-blue focus:border-transparent text-base resize-none min-h-[48px] max-h-[120px] leading-relaxed"
                disabled={state.isLoading}
                rows={1}
                style={{ height: '48px' }}
              />
            </div>
            <button
              type="button"
              onClick={handleLocationClick}
              className="p-3 text-gray-400 hover:text-emergency-blue transition-colors rounded-full hover:bg-gray-100"
              title="Share Location"
            >
              <MapPin className="w-6 h-6" />
            </button>
            <button
              type="submit"
              disabled={!message.trim() || state.isLoading}
              className="w-12 h-12 bg-gradient-to-r from-emergency-blue to-blue-600 text-white rounded-full flex items-center justify-center hover:from-blue-600 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-105 shadow-lg"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
          
          {/* Quick Actions */}
          <div className="flex flex-wrap gap-3 mt-4">
            <button
              type="button"
              onClick={() => {
                setMessage('I need immediate medical assistance')
                // Reset textarea height and keep focus
                if (textareaRef.current) {
                  textareaRef.current.style.height = '48px'
                  textareaRef.current.focus()
                }
              }}
              className="px-4 py-2 text-sm bg-red-100 text-red-800 rounded-full hover:bg-red-200 transition-all duration-300 transform hover:scale-105 font-medium"
            >
              🏥 Medical Emergency
            </button>
            <button
              type="button"
              onClick={() => {
                setMessage('Fire emergency, need fire brigade')
                // Reset textarea height and keep focus
                if (textareaRef.current) {
                  textareaRef.current.style.height = '48px'
                  textareaRef.current.focus()
                }
              }}
              className="px-4 py-2 text-sm bg-orange-100 text-orange-800 rounded-full hover:bg-orange-200 transition-all duration-300 transform hover:scale-105 font-medium"
            >
              🔥 Fire Emergency
            </button>
            <button
              type="button"
              onClick={() => {
                setMessage('Need police assistance')
                // Reset textarea height and keep focus
                if (textareaRef.current) {
                  textareaRef.current.style.height = '48px'
                  textareaRef.current.focus()
                }
              }}
              className="px-4 py-2 text-sm bg-blue-100 text-blue-800 rounded-full hover:bg-blue-200 transition-all duration-300 transform hover:scale-105 font-medium"
            >
              👮 Police Emergency
            </button>
            <button
              type="button"
              onClick={clearChat}
              className="px-4 py-2 text-sm bg-gray-100 text-gray-800 rounded-full hover:bg-gray-200 transition-all duration-300 transform hover:scale-105 font-medium"
            >
              🗑️ Clear Chat
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default ChatInterface

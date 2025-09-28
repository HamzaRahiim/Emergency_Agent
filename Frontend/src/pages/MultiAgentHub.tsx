import React from 'react'
import { Zap, Clock, Users, Brain, Shield, Heart, Flame, AlertTriangle } from 'lucide-react'
import ChatInterface from '../components/ChatInterface'
import Header from '../components/Header'
import Footer from '../components/Footer'
import { useScrollAnimation } from '../hooks/useScrollAnimation'

const MultiAgentHub: React.FC = () => {
  // Scroll animations for different sections
  const heroRef = useScrollAnimation({ threshold: 0.2 })
  const featuresRef = useScrollAnimation({ threshold: 0.1 })
  const examplesRef = useScrollAnimation({ threshold: 0.1 })
  const tipsRef = useScrollAnimation({ threshold: 0.1 })

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100">
      <Header />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-12">
          {/* Hero Section */}
          <div 
            ref={heroRef.ref}
            className={`text-center transition-all duration-1000 ${
              heroRef.isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
            }`}
          >
            <div className="flex items-center justify-center w-24 h-24 mx-auto mb-8 bg-gradient-to-r from-emergency-red via-emergency-orange to-emergency-red rounded-full group hover:scale-110 hover:rotate-12 transition-all duration-500 shadow-2xl">
              <Zap className="w-12 h-12 text-white group-hover:animate-pulse" />
            </div>
            <h1 className="text-5xl font-bold bg-gradient-to-r from-emergency-red to-emergency-orange bg-clip-text text-transparent mb-6 group-hover:scale-105 transition-transform duration-300">
              Multi-Agent Emergency Hub
            </h1>
            <p className="text-xl text-gray-700 max-w-4xl mx-auto leading-relaxed font-medium">
              🚨 **Intelligent Emergency Coordination System** 🚨<br/>
              Describe your emergency and our AI will automatically coordinate the best response across medical, fire, and police services. 
              Get instant, coordinated assistance when every second counts.
            </p>
          </div>

          {/* Features */}
          <div 
            ref={featuresRef.ref}
            className={`grid grid-cols-1 md:grid-cols-3 gap-8 transition-all duration-1000 ${
              featuresRef.isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
            }`}
          >
            <div className="bg-white rounded-2xl shadow-xl p-8 text-center hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-3 hover:scale-105 group border border-gray-100">
              <div className="flex items-center justify-center w-16 h-16 mx-auto mb-6 bg-gradient-to-r from-purple-500 to-purple-600 rounded-full group-hover:scale-110 group-hover:rotate-12 transition-all duration-500 shadow-lg">
                <Brain className="w-8 h-8 text-white group-hover:animate-pulse" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-purple-600 transition-colors duration-300">AI-Powered Intelligence</h3>
              <p className="text-gray-600 leading-relaxed">Advanced AI automatically detects emergency types and routes requests to the most appropriate services for optimal response.</p>
            </div>
            
            <div className="bg-white rounded-2xl shadow-xl p-8 text-center hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-3 hover:scale-105 group border border-gray-100">
              <div className="flex items-center justify-center w-16 h-16 mx-auto mb-6 bg-gradient-to-r from-green-500 to-green-600 rounded-full group-hover:scale-110 group-hover:rotate-12 transition-all duration-500 shadow-lg">
                <Users className="w-8 h-8 text-white group-hover:animate-pulse" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-green-600 transition-colors duration-300">Multi-Service Coordination</h3>
              <p className="text-gray-600 leading-relaxed">Seamlessly coordinates between medical, fire, and police services for complex emergencies requiring multiple response teams.</p>
            </div>
            
            <div className="bg-white rounded-2xl shadow-xl p-8 text-center hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-3 hover:scale-105 group border border-gray-100">
              <div className="flex items-center justify-center w-16 h-16 mx-auto mb-6 bg-gradient-to-r from-blue-500 to-blue-600 rounded-full group-hover:scale-110 group-hover:rotate-12 transition-all duration-500 shadow-lg">
                <Clock className="w-8 h-8 text-white group-hover:animate-pulse" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-blue-600 transition-colors duration-300">Real-time Response</h3>
              <p className="text-gray-600 leading-relaxed">Instant coordination and response with live updates, ensuring emergency services are dispatched immediately when needed.</p>
            </div>
          </div>

          {/* Chat Interface - Full Width */}
          <div className="w-full">
            <div className="bg-white rounded-3xl shadow-2xl border border-gray-100 overflow-hidden hover:shadow-3xl transition-all duration-500 transform hover:-translate-y-1">
              <ChatInterface
                agentType="multi-agent"
                title="🚨 Emergency Coordination Hub"
                description="Describe your emergency and I'll coordinate the appropriate services automatically"
                gradientClass="bg-gradient-to-r from-emergency-red via-emergency-orange to-emergency-red"
                icon={<Zap className="w-8 h-8" />}
              />
            </div>
          </div>

          {/* Multi-Service Examples */}
          <div 
            ref={examplesRef.ref}
            className={`bg-gradient-to-br from-emergency-red via-emergency-orange to-emergency-red rounded-3xl p-10 text-white relative overflow-hidden group hover:shadow-2xl transition-all duration-500 ${
              examplesRef.isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
            }`}
          >
            <div className="absolute inset-0 bg-gradient-to-br from-transparent via-white/10 to-transparent animate-pulse"></div>
            <div className="absolute top-0 right-0 w-32 h-32 bg-white/5 rounded-full -translate-y-16 translate-x-16"></div>
            <div className="absolute bottom-0 left-0 w-24 h-24 bg-white/5 rounded-full translate-y-12 -translate-x-12"></div>
            <div className="relative">
              <div className="flex items-center justify-center w-16 h-16 mx-auto mb-6 bg-white/20 rounded-full group-hover:scale-110 group-hover:rotate-12 transition-all duration-500">
                <AlertTriangle className="w-8 h-8 text-white group-hover:animate-pulse" />
              </div>
              <h3 className="text-3xl font-bold mb-8 text-center group-hover:scale-105 transition-transform duration-300">
                🚨 Multi-Service Emergency Examples 🚨
              </h3>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 text-base">
                <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
                  <h4 className="font-bold mb-6 text-xl flex items-center space-x-2">
                    <Flame className="w-6 h-6" />
                    <span>Complex Emergencies:</span>
                  </h4>
                  <ul className="space-y-3 text-white/95">
                    <li className="flex items-center space-x-3 p-2 rounded-lg bg-white/5">
                      <div className="w-3 h-3 bg-white rounded-full animate-pulse"></div>
                      <span className="font-medium">🔥 Fire with injuries → Fire + Medical</span>
                    </li>
                    <li className="flex items-center space-x-3 p-2 rounded-lg bg-white/5">
                      <div className="w-3 h-3 bg-white rounded-full animate-pulse"></div>
                      <span className="font-medium">🚗 Traffic accident with casualties → Police + Medical</span>
                    </li>
                    <li className="flex items-center space-x-3 p-2 rounded-lg bg-white/5">
                      <div className="w-3 h-3 bg-white rounded-full animate-pulse"></div>
                      <span className="font-medium">🏢 Building collapse → Fire + Medical + Police</span>
                    </li>
                    <li className="flex items-center space-x-3 p-2 rounded-lg bg-white/5">
                      <div className="w-3 h-3 bg-white rounded-full animate-pulse"></div>
                      <span className="font-medium">👮 Crime with injuries → Police + Medical</span>
                    </li>
                  </ul>
                </div>
                <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
                  <h4 className="font-bold mb-6 text-xl flex items-center space-x-2">
                    <Brain className="w-6 h-6" />
                    <span>AI Coordination:</span>
                  </h4>
                  <ul className="space-y-3 text-white/95">
                    <li className="flex items-center space-x-3 p-2 rounded-lg bg-white/5">
                      <div className="w-3 h-3 bg-white rounded-full animate-pulse"></div>
                      <span className="font-medium">🤖 Automatic service detection</span>
                    </li>
                    <li className="flex items-center space-x-3 p-2 rounded-lg bg-white/5">
                      <div className="w-3 h-3 bg-white rounded-full animate-pulse"></div>
                      <span className="font-medium">⚡ Real-time agent coordination</span>
                    </li>
                    <li className="flex items-center space-x-3 p-2 rounded-lg bg-white/5">
                      <div className="w-3 h-3 bg-white rounded-full animate-pulse"></div>
                      <span className="font-medium">🎯 Unified emergency response</span>
                    </li>
                    <li className="flex items-center space-x-3 p-2 rounded-lg bg-white/5">
                      <div className="w-3 h-3 bg-white rounded-full animate-pulse"></div>
                      <span className="font-medium">🧠 Context-aware routing</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          {/* Emergency Tips */}
          <div 
            ref={tipsRef.ref}
            className={`bg-gradient-to-br from-red-50 via-orange-50 to-red-50 rounded-3xl p-10 border border-red-100 hover:shadow-xl transition-all duration-500 ${
              tipsRef.isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
            }`}
          >
            <div className="text-center mb-8">
              <div className="flex items-center justify-center w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-emergency-red to-emergency-orange rounded-full group-hover:scale-110 group-hover:rotate-12 transition-all duration-500">
                <AlertTriangle className="w-8 h-8 text-white group-hover:animate-pulse" />
              </div>
              <h3 className="text-3xl font-bold text-gray-900 mb-2">🚨 Emergency Response Tips 🚨</h3>
              <p className="text-gray-600">Essential guidelines for effective emergency communication</p>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 text-base">
              <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-6 border border-red-200">
                <h4 className="font-bold text-gray-900 mb-6 text-xl flex items-center space-x-2">
                  <Heart className="w-6 h-6 text-emergency-red" />
                  <span>For Any Emergency:</span>
                </h4>
                <ul className="space-y-4">
                  <li className="flex items-start space-x-3 p-3 rounded-lg bg-white/50 border border-red-100">
                    <div className="w-3 h-3 bg-emergency-red rounded-full mt-2 animate-pulse"></div>
                    <span className="font-medium text-gray-800">🧘 Stay calm and describe the situation clearly</span>
                  </li>
                  <li className="flex items-start space-x-3 p-3 rounded-lg bg-white/50 border border-red-100">
                    <div className="w-3 h-3 bg-emergency-red rounded-full mt-2 animate-pulse"></div>
                    <span className="font-medium text-gray-800">📍 Provide your exact location if possible</span>
                  </li>
                  <li className="flex items-start space-x-3 p-3 rounded-lg bg-white/50 border border-red-100">
                    <div className="w-3 h-3 bg-emergency-red rounded-full mt-2 animate-pulse"></div>
                    <span className="font-medium text-gray-800">🏥 Mention any injuries or casualties</span>
                  </li>
                  <li className="flex items-start space-x-3 p-3 rounded-lg bg-white/50 border border-red-100">
                    <div className="w-3 h-3 bg-emergency-red rounded-full mt-2 animate-pulse"></div>
                    <span className="font-medium text-gray-800">🤖 Follow the AI agent's instructions</span>
                  </li>
                </ul>
              </div>
              <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-6 border border-red-200">
                <h4 className="font-bold text-gray-900 mb-6 text-xl flex items-center space-x-2">
                  <Brain className="w-6 h-6 text-emergency-orange" />
                  <span>System Capabilities:</span>
                </h4>
                <ul className="space-y-4">
                  <li className="flex items-start space-x-3 p-3 rounded-lg bg-white/50 border border-orange-100">
                    <div className="w-3 h-3 bg-emergency-orange rounded-full mt-2 animate-pulse"></div>
                    <span className="font-medium text-gray-800">🔍 Multi-service emergency detection</span>
                  </li>
                  <li className="flex items-start space-x-3 p-3 rounded-lg bg-white/50 border border-orange-100">
                    <div className="w-3 h-3 bg-emergency-orange rounded-full mt-2 animate-pulse"></div>
                    <span className="font-medium text-gray-800">⚡ Automatic agent coordination</span>
                  </li>
                  <li className="flex items-start space-x-3 p-3 rounded-lg bg-white/50 border border-orange-100">
                    <div className="w-3 h-3 bg-emergency-orange rounded-full mt-2 animate-pulse"></div>
                    <span className="font-medium text-gray-800">🗺️ Location-based service routing</span>
                  </li>
                  <li className="flex items-start space-x-3 p-3 rounded-lg bg-white/50 border border-orange-100">
                    <div className="w-3 h-3 bg-emergency-orange rounded-full mt-2 animate-pulse"></div>
                    <span className="font-medium text-gray-800">⚡ Real-time emergency response</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <Footer />
    </div>
  )
}

export default MultiAgentHub

import React from 'react'
import { Flame, MapPin, Phone, Clock } from 'lucide-react'
import ChatInterface from '../components/ChatInterface'
import Header from '../components/Header'
import Footer from '../components/Footer'
import { useScrollAnimation } from '../hooks/useScrollAnimation'

const FireEmergency: React.FC = () => {
  // Scroll animations for different sections
  const heroRef = useScrollAnimation({ threshold: 0.2 })
  const statsRef = useScrollAnimation({ threshold: 0.1 })
  const tipsRef = useScrollAnimation({ threshold: 0.1 })

  return (
    <div className="min-h-screen bg-white">
      <Header />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8">
          {/* Hero Section */}
          <div 
            ref={heroRef.ref}
            className={`text-center transition-all duration-1000 ${
              heroRef.isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
            }`}
          >
            <div className="flex items-center justify-center w-20 h-20 mx-auto mb-6 bg-gradient-to-r from-emergency-orange to-emergency-red rounded-full group hover:scale-110 hover:rotate-12 transition-all duration-500">
              <Flame className="w-10 h-10 text-white group-hover:animate-pulse" />
            </div>
            <h1 className="text-4xl font-bold text-gray-900 mb-4 group-hover:text-emergency-orange transition-colors duration-300">
              Fire & Emergency Services
            </h1>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Get immediate fire brigade response, rescue operations, and emergency services. 
              Our AI agent coordinates fire and emergency response across Karachi with 15+ fire stations.
            </p>
          </div>

          {/* Quick Info */}
          <div 
            ref={statsRef.ref}
            className={`grid grid-cols-1 md:grid-cols-3 gap-6 transition-all duration-1000 ${
              statsRef.isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
            }`}
          >
            <div className="bg-white rounded-lg shadow-lg p-6 text-center hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 hover:scale-105 group">
              <div className="flex items-center justify-center w-12 h-12 mx-auto mb-4 bg-orange-100 rounded-full group-hover:scale-110 group-hover:rotate-12 transition-all duration-500">
                <MapPin className="w-6 h-6 text-emergency-orange group-hover:animate-pulse" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2 group-hover:text-emergency-orange transition-colors duration-300">15+ Stations</h3>
              <p className="text-sm text-gray-600">Fire stations across Karachi</p>
            </div>
            
            <div className="bg-white rounded-lg shadow-lg p-6 text-center hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 hover:scale-105 group">
              <div className="flex items-center justify-center w-12 h-12 mx-auto mb-4 bg-green-100 rounded-full group-hover:scale-110 group-hover:rotate-12 transition-all duration-500">
                <Clock className="w-6 h-6 text-green-600 group-hover:animate-pulse" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2 group-hover:text-green-600 transition-colors duration-300">8-12 min</h3>
              <p className="text-sm text-gray-600">Average response time</p>
            </div>
            
            <div className="bg-white rounded-lg shadow-lg p-6 text-center hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 hover:scale-105 group">
              <div className="flex items-center justify-center w-12 h-12 mx-auto mb-4 bg-red-100 rounded-full group-hover:scale-110 group-hover:rotate-12 transition-all duration-500">
                <Phone className="w-6 h-6 text-red-600 group-hover:animate-pulse" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2 group-hover:text-red-600 transition-colors duration-300">24/7 Service</h3>
              <p className="text-sm text-gray-600">Always available</p>
            </div>
          </div>

          {/* Chat Interface */}
          <div className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-2xl transition-all duration-500">
            <ChatInterface
              agentType="fire"
              title="Fire & Emergency Coordinator"
              description="Report fire emergencies, building collapses, gas leaks, or rescue operations"
              gradientClass="bg-gradient-to-r from-emergency-orange to-emergency-red"
              icon={<Flame className="w-6 h-6" />}
            />
          </div>

          {/* Emergency Tips */}
          <div 
            ref={tipsRef.ref}
            className={`bg-orange-50 rounded-2xl p-8 hover:shadow-lg transition-all duration-500 ${
              tipsRef.isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
            }`}
          >
            <h3 className="text-2xl font-bold text-gray-900 mb-6">Fire Emergency Tips</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm text-gray-700">
              <div>
                <h4 className="font-semibold text-gray-900 mb-4 text-lg">If You Discover a Fire:</h4>
                <ul className="space-y-2">
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-emergency-orange rounded-full"></div>
                    <span>Call 112 immediately</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-emergency-orange rounded-full"></div>
                    <span>Evacuate the building immediately</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-emergency-orange rounded-full"></div>
                    <span>Use stairs, not elevators</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-emergency-orange rounded-full"></div>
                    <span>Stay low to avoid smoke</span>
                  </li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 mb-4 text-lg">Types of Fire Emergencies:</h4>
                <ul className="space-y-2">
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-emergency-orange rounded-full"></div>
                    <span>Building fires</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-emergency-orange rounded-full"></div>
                    <span>Vehicle fires</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-emergency-orange rounded-full"></div>
                    <span>Gas leaks</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-emergency-orange rounded-full"></div>
                    <span>Building collapses</span>
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

export default FireEmergency

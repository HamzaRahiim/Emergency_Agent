import React from 'react'
import { Link } from 'react-router-dom'
import { 
  Heart, 
  Flame, 
  Shield, 
  Zap, 
  MapPin, 
  Phone, 
  Clock,
  Users,
  AlertTriangle,
  Bot,
} from 'lucide-react'
import Header from '../components/Header'
import Footer from '../components/Footer'
import { useScrollAnimation } from '../hooks/useScrollAnimation'

const HomePage: React.FC = () => {
  // Scroll animations for different sections
  const heroRef = useScrollAnimation({ threshold: 0.2 })
  const howItWorksRef = useScrollAnimation({ threshold: 0.1 })
  const servicesRef = useScrollAnimation({ threshold: 0.1 })
  const statsRef = useScrollAnimation({ threshold: 0.1 })
  const faqRef = useScrollAnimation({ threshold: 0.1 })
  const techRef = useScrollAnimation({ threshold: 0.1 })
  const contactRef = useScrollAnimation({ threshold: 0.1 })

  return (
    <div className="min-h-screen bg-white">
      <Header />

      {/* Hero Section */}
      <section 
        ref={heroRef.ref}
        className={`py-16 px-4 sm:px-6 lg:px-8 transition-all duration-1000 ${
          heroRef.isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        }`}
      >
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold text-emergency-red mb-4 animate-pulse">
            Emergency Response
          </h1>
          <h2 className="text-3xl font-semibold text-gray-900 mb-6">
            When Every Second Counts
          </h2>
          <p className="text-lg text-gray-600 mb-12 max-w-2xl mx-auto">
            Our AI-powered emergency response system ensures rapid, coordinated assistance when you need it most. 
            Get instant help from medical, fire, police, and emergency services across Karachi.
          </p>
          
          {/* Emergency Request Card */}
          <div className="bg-white rounded-2xl shadow-lg p-8 max-w-md mx-auto hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 hover:scale-105 group">
            <h3 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-emergency-red transition-colors duration-300">
              Emergency Request
            </h3>
            <p className="text-gray-600 mb-6">Please enter your details and we will help you immediately</p>
            <Link
              to="/hub"
              className="w-full bg-emergency-red text-white font-bold py-4 px-6 rounded-lg flex items-center justify-center space-x-2 hover:bg-red-700 transition-all duration-300 transform hover:scale-105 hover:shadow-lg group"
            >
              <AlertTriangle className="w-5 h-5 group-hover:animate-bounce" />
              <span>EMERGENCY REQUEST</span>
            </Link>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section 
        ref={howItWorksRef.ref}
        className={`py-16 px-4 sm:px-6 lg:px-8 bg-gray-50 transition-all duration-1000 ${
          howItWorksRef.isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        }`}
      >
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">How It Works</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Our streamlined emergency response system ensures you receive the right help when you need it most
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Step 1: Report Emergency */}
            <div className="text-center group hover:transform hover:scale-105 transition-all duration-500">
              <div className="w-16 h-16 bg-emergency-red rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 group-hover:rotate-12 transition-all duration-500">
                <span className="text-2xl font-bold text-white">1</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4 group-hover:text-emergency-red transition-colors duration-300">
                Report Emergency
              </h3>
              <p className="text-gray-600 mb-6">
                Find yourself in an emergency situation? Quickly report it through our platform, providing necessary details. 
                Our AI will analyze and provide you with the best course of action.
              </p>
              <div className="flex justify-center space-x-4">
                <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center hover:bg-emergency-red hover:text-white transition-all duration-300 group-hover:scale-110">
                  <AlertTriangle className="w-4 h-4 text-emergency-red group-hover:text-white transition-colors duration-300" />
                </div>
                <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center hover:bg-emergency-red hover:text-white transition-all duration-300 group-hover:scale-110">
                  <Users className="w-4 h-4 text-emergency-red group-hover:text-white transition-colors duration-300" />
                </div>
                <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center hover:bg-emergency-red hover:text-white transition-all duration-300 group-hover:scale-110">
                  <MapPin className="w-4 h-4 text-emergency-red group-hover:text-white transition-colors duration-300" />
                </div>
              </div>
            </div>
            
            {/* Step 2: Instant Dispatch */}
            <div className="text-center group hover:transform hover:scale-105 transition-all duration-500">
              <div className="w-16 h-16 bg-emergency-orange rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 group-hover:rotate-12 transition-all duration-500">
                <span className="text-2xl font-bold text-white">2</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4 group-hover:text-emergency-orange transition-colors duration-300">
                Instant Dispatch
              </h3>
              <p className="text-gray-600 mb-6">
                Our AI will instantly dispatch the nearest and most appropriate emergency services to your location. 
                We ensure rapid response times with coordinated multi-agent assistance.
              </p>
              <div className="flex justify-center space-x-4">
                <div className="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center hover:bg-emergency-orange hover:text-white transition-all duration-300 group-hover:scale-110">
                  <Clock className="w-4 h-4 text-emergency-orange group-hover:text-white transition-colors duration-300" />
                </div>
                <div className="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center hover:bg-emergency-orange hover:text-white transition-all duration-300 group-hover:scale-110">
                  <MapPin className="w-4 h-4 text-emergency-orange group-hover:text-white transition-colors duration-300" />
                </div>
                <div className="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center hover:bg-emergency-orange hover:text-white transition-all duration-300 group-hover:scale-110">
                  <Heart className="w-4 h-4 text-emergency-orange group-hover:text-white transition-colors duration-300" />
                </div>
              </div>
            </div>
            
            {/* Step 3: Real-Time Updates */}
            <div className="text-center group hover:transform hover:scale-105 transition-all duration-500">
              <div className="w-16 h-16 bg-emergency-green rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 group-hover:rotate-12 transition-all duration-500">
                <span className="text-2xl font-bold text-white">3</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4 group-hover:text-emergency-green transition-colors duration-300">
                Real-Time Updates
              </h3>
              <p className="text-gray-600 mb-6">
                Receive real-time updates on the status of your emergency, including estimated arrival times and 
                service provider details. Stay informed every step of the way.
              </p>
              <div className="flex justify-center space-x-4">
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center hover:bg-emergency-green hover:text-white transition-all duration-300 group-hover:scale-110">
                  <Phone className="w-4 h-4 text-emergency-green group-hover:text-white transition-colors duration-300" />
                </div>
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center hover:bg-emergency-green hover:text-white transition-all duration-300 group-hover:scale-110">
                  <AlertTriangle className="w-4 h-4 text-emergency-green group-hover:text-white transition-colors duration-300" />
                </div>
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center hover:bg-emergency-green hover:text-white transition-all duration-300 group-hover:scale-110">
                  <Clock className="w-4 h-4 text-emergency-green group-hover:text-white transition-colors duration-300" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Emergency Service Categories */}
      <section 
        ref={servicesRef.ref}
        className={`py-16 px-4 sm:px-6 lg:px-8 transition-all duration-1000 ${
          servicesRef.isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        }`}
      >
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Emergency Services</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Our comprehensive emergency response system covers all critical services to ensure your safety and well-being
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Medical Emergency Card */}
            <div className="bg-white rounded-2xl shadow-lg p-8 hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 hover:scale-105 group">
              <div className="text-center mb-6">
                <div className="w-16 h-16 bg-emergency-blue/10 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:scale-110 group-hover:rotate-12 transition-all duration-500">
                  <Heart className="w-8 h-8 text-emergency-blue group-hover:animate-pulse" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-emergency-blue transition-colors duration-300">
                  Medical Emergency
                </h3>
                <p className="text-gray-600">
                  Rapid medical response with trained professionals and advanced equipment to handle any medical emergency situation.
                </p>
              </div>
              
              <div className="space-y-3">
                <div className="flex items-center space-x-3 group/item">
                  <div className="w-5 h-5 bg-emergency-blue rounded-full flex items-center justify-center group-hover/item:scale-125 transition-transform duration-300">
                    <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <span className="text-gray-700 group-hover/item:text-emergency-blue transition-colors duration-300">Ambulance Service</span>
                </div>
                <div className="flex items-center space-x-3 group/item">
                  <div className="w-5 h-5 bg-emergency-blue rounded-full flex items-center justify-center group-hover/item:scale-125 transition-transform duration-300">
                    <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <span className="text-gray-700 group-hover/item:text-emergency-blue transition-colors duration-300">First Aid</span>
                </div>
                <div className="flex items-center space-x-3 group/item">
                  <div className="w-5 h-5 bg-emergency-blue rounded-full flex items-center justify-center group-hover/item:scale-125 transition-transform duration-300">
                    <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <span className="text-gray-700 group-hover/item:text-emergency-blue transition-colors duration-300">Medical Assistance</span>
                </div>
                <div className="flex items-center space-x-3 group/item">
                  <div className="w-5 h-5 bg-emergency-blue rounded-full flex items-center justify-center group-hover/item:scale-125 transition-transform duration-300">
                    <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <span className="text-gray-700 group-hover/item:text-emergency-blue transition-colors duration-300">Emergency Care</span>
                </div>
              </div>
            </div>

            {/* Fire & Rescue Card */}
            <div className="bg-white rounded-2xl shadow-lg p-8 hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 hover:scale-105 group">
              <div className="text-center mb-6">
                <div className="w-16 h-16 bg-emergency-orange/10 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:scale-110 group-hover:rotate-12 transition-all duration-500">
                  <Flame className="w-8 h-8 text-emergency-orange group-hover:animate-pulse" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-emergency-orange transition-colors duration-300">
                  Fire & Rescue
                </h3>
                <p className="text-gray-600">
                  Professional firefighting and rescue operations with specialized equipment and trained personnel for any emergency.
                </p>
              </div>
              
              <div className="space-y-3">
                <div className="flex items-center space-x-3 group/item">
                  <div className="w-5 h-5 bg-emergency-orange rounded-full flex items-center justify-center group-hover/item:scale-125 transition-transform duration-300">
                    <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <span className="text-gray-700 group-hover/item:text-emergency-orange transition-colors duration-300">Firefighting</span>
                </div>
                <div className="flex items-center space-x-3 group/item">
                  <div className="w-5 h-5 bg-emergency-orange rounded-full flex items-center justify-center group-hover/item:scale-125 transition-transform duration-300">
                    <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <span className="text-gray-700 group-hover/item:text-emergency-orange transition-colors duration-300">Rescue Operations</span>
                </div>
                <div className="flex items-center space-x-3 group/item">
                  <div className="w-5 h-5 bg-emergency-orange rounded-full flex items-center justify-center group-hover/item:scale-125 transition-transform duration-300">
                    <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <span className="text-gray-700 group-hover/item:text-emergency-orange transition-colors duration-300">Hazardous Material</span>
                </div>
                <div className="flex items-center space-x-3 group/item">
                  <div className="w-5 h-5 bg-emergency-orange rounded-full flex items-center justify-center group-hover/item:scale-125 transition-transform duration-300">
                    <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <span className="text-gray-700 group-hover/item:text-emergency-orange transition-colors duration-300">Emergency Evacuation</span>
                </div>
              </div>
            </div>

            {/* Police Response Card */}
            <div className="bg-white rounded-2xl shadow-lg p-8 hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 hover:scale-105 group">
              <div className="text-center mb-6">
                <div className="w-16 h-16 bg-emergency-blue/10 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:scale-110 group-hover:rotate-12 transition-all duration-500">
                  <Shield className="w-8 h-8 text-emergency-blue group-hover:animate-pulse" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-emergency-blue transition-colors duration-300">
                  Police Response
                </h3>
                <p className="text-gray-600">
                  Rapid law enforcement response with trained officers and specialized units to maintain public safety and security.
                </p>
              </div>
              
              <div className="space-y-3">
                <div className="flex items-center space-x-3 group/item">
                  <div className="w-5 h-5 bg-emergency-blue rounded-full flex items-center justify-center group-hover/item:scale-125 transition-transform duration-300">
                    <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <span className="text-gray-700 group-hover/item:text-emergency-blue transition-colors duration-300">Crime Prevention</span>
                </div>
                <div className="flex items-center space-x-3 group/item">
                  <div className="w-5 h-5 bg-emergency-blue rounded-full flex items-center justify-center group-hover/item:scale-125 transition-transform duration-300">
                    <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <span className="text-gray-700 group-hover/item:text-emergency-blue transition-colors duration-300">Traffic Control</span>
                </div>
                <div className="flex items-center space-x-3 group/item">
                  <div className="w-5 h-5 bg-emergency-blue rounded-full flex items-center justify-center group-hover/item:scale-125 transition-transform duration-300">
                    <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <span className="text-gray-700 group-hover/item:text-emergency-blue transition-colors duration-300">Emergency Patrol</span>
                </div>
                <div className="flex items-center space-x-3 group/item">
                  <div className="w-5 h-5 bg-emergency-blue rounded-full flex items-center justify-center group-hover/item:scale-125 transition-transform duration-300">
                    <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <span className="text-gray-700 group-hover/item:text-emergency-blue transition-colors duration-300">Public Safety</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Emergency Response Statistics */}
      <section 
        ref={statsRef.ref}
        className={`py-16 px-4 sm:px-6 lg:px-8 transition-all duration-1000 ${
          statsRef.isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        }`}
      >
        <div className="max-w-6xl mx-auto">
          <div className="bg-gradient-to-r from-pink-500 via-red-500 to-blue-600 rounded-2xl p-12 text-white relative overflow-hidden group hover:shadow-2xl transition-all duration-500">
            {/* Animated background */}
            <div className="absolute inset-0 bg-gradient-to-r from-pink-500 via-red-500 to-blue-600 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-transparent via-white/10 to-transparent animate-pulse"></div>
            
            <div className="text-center mb-12 relative">
              <h2 className="text-3xl font-bold mb-4 group-hover:scale-105 transition-transform duration-300">
                Emergency Response Statistics
              </h2>
              <p className="text-white/90 text-lg max-w-2xl mx-auto">
                Our commitment to excellence is reflected in our outstanding performance metrics and response capabilities
              </p>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 relative">
              {/* Average Response Time */}
              <div className="text-center group/stat hover:scale-110 transition-all duration-500">
                <div className="text-4xl md:text-5xl font-bold mb-2 group-hover/stat:animate-bounce">2.5</div>
                <div className="text-white/80 text-sm md:text-base group-hover/stat:text-white transition-colors duration-300">
                  Average Response Time (minutes)
                </div>
              </div>
              
              {/* Success Rate */}
              <div className="text-center group/stat hover:scale-110 transition-all duration-500">
                <div className="text-4xl md:text-5xl font-bold mb-2 group-hover/stat:animate-bounce">99.8%</div>
                <div className="text-white/80 text-sm md:text-base group-hover/stat:text-white transition-colors duration-300">
                  Success Rate
                </div>
              </div>
              
              {/* Service Availability */}
              <div className="text-center group/stat hover:scale-110 transition-all duration-500">
                <div className="text-4xl md:text-5xl font-bold mb-2 group-hover/stat:animate-bounce">24/7</div>
                <div className="text-white/80 text-sm md:text-base group-hover/stat:text-white transition-colors duration-300">
                  Service Availability
                </div>
              </div>
              
              {/* Active Responders */}
              <div className="text-center group/stat hover:scale-110 transition-all duration-500">
                <div className="text-4xl md:text-5xl font-bold mb-2 group-hover/stat:animate-bounce">150+</div>
                <div className="text-white/80 text-sm md:text-base group-hover/stat:text-white transition-colors duration-300">
                  Active Responders
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Frequently Asked Questions */}
      <section 
        ref={faqRef.ref}
        className={`py-16 px-4 sm:px-6 lg:px-8 bg-gray-50 transition-all duration-1000 ${
          faqRef.isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        }`}
      >
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Frequently Asked Questions</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Get answers to common questions about our emergency response services and how we can help you
            </p>
          </div>
          
          <div className="space-y-4">
            {/* FAQ Item 1 */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-lg transition-all duration-300 group">
              <button className="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 transition-all duration-300 group-hover:bg-emergency-red/5">
                <span className="font-semibold text-gray-900 group-hover:text-emergency-red transition-colors duration-300">
                  How quickly will emergency responders arrive?
                </span>
                <svg className="w-5 h-5 text-gray-500 transform transition-all duration-300 group-hover:rotate-180 group-hover:text-emergency-red" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div className="px-6 pb-4 text-gray-600">
                <p>Our average response time is 2.5 minutes for critical emergencies. We have strategically located response teams across Karachi to ensure rapid deployment to any location within the city.</p>
              </div>
            </div>

            {/* FAQ Item 2 */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-lg transition-all duration-300 group">
              <button className="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 transition-all duration-300 group-hover:bg-emergency-red/5">
                <span className="font-semibold text-gray-900 group-hover:text-emergency-red transition-colors duration-300">
                  What kind of emergencies do you respond to?
                </span>
                <svg className="w-5 h-5 text-gray-500 transform transition-all duration-300 group-hover:rotate-180 group-hover:text-emergency-red" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div className="px-6 pb-4 text-gray-600">
                <p>We respond to all types of emergencies including medical emergencies, fires, police situations, natural disasters, and multi-service emergencies that require coordinated response from multiple agencies.</p>
              </div>
            </div>

            {/* FAQ Item 3 */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-lg transition-all duration-300 group">
              <button className="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 transition-all duration-300 group-hover:bg-emergency-red/5">
                <span className="font-semibold text-gray-900 group-hover:text-emergency-red transition-colors duration-300">
                  Is the service available 24/7?
                </span>
                <svg className="w-5 h-5 text-gray-500 transform transition-all duration-300 group-hover:rotate-180 group-hover:text-emergency-red" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div className="px-6 pb-4 text-gray-600">
                <p>Yes, our emergency response system operates 24 hours a day, 7 days a week, 365 days a year. Our AI-powered system and response teams are always ready to assist you in any emergency situation.</p>
              </div>
            </div>

            {/* FAQ Item 4 */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-lg transition-all duration-300 group">
              <button className="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 transition-all duration-300 group-hover:bg-emergency-red/5">
                <span className="font-semibold text-gray-900 group-hover:text-emergency-red transition-colors duration-300">
                  What if I accidentally call emergency services?
                </span>
                <svg className="w-5 h-5 text-gray-500 transform transition-all duration-300 group-hover:rotate-180 group-hover:text-emergency-red" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div className="px-6 pb-4 text-gray-600">
                <p>No worries! Simply inform our AI assistant that it was an accidental call. Our system is designed to handle such situations gracefully and will not dispatch emergency services unless there's a confirmed emergency.</p>
              </div>
            </div>

            {/* FAQ Item 5 */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-lg transition-all duration-300 group">
              <button className="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 transition-all duration-300 group-hover:bg-emergency-red/5">
                <span className="font-semibold text-gray-900 group-hover:text-emergency-red transition-colors duration-300">
                  How can I volunteer for the service?
                </span>
                <svg className="w-5 h-5 text-gray-500 transform transition-all duration-300 group-hover:rotate-180 group-hover:text-emergency-red" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div className="px-6 pb-4 text-gray-600">
                <p>We welcome volunteers! Please contact us through our Contact page or call our main office. We offer various volunteer opportunities including community outreach, training programs, and emergency preparedness education.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Advanced Technology Section */}
      <section 
        ref={techRef.ref}
        className={`py-16 px-4 sm:px-6 lg:px-8 transition-all duration-1000 ${
          techRef.isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        }`}
      >
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Advanced Technology</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Our technology helps you stay connected and respond to emergency situations
            </p>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Features List */}
            <div className="space-y-8">
              {/* GPS Tracking */}
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <MapPin className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">GPS Tracking</h3>
                  <p className="text-gray-600">
                    Real-time location tracking ensures emergency responders can find you quickly and accurately, 
                    even in complex urban environments.
                  </p>
                </div>
              </div>
              
              {/* AI Powered Dispatch */}
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <Bot className="w-6 h-6 text-green-600" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">AI Powered Dispatch</h3>
                  <p className="text-gray-600">
                    Intelligent routing and resource allocation using advanced AI algorithms to ensure 
                    the fastest and most appropriate emergency response.
                  </p>
                </div>
              </div>
              
              {/* Real Time Communication */}
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <Phone className="w-6 h-6 text-purple-600" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Real Time Communication</h3>
                  <p className="text-gray-600">
                    Seamless communication between emergency responders, dispatchers, and victims 
                    with instant updates and status notifications.
                  </p>
                </div>
              </div>
              
              {/* Secure Data Protection */}
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <Shield className="w-6 h-6 text-red-600" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Secure Data Protection</h3>
                  <p className="text-gray-600">
                    Enterprise-grade security protocols protect your personal information and emergency data 
                    with end-to-end encryption and secure storage.
                  </p>
                </div>
              </div>
            </div>
            
            {/* Command Center Image */}
            <div className="text-center">
              <div className="bg-gray-100 rounded-2xl p-8 mb-6">
                <div className="bg-gray-200 rounded-lg h-64 flex items-center justify-center">
                  <div className="text-center">
                    <div className="w-16 h-16 bg-emergency-blue rounded-full flex items-center justify-center mx-auto mb-4">
                      <AlertTriangle className="w-8 h-8 text-white" />
                    </div>
                    <p className="text-gray-600 font-medium">24/7 Command Center</p>
                  </div>
                </div>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">24/7 Command Center</h3>
              <p className="text-gray-600">
                Our state-of-the-art command center operates around the clock with advanced monitoring systems, 
                trained operators, and cutting-edge technology to coordinate emergency responses across Karachi.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Information Section */}
      <section 
        ref={contactRef.ref}
        className={`py-16 px-4 sm:px-6 lg:px-8 bg-gray-50 transition-all duration-1000 ${
          contactRef.isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        }`}
      >
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Contact Information</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              We're here to help you 24/7. Reach out to us anytime.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Emergency Line */}
            <div className="bg-white rounded-2xl shadow-lg p-8 text-center">
              <div className="w-16 h-16 bg-emergency-red rounded-full flex items-center justify-center mx-auto mb-6">
                <Phone className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Emergency Line</h3>
              <p className="text-gray-600 mb-4">For immediate assistance in life-threatening situations.</p>
              <div className="text-3xl font-bold text-emergency-red mb-2">112</div>
              <p className="text-sm text-gray-500">Available 24/7</p>
            </div>
            
            {/* Support Center */}
            <div className="bg-white rounded-2xl shadow-lg p-8 text-center">
              <div className="w-16 h-16 bg-emergency-blue rounded-full flex items-center justify-center mx-auto mb-6">
                <div className="w-8 h-8 text-white font-bold text-xl">?</div>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Support Center</h3>
              <p className="text-gray-600 mb-4">For general inquiries, technical support, and non-emergency issues.</p>
              <div className="text-2xl font-bold text-emergency-blue mb-2">(021) 123 HELP</div>
              <p className="text-sm text-gray-500">Mon-Fri, 9 AM - 5 PM PKT</p>
            </div>
            
            {/* Technical Support */}
            <div className="bg-white rounded-2xl shadow-lg p-8 text-center">
              <div className="w-16 h-16 bg-emergency-green rounded-full flex items-center justify-center mx-auto mb-6">
                <Zap className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Technical Support</h3>
              <p className="text-gray-600 mb-4">For advanced technical assistance and troubleshooting.</p>
              <div className="text-2xl font-bold text-emergency-green mb-2">(021) 123-TECH</div>
              <p className="text-sm text-gray-500">Available 24/7</p>
            </div>
          </div>
          
          {/* Additional Ways to Reach Us */}
          <div className="mt-16 text-center">
            <h3 className="text-2xl font-bold text-gray-900 mb-8">Additional Ways to Reach Us</h3>
            <div className="flex flex-wrap justify-center gap-8">
              <div className="flex flex-col items-center space-y-2">
                <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center">
                  <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <span className="text-sm font-medium text-gray-700">Email Us</span>
              </div>
              
              <div className="flex flex-col items-center space-y-2">
                <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center">
                  <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                </div>
                <span className="text-sm font-medium text-gray-700">Live Chat</span>
              </div>
              
              <div className="flex flex-col items-center space-y-2">
                <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center">
                  <MapPin className="w-6 h-6 text-gray-600" />
                </div>
                <span className="text-sm font-medium text-gray-700">Visit Us</span>
              </div>
              
              <div className="flex flex-col items-center space-y-2">
                <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center">
                  <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <span className="text-sm font-medium text-gray-700">Schedule a Demo</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  )
}

export default HomePage

import React from 'react'
import { Link } from 'react-router-dom'
import { Phone, MapPin, ArrowUp } from 'lucide-react'
import logoImage from '../assets/logo.jpeg'

const Footer: React.FC = () => {
  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    })
  }

  return (
    <>
      {/* Scroll to Top Button */}
      <button
        onClick={scrollToTop}
        className="fixed bottom-8 right-8 w-12 h-12 bg-emergency-red text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-110 hover:-translate-y-1 z-50 group"
        aria-label="Scroll to top"
      >
        <ArrowUp className="w-6 h-6 mx-auto transition-transform duration-300 group-hover:-translate-y-1" />
      </button>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-5">
          <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-emergency-red via-transparent to-emergency-orange"></div>
        </div>
        
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 relative">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* Logo and Description */}
            <div className="col-span-1 md:col-span-2">
              <div className="flex items-center space-x-3 mb-4 group">
                <div className="w-12 h-12 rounded-lg overflow-hidden transition-all duration-300 group-hover:scale-110 group-hover:rotate-3 shadow-lg">
                  <img 
                    src={logoImage} 
                    alt="Emergency Agent Logo" 
                    className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
                  />
                </div>
                <span className="text-xl font-bold group-hover:text-emergency-red transition-colors duration-300">
                  Emergency Response
                </span>
              </div>
              <p className="text-gray-400 mb-4 max-w-md leading-relaxed">
                AI-powered emergency response system providing rapid, coordinated assistance 
                across Karachi. When every second counts, we're here to help.
              </p>
              <div className="flex items-center space-x-4 text-sm text-gray-400">
                <div className="flex items-center space-x-1 group cursor-pointer">
                  <Phone className="w-4 h-4 group-hover:text-emergency-red transition-colors duration-300" />
                  <span className="group-hover:text-white transition-colors duration-300">Emergency: 112</span>
                </div>
                <div className="flex items-center space-x-1 group cursor-pointer">
                  <MapPin className="w-4 h-4 group-hover:text-emergency-red transition-colors duration-300" />
                  <span className="group-hover:text-white transition-colors duration-300">Karachi, Pakistan</span>
                </div>
              </div>
            </div>
            
            {/* Quick Links */}
            <div>
              <h3 className="text-lg font-semibold mb-4 text-white">Quick Links</h3>
              <ul className="space-y-3">
                <li>
                  <Link 
                    to="/hub" 
                    className="text-gray-400 hover:text-white transition-all duration-300 relative group"
                  >
                    Emergency Hub
                    <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-emergency-red transition-all duration-300 group-hover:w-full"></span>
                  </Link>
                </li>
                <li>
                  <Link 
                    to="/medical" 
                    className="text-gray-400 hover:text-white transition-all duration-300 relative group"
                  >
                    Medical Emergency
                    <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-emergency-red transition-all duration-300 group-hover:w-full"></span>
                  </Link>
                </li>
                <li>
                  <Link 
                    to="/fire" 
                    className="text-gray-400 hover:text-white transition-all duration-300 relative group"
                  >
                    Fire & Rescue
                    <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-emergency-red transition-all duration-300 group-hover:w-full"></span>
                  </Link>
                </li>
                <li>
                  <Link 
                    to="/police" 
                    className="text-gray-400 hover:text-white transition-all duration-300 relative group"
                  >
                    Police Emergency
                    <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-emergency-red transition-all duration-300 group-hover:w-full"></span>
                  </Link>
                </li>
              </ul>
            </div>
            
            {/* Services */}
            <div>
              <h3 className="text-lg font-semibold mb-4 text-white">Services</h3>
              <ul className="space-y-3">
                <li className="text-gray-400 hover:text-white transition-colors duration-300 cursor-pointer group">
                  <span className="group-hover:text-emergency-red transition-colors duration-300">AI-Powered Detection</span>
                </li>
                <li className="text-gray-400 hover:text-white transition-colors duration-300 cursor-pointer group">
                  <span className="group-hover:text-emergency-red transition-colors duration-300">Multi-Agent Coordination</span>
                </li>
                <li className="text-gray-400 hover:text-white transition-colors duration-300 cursor-pointer group">
                  <span className="group-hover:text-emergency-red transition-colors duration-300">Real-Time Tracking</span>
                </li>
                <li className="text-gray-400 hover:text-white transition-colors duration-300 cursor-pointer group">
                  <span className="group-hover:text-emergency-red transition-colors duration-300">24/7 Emergency Response</span>
                </li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p className="hover:text-white transition-colors duration-300">
              &copy; 2024 Emergency Response System. AI-Powered Emergency Response for Karachi.
            </p>
          </div>
        </div>
      </footer>
    </>
  )
}

export default Footer

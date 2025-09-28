import React from 'react'
import { Link } from 'react-router-dom'
import { AlertTriangle } from 'lucide-react'
import logoImage from '../assets/logo.jpeg'

interface HeaderProps {
  showAlertBanner?: boolean
}

const Header: React.FC<HeaderProps> = ({ showAlertBanner = true }) => {
  return (
    <>
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50 transition-all duration-300 hover:shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-3 group">
              <div className="w-12 h-12 rounded-lg overflow-hidden transition-all duration-300 group-hover:scale-110 group-hover:rotate-3 shadow-lg">
                <img 
                  src={logoImage} 
                  alt="Emergency Agent Logo" 
                  className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
                />
              </div>
              <span className="text-xl font-bold text-gray-900 transition-colors duration-300 group-hover:text-emergency-red">
                Emergency Response
              </span>
            </Link>
            
            {/* Navigation */}
            <nav className="hidden md:flex space-x-8">
              <Link 
                to="/" 
                className="text-gray-600 hover:text-emergency-red transition-all duration-300 relative group"
              >
                Home
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-emergency-red transition-all duration-300 group-hover:w-full"></span>
              </Link>
              <a 
                href="#about" 
                className="text-gray-600 hover:text-emergency-red transition-all duration-300 relative group"
              >
                About Us
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-emergency-red transition-all duration-300 group-hover:w-full"></span>
              </a>
              <a 
                href="#contact" 
                className="text-gray-600 hover:text-emergency-red transition-all duration-300 relative group"
              >
                Contact
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-emergency-red transition-all duration-300 group-hover:w-full"></span>
              </a>
              <Link 
                to="/hub" 
                className="text-gray-600 hover:text-emergency-red transition-all duration-300 relative group"
              >
                Report
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-emergency-red transition-all duration-300 group-hover:w-full"></span>
              </Link>
            </nav>
            
            {/* Language/Notification */}
            <div className="flex items-center space-x-2 group cursor-pointer">
              <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse group-hover:scale-125 transition-transform duration-300"></div>
              <span className="text-sm text-gray-600 group-hover:text-emergency-red transition-colors duration-300">EN</span>
            </div>
          </div>
        </div>
      </header>

      {/* Alert Banner */}
      {showAlertBanner && (
        <div className="bg-emergency-red text-white py-2 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent animate-pulse"></div>
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
            <div className="flex items-center justify-center space-x-2">
              <AlertTriangle className="w-4 h-4 animate-bounce" />
              <span className="text-sm font-medium">Emergency Alert: Stay informed and prepared for any emergency situation</span>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

export default Header

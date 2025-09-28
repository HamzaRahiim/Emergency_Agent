import React from 'react'
import { useLocation } from 'react-router-dom'
import logoImage from '../assets/logo.jpeg'


interface LayoutProps {
  children: React.ReactNode
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation()


  return (
    <div className="min-h-screen bg-gray-50 mt-0">
      {/* Main Content */}
      <main className={location.pathname === '/' ? '' : 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-8'}>
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-3 mb-4 md:mb-0">
              <div className="w-8 h-8 rounded-lg overflow-hidden shadow-md">
                <img 
                  src={logoImage} 
                  alt="Emergency Agent Logo" 
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="text-sm text-gray-500">
                © 2025 Emergency Agent System. AI-Powered Emergency Response for Karachi.
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Layout

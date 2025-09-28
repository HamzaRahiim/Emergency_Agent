import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { EmergencyProvider } from './contexts/EmergencyContext'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import MedicalEmergency from './pages/MedicalEmergency'
import FireEmergency from './pages/FireEmergency'
import PoliceEmergency from './pages/PoliceEmergency'
import MultiAgentHub from './pages/MultiAgentHub'

function App() {
  return (
    <EmergencyProvider>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/medical" element={<MedicalEmergency />} />
            <Route path="/fire" element={<FireEmergency />} />
            <Route path="/police" element={<PoliceEmergency />} />
            <Route path="/hub" element={<MultiAgentHub />} />
          </Routes>
        </Layout>
      </Router>
    </EmergencyProvider>
  )
}

export default App

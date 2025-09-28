import json
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from models.schemas import Appointment

class AppointmentAgent:
    def __init__(self):
        """Initialize appointment agent with mock data storage"""
        self.appointments_file = "data/appointments.json"
        self.appointments = self._load_appointments()
    
    def _load_appointments(self) -> Dict[str, Appointment]:
        """Load existing appointments from file"""
        try:
            with open(self.appointments_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                appointments = {}
                for appointment_id, appointment_data in data.items():
                    appointment_data['appointment_time'] = datetime.fromisoformat(appointment_data['appointment_time'])
                    appointments[appointment_id] = Appointment(**appointment_data)
                return appointments
        except FileNotFoundError:
            return {}
    
    def _save_appointments(self):
        """Save appointments to file"""
        import os
        os.makedirs(os.path.dirname(self.appointments_file), exist_ok=True)
        
        data = {}
        for appointment_id, appointment in self.appointments.items():
            appointment_dict = appointment.dict()
            appointment_dict['appointment_time'] = appointment.appointment_time.isoformat()
            data[appointment_id] = appointment_dict
        
        with open(self.appointments_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def book_appointment(self, hospital_id: str, hospital_name: str, patient_name: str, 
                        speciality: str = None, urgency: str = "medium") -> Appointment:
        """Book an appointment at a hospital"""
        appointment_id = str(uuid.uuid4())
        
        # Calculate appointment time based on urgency
        now = datetime.now()
        if urgency == "critical":
            appointment_time = now + timedelta(hours=1)  # ASAP
        elif urgency == "high":
            appointment_time = now + timedelta(hours=4)  # Same day
        elif urgency == "medium":
            appointment_time = now + timedelta(days=1)   # Next day
        else:
            appointment_time = now + timedelta(days=3)   # Within few days
        
        # Mock doctor assignment based on speciality
        doctor_name = self._get_available_doctor(speciality)
        
        appointment = Appointment(
            appointment_id=appointment_id,
            hospital_id=hospital_id,
            hospital_name=hospital_name,
            patient_name=patient_name,
            appointment_time=appointment_time,
            doctor_name=doctor_name,
            speciality=speciality,
            status="scheduled"
        )
        
        self.appointments[appointment_id] = appointment
        self._save_appointments()
        
        return appointment
    
    def _get_available_doctor(self, speciality: str = None) -> str:
        """Mock function to get available doctor"""
        doctors = {
            "cardiology": ["Dr. Ahmed Khan", "Dr. Sara Ali"],
            "dentistry": ["Dr. Mohammad Hassan", "Dr. Fatima Khan"],
            "nephrology": ["Dr. Amanullah Khan", "Dr. Ayesha Malik"],
            "pediatrics": ["Dr. Hassan Sheikh", "Dr. Zara Ahmed"],
            "gynecology": ["Dr. Maryam Khan", "Dr. Farah Ali"],
            "general": ["Dr. Ali Raza", "Dr. Sana Khan", "Dr. Usman Ahmed"]
        }
        
        if speciality and speciality in doctors:
            import random
            return random.choice(doctors[speciality])
        else:
            import random
            return random.choice(doctors["general"])
    
    def get_patient_appointments(self, patient_name: str) -> List[Appointment]:
        """Get all appointments for a patient"""
        return [apt for apt in self.appointments.values() 
                if apt.patient_name.lower() == patient_name.lower()]
    
    def cancel_appointment(self, appointment_id: str) -> bool:
        """Cancel an appointment"""
        if appointment_id in self.appointments:
            self.appointments[appointment_id].status = "cancelled"
            self._save_appointments()
            return True
        return False
    
    def update_appointment_status(self, appointment_id: str, status: str) -> bool:
        """Update appointment status"""
        if appointment_id in self.appointments:
            self.appointments[appointment_id].status = status
            self._save_appointments()
            return True
        return False
    
    def get_appointment(self, appointment_id: str) -> Optional[Appointment]:
        """Get specific appointment by ID"""
        return self.appointments.get(appointment_id)


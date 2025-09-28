import httpx
from typing import Optional, Dict, Any
import json

class IPLocationService:
    def __init__(self):
        """Initialize IP-based location service"""
        self.ip_api_url = "http://ip-api.com/json/"
        self.fallback_location = {
            "latitude": 24.8607,
            "longitude": 67.0011,
            "address": "Karachi, Pakistan",
            "city": "Karachi",
            "region": "Sindh",
            "country": "Pakistan"
        }
    
    async def get_location_from_ip(self, ip_address: str = None) -> Dict[str, Any]:
        """
        Get location from IP address
        """
        try:
            # Use provided IP or get from request
            url = f"{self.ip_api_url}{ip_address}" if ip_address else self.ip_api_url
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=5.0)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("status") == "success":
                        return {
                            "latitude": float(data.get("lat", 24.8607)),
                            "longitude": float(data.get("lon", 67.0011)),
                            "address": f"{data.get('city', 'Karachi')}, {data.get('country', 'Pakistan')}",
                            "city": data.get("city", "Karachi"),
                            "region": data.get("regionName", "Sindh"),
                            "country": data.get("country", "Pakistan"),
                            "source": "ip"
                        }
                
        except Exception as e:
            print(f"IP location service error: {e}")
        
        # Return Karachi fallback
        return {
            **self.fallback_location,
            "source": "fallback"
        }
    
    def is_karachi_location(self, location_data: Dict[str, Any]) -> bool:
        """Check if location is in Karachi area"""
        city = location_data.get("city", "").lower()
        country = location_data.get("country", "").lower()
        
        # Check if it's in Karachi or Pakistan
        return "karachi" in city or "pakistan" in country or location_data.get("source") == "fallback"
    
    def get_karachi_coordinates(self, area_name: str = None) -> Dict[str, Any]:
        """Get specific Karachi area coordinates"""
        karachi_areas = {
            'saddar': {"lat": 24.8607, "lon": 67.0011, "address": "Saddar, Karachi"},
            'clifton': {"lat": 24.8123, "lon": 66.9967, "address": "Clifton, Karachi"},
            'defence': {"lat": 24.8047, "lon": 67.0281, "address": "Defence Housing Authority, Karachi"},
            'gulshan': {"lat": 24.8918, "lon": 67.0281, "address": "Gulshan-e-Iqbal, Karachi"},
            'north nazimabad': {"lat": 24.9056, "lon": 67.0822, "address": "North Nazimabad, Karachi"},
            'federal b area': {"lat": 24.9142, "lon": 67.0810, "address": "Federal B Area, Karachi"},
            'pecs': {"lat": 24.8738, "lon": 67.0378, "address": "PECHS, Karachi"},
            'gulberg': {"lat": 24.9167, "lon": 67.0667, "address": "Gulberg, Karachi"},
            'malir': {"lat": 24.9000, "lon": 67.1000, "address": "Malir, Karachi"},
            'korangi': {"lat": 24.8500, "lon": 67.0833, "address": "Korangi, Karachi"}
        }
        
        if area_name and area_name.lower() in karachi_areas:
            area = karachi_areas[area_name.lower()]
            return {
                "latitude": area["lat"],
                "longitude": area["lon"],
                "address": area["address"],
                "source": "karachi_area"
            }
        
        # Default to Saddar
        return {
            "latitude": 24.8607,
            "longitude": 67.0011,
            "address": "Saddar, Karachi",
            "source": "karachi_default"
        }


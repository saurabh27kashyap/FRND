"""
In-Memory Database Manager for Hotel Room Booking Platform
Simulates database operations with optimized data structures
"""

from typing import Dict, List
import random
from datetime import date, timedelta

from models import Hotel, Room, Booking, RoomType

class DatabaseManager:
    """In-memory database with optimized data structures"""
    
    def __init__(self):
        # Primary data stores
        self.hotels: Dict[str, Hotel] = {}
        self.rooms: Dict[str, Room] = {}
        self.bookings: Dict[str, Booking] = {}
        
        # Initialize with some sample data
        self._create_initial_data()
    
    def _create_initial_data(self):
        """Create initial sample data with realistic hotels"""
        
        # Famous hotel chains and boutique hotels
        hotel_data = [
            # Mumbai Hotels
            {"name": "The Taj Mahal Palace Mumbai", "city": "Mumbai", "address": "Apollo Bunder, Colaba", "rating": 5, 
             "description": "Iconic luxury hotel overlooking the Gateway of India", 
             "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Bar", "Valet Parking", "Concierge", "Business Center"]},
            {"name": "The Oberoi Mumbai", "city": "Mumbai", "address": "Nariman Point", "rating": 5,
             "description": "Luxury hotel with stunning views of Marine Drive",
             "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Bar", "Gym", "Business Center"]},
            {"name": "ITC Grand Central Mumbai", "city": "Mumbai", "address": "Parel", "rating": 5,
             "description": "Contemporary luxury hotel in the heart of Mumbai",
             "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Bar", "Gym", "Parking"]},
            
            # Delhi Hotels  
            {"name": "The Imperial New Delhi", "city": "Delhi", "address": "Janpath", "rating": 5,
             "description": "Heritage luxury hotel in the heart of New Delhi",
             "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Bar", "Gym", "Valet Parking", "Concierge"]},
            {"name": "The Leela Palace New Delhi", "city": "Delhi", "address": "Chanakyapuri", "rating": 5,
             "description": "Opulent palace hotel with world-class amenities",
             "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Bar", "Gym", "Business Center", "Parking"]},
            {"name": "Shangri-La Eros New Delhi", "city": "Delhi", "address": "Connaught Place", "rating": 5,
             "description": "Luxury hotel in the commercial heart of Delhi",
             "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Bar", "Gym", "Business Center"]},
            
            # Bangalore Hotels
            {"name": "The Ritz-Carlton Bangalore", "city": "Bangalore", "address": "Residency Road", "rating": 5,
             "description": "Sophisticated luxury hotel in the Garden City",
             "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Bar", "Gym", "Business Center", "Parking"]},
            {"name": "ITC Gardenia Bangalore", "city": "Bangalore", "address": "Residency Road", "rating": 5,
             "description": "Eco-friendly luxury hotel with lush gardens",
             "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Bar", "Gym", "Parking", "Garden"]},
            {"name": "The Oberoi Bangalore", "city": "Bangalore", "address": "MG Road", "rating": 5,
             "description": "Contemporary luxury in the heart of Bangalore",
             "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Bar", "Gym", "Business Center"]},
            
            # Goa Hotels
            {"name": "Taj Exotica Resort & Spa Goa", "city": "Goa", "address": "Benaulim Beach", "rating": 5,
             "description": "Beachfront luxury resort with pristine beaches",
             "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Bar", "Beach Access", "Water Sports", "Parking"]},
            {"name": "The Leela Goa", "city": "Goa", "address": "Cavelossim Beach", "rating": 5,
             "description": "Palatial beachfront resort with lagoon views",
             "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Bar", "Beach Access", "Golf Course", "Parking"]},
            {"name": "Grand Hyatt Goa", "city": "Goa", "address": "Bambolim", "rating": 5,
             "description": "Contemporary resort with panoramic views",
             "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Bar", "Gym", "Beach Access", "Parking"]},
            
            # Chennai Hotels
            {"name": "ITC Grand Chola Chennai", "city": "Chennai", "address": "Guindy", "rating": 5,
             "description": "Magnificent luxury hotel inspired by Chola architecture",
             "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Bar", "Gym", "Business Center", "Parking"]},
            {"name": "The Leela Palace Chennai", "city": "Chennai", "address": "Adyar", "rating": 5,
             "description": "Elegant hotel overlooking the Bay of Bengal",
             "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Bar", "Gym", "Beach Access", "Parking"]},
            
            # Jaipur Hotels
            {"name": "Rambagh Palace Jaipur", "city": "Jaipur", "address": "Bhawani Singh Road", "rating": 5,
             "description": "Former royal palace turned luxury hotel",
             "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Bar", "Gym", "Heritage Tours", "Parking"]},
            {"name": "The Oberoi Rajvilas Jaipur", "city": "Jaipur", "address": "Goner Road", "rating": 5,
             "description": "Luxury resort with traditional Rajasthani architecture",
             "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Bar", "Gym", "Cultural Shows", "Parking"]},
            
            # Mid-range and Budget Hotels
            {"name": "Hotel Sahara Star Mumbai", "city": "Mumbai", "address": "Vile Parle East", "rating": 4,
             "description": "Contemporary hotel near the airport",
             "amenities": ["WiFi", "Pool", "Restaurant", "Bar", "Gym", "Airport Shuttle", "Parking"]},
            {"name": "The Park Delhi", "city": "Delhi", "address": "Sansad Marg", "rating": 4,
             "description": "Boutique hotel with modern design",
             "amenities": ["WiFi", "Pool", "Restaurant", "Bar", "Gym", "Business Center"]},
            {"name": "Vivanta Bangalore", "city": "Bangalore", "address": "MG Road", "rating": 4,
             "description": "Stylish hotel in the business district",
             "amenities": ["WiFi", "Pool", "Restaurant", "Bar", "Gym", "Business Center", "Parking"]},
            {"name": "Novotel Goa Resort", "city": "Goa", "address": "Candolim Beach", "rating": 4,
             "description": "Beachfront resort with family-friendly amenities",
             "amenities": ["WiFi", "Pool", "Restaurant", "Bar", "Beach Access", "Kids Club", "Parking"]},
        ]
        
        # Create hotels from the enhanced data
        for hotel_info in hotel_data:
            hotel = Hotel(
                name=hotel_info["name"],
                city=hotel_info["city"],
                address=hotel_info["address"],
                star_rating=hotel_info["rating"],
                description=hotel_info["description"],
                amenities=hotel_info["amenities"]
            )
            
            # Add realistic room distribution based on hotel type
            if hotel_info["rating"] == 5:
                # Luxury hotels - fewer rooms, higher prices
                room_count = random.randint(50, 150)
                base_price = random.randint(8000, 25000)
            else:
                # Mid-range hotels - more rooms, moderate prices
                room_count = random.randint(80, 200)
                base_price = random.randint(3000, 12000)
            
            # Create rooms with realistic pricing tiers
            for j in range(room_count):
                room_type = random.choice(list(RoomType))
                
                # Price multiplier based on room type
                price_multiplier = {
                    RoomType.SINGLE: 1.0,
                    RoomType.DOUBLE: 1.3,
                    RoomType.DELUXE: 1.8,
                    RoomType.SUITE: 2.5
                }
                
                room_price = int(base_price * price_multiplier[room_type])
                
                # Room amenities based on hotel rating
                if hotel_info["rating"] == 5:
                    room_amenities = random.sample([
                        "AC", "Smart TV", "Mini Bar", "Balcony", "City View", "Sea View", 
                        "Mountain View", "WiFi", "Safe", "Coffee Machine", "Butler Service"
                    ], random.randint(5, 8))
                else:
                    room_amenities = random.sample([
                        "AC", "TV", "Mini Bar", "Balcony", "City View", "WiFi", "Safe", "Tea/Coffee"
                    ], random.randint(3, 6))
                
                room = Room(
                    hotel_id=hotel.id,
                    room_number=f"{random.randint(1, 10)}{j+1:02d}",
                    room_type=room_type,
                    price=room_price,
                    max_occupancy=2 if room_type == RoomType.SINGLE else random.randint(2, 4),
                    amenities=room_amenities
                )
                hotel.rooms.append(room)
                self.rooms[room.id] = room
            
            self.hotels[hotel.id] = hotel
        
        print(f"Created {len(self.hotels)} hotels with realistic dummy data")
    
    def generate_sample_data(self, count: int = 1000):
        """Generate large dataset for performance testing"""
        cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", 
                 "Pune", "Ahmedabad", "Jaipur", "Goa", "Kochi", "Lucknow", "Indore",
                 "Bhopal", "Visakhapatnam", "Vadodara", "Ludhiana", "Agra", "Nashik", "Faridabad"]
        
        hotel_prefixes = ["Grand", "Royal", "Luxury", "Premium", "Elite", "Imperial", 
                         "Majestic", "Regal", "Supreme", "Deluxe", "Platinum", "Golden"]
        
        hotel_suffixes = ["Palace", "Inn", "Resort", "Lodge", "Hotel", "Suites", 
                         "Manor", "Plaza", "Tower", "Gardens", "Heights", "Vista"]
        
        # Clear existing data except initial sample
        initial_count = len(self.hotels)
        
        for i in range(count - initial_count):
            city = random.choice(cities)
            prefix = random.choice(hotel_prefixes)
            suffix = random.choice(hotel_suffixes)
            name = f"{prefix} {suffix} {city}"
            
            hotel = Hotel(
                name=name,
                city=city,
                address=f"{random.randint(1, 999)} {random.choice(['MG Road', 'Park Street', 'Main Street', 'Commercial Street', 'Ring Road'])}",
                star_rating=random.randint(2, 5),
                description=f"A comfortable {random.randint(2, 5)}-star accommodation in {city}",
                amenities=random.sample(["WiFi", "Pool", "Gym", "Spa", "Restaurant", "Bar", 
                                       "Parking", "Conference Room", "Laundry", "Room Service"], 
                                      random.randint(3, 7))
            )
            
            # Add rooms
            room_count = random.randint(5, 30)
            for j in range(room_count):
                room = Room(
                    hotel_id=hotel.id,
                    room_number=f"{random.randint(1, 5)}{j+1:02d}",
                    room_type=random.choice(list(RoomType)),
                    price=random.randint(1500, 20000),
                    max_occupancy=random.randint(1, 6),
                    amenities=random.sample(["AC", "TV", "Mini Bar", "Balcony", "City View", 
                                           "Sea View", "Mountain View", "WiFi", "Safe"], 
                                          random.randint(2, 5))
                )
                hotel.rooms.append(room)
                self.rooms[room.id] = room
            
            self.hotels[hotel.id] = hotel
        
        print(f"Generated {len(self.hotels)} hotels with {len(self.rooms)} rooms total")

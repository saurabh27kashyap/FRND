"""
Data Models for Hotel Room Booking Platform
Clean data structures with proper validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime
from enum import Enum
import uuid

class RoomType(str, Enum):
    """Room type enumeration"""
    SINGLE = "Single"
    DOUBLE = "Double"
    SUITE = "Suite"
    DELUXE = "Deluxe"

class BookingStatus(str, Enum):
    """Booking status enumeration"""
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    PENDING = "pending"

class Room(BaseModel):
    """Room model with availability and pricing"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    hotel_id: str
    room_number: str
    room_type: RoomType
    price: float = Field(gt=0, description="Price per night")
    is_available: bool = True
    max_occupancy: int = Field(gt=0, le=10)
    amenities: List[str] = []
    
    class Config:
        use_enum_values = True

class Hotel(BaseModel):
    """Hotel model with location and room management"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(min_length=1, max_length=200)
    city: str = Field(min_length=1, max_length=100)
    address: str = ""
    star_rating: int = Field(ge=1, le=5, default=3)
    description: str = ""
    amenities: List[str] = []
    rooms: List[Room] = []
    
    def add_room(self, room: Room):
        """Add a room to the hotel"""
        room.hotel_id = self.id
        self.rooms.append(room)

class Booking(BaseModel):
    """Booking model with date validation"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    room_id: str
    hotel_id: str
    guest_name: str = Field(min_length=1, max_length=100)
    guest_email: str = Field(pattern=r'^[^@]+@[^@]+\.[^@]+$')
    check_in_date: date
    check_out_date: date
    total_price: float = Field(gt=0)
    status: BookingStatus = BookingStatus.CONFIRMED
    created_at: datetime = Field(default_factory=datetime.now)
    
    def validate_dates(self):
        """Validate booking dates"""
        if self.check_in_date >= self.check_out_date:
            raise ValueError("Check-out date must be after check-in date")
        if self.check_in_date < date.today():
            raise ValueError("Check-in date cannot be in the past")

class BookingRequest(BaseModel):
    """Request model for creating bookings"""
    room_id: str
    guest_name: str = Field(min_length=1, max_length=100)
    guest_email: str = Field(pattern=r'^[^@]+@[^@]+\.[^@]+$')
    check_in_date: date
    check_out_date: date

class SearchRequest(BaseModel):
    """Request model for hotel search"""
    city: Optional[str] = None
    hotel_name: Optional[str] = None
    limit: int = Field(default=50, le=1000)
    
    def validate_search_criteria(self):
        """Validate that at least one search criterion is provided"""
        if not self.city and not self.hotel_name:
            raise ValueError("At least one search criterion (city or hotel_name) must be provided")

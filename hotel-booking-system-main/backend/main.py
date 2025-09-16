"""
Hotel Room Booking Platform - Main FastAPI Application
Clean Architecture Implementation with Separation of Concerns
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from typing import List, Optional
from datetime import datetime, date
import threading
import time

from models import Hotel, Room, Booking, BookingRequest, SearchRequest
from services import HotelService, BookingService, SearchService
from database import DatabaseManager

# Global services
hotel_service = HotelService()
booking_service = BookingService()
search_service = SearchService()
db_manager = DatabaseManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application with sample data"""
    # Generate sample data for testing
    db_manager.generate_sample_data(1000)  # Generate 1000 hotels for testing
    yield

app = FastAPI(
    title="Hotel Room Booking Platform",
    description="Professional hotel booking system with clean architecture",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}

# Hotel endpoints
@app.get("/api/hotels", response_model=List[Hotel])
async def get_hotels(skip: int = 0, limit: int = 100):
    """Get all hotels with pagination"""
    return hotel_service.get_hotels(skip=skip, limit=limit)

@app.get("/api/hotels/{hotel_id}", response_model=Hotel)
async def get_hotel(hotel_id: str):
    """Get specific hotel by ID"""
    hotel = hotel_service.get_hotel_by_id(hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel

@app.post("/api/hotels", response_model=Hotel)
async def create_hotel(hotel: Hotel):
    """Create a new hotel"""
    return hotel_service.create_hotel(hotel)

# Room endpoints
@app.get("/api/hotels/{hotel_id}/rooms", response_model=List[Room])
async def get_hotel_rooms(hotel_id: str):
    """Get all rooms for a specific hotel"""
    rooms = hotel_service.get_hotel_rooms(hotel_id)
    if not rooms:
        raise HTTPException(status_code=404, detail="Hotel not found or no rooms available")
    return rooms

@app.get("/api/rooms/{room_id}", response_model=Room)
async def get_room(room_id: str):
    """Get specific room by ID"""
    room = hotel_service.get_room_by_id(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

# Search endpoints
@app.post("/api/search", response_model=List[Hotel])
async def search_hotels(search_request: SearchRequest):
    """Search hotels by city and/or name with performance optimization"""
    return search_service.search_hotels(
        city=search_request.city,
        hotel_name=search_request.hotel_name,
        limit=search_request.limit
    )

# Booking endpoints
@app.post("/api/bookings", response_model=Booking)
async def create_booking(booking_request: BookingRequest):
    """Create a new booking with double-booking prevention"""
    try:
        booking = booking_service.create_booking(booking_request)
        return booking
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/bookings", response_model=List[Booking])
async def get_bookings(guest_name: Optional[str] = None):
    """Get all bookings, optionally filtered by guest name"""
    return booking_service.get_bookings(guest_name=guest_name)

@app.get("/api/bookings/{booking_id}", response_model=Booking)
async def get_booking(booking_id: str):
    """Get specific booking by ID"""
    booking = booking_service.get_booking_by_id(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@app.delete("/api/bookings/{booking_id}")
async def cancel_booking(booking_id: str):
    """Cancel a booking"""
    success = booking_service.cancel_booking(booking_id)
    if not success:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Booking cancelled successfully"}

# Performance testing endpoint
@app.get("/api/performance/search")
async def performance_test_search():
    """Test search performance with large dataset"""
    start_time = time.time()
    results = search_service.search_hotels(city="Mumbai", limit=100)
    end_time = time.time()
    
    return {
        "results_count": len(results),
        "execution_time_ms": round((end_time - start_time) * 1000, 2),
        "total_hotels_in_db": len(db_manager.hotels)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

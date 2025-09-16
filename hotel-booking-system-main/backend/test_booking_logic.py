"""
Unit Tests for Hotel Booking Platform Backend
Tests core business logic and edge cases
"""

import pytest
import asyncio
from datetime import date, timedelta
import threading
import time

from models import Hotel, Room, Booking, BookingRequest, RoomType
from services import HotelService, BookingService, SearchService
from database import DatabaseManager

class TestHotelService:
    def setup_method(self):
        """Setup test data"""
        self.hotel_service = HotelService()
        self.db = self.hotel_service.db
        
        # Clear existing data
        self.db.hotels.clear()
        self.db.rooms.clear()
        
        # Create test hotel
        self.test_hotel = Hotel(
            name="Test Hotel",
            city="Mumbai",
            address="Test Address",
            star_rating=4,
            description="Test hotel for unit testing"
        )
        
        # Add test rooms
        self.test_room = Room(
            hotel_id=self.test_hotel.id,
            room_number="101",
            room_type=RoomType.SINGLE,
            price=5000,
            max_occupancy=2
        )
        
        self.test_hotel.rooms.append(self.test_room)
        self.db.hotels[self.test_hotel.id] = self.test_hotel
        self.db.rooms[self.test_room.id] = self.test_room
    
    def test_create_hotel(self):
        """Test hotel creation"""
        new_hotel = Hotel(
            name="New Test Hotel",
            city="Delhi",
            address="New Address",
            star_rating=5
        )
        
        created_hotel = self.hotel_service.create_hotel(new_hotel)
        
        assert created_hotel.id == new_hotel.id
        assert created_hotel.name == "New Test Hotel"
        assert created_hotel.city == "Delhi"
        assert self.db.hotels[new_hotel.id] == new_hotel
    
    def test_get_hotel_by_id(self):
        """Test retrieving hotel by ID"""
        retrieved_hotel = self.hotel_service.get_hotel_by_id(self.test_hotel.id)
        
        assert retrieved_hotel is not None
        assert retrieved_hotel.name == "Test Hotel"
        assert retrieved_hotel.city == "Mumbai"
    
    def test_get_nonexistent_hotel(self):
        """Test retrieving non-existent hotel"""
        retrieved_hotel = self.hotel_service.get_hotel_by_id("nonexistent-id")
        assert retrieved_hotel is None
    
    def test_get_hotel_rooms(self):
        """Test retrieving hotel rooms"""
        rooms = self.hotel_service.get_hotel_rooms(self.test_hotel.id)
        
        assert len(rooms) == 1
        assert rooms[0].room_number == "101"
        assert rooms[0].room_type == RoomType.SINGLE

class TestSearchService:
    def setup_method(self):
        """Setup test data"""
        self.search_service = SearchService()
        self.db = self.search_service.db
        
        # Clear existing data
        self.db.hotels.clear()
        
        # Create test hotels
        self.mumbai_hotel = Hotel(
            name="Mumbai Grand Hotel",
            city="Mumbai",
            address="Mumbai Address"
        )
        
        self.delhi_hotel = Hotel(
            name="Delhi Palace Hotel",
            city="Delhi", 
            address="Delhi Address"
        )
        
        self.royal_hotel = Hotel(
            name="Royal Mumbai Resort",
            city="Mumbai",
            address="Royal Address"
        )
        
        # Add to database
        for hotel in [self.mumbai_hotel, self.delhi_hotel, self.royal_hotel]:
            self.db.hotels[hotel.id] = hotel
        
        # Rebuild search indexes
        self.search_service.rebuild_indexes()
    
    def test_search_by_city(self):
        """Test searching hotels by city"""
        results = self.search_service.search_hotels(city="Mumbai")
        
        assert len(results) == 2
        hotel_names = [hotel.name for hotel in results]
        assert "Mumbai Grand Hotel" in hotel_names
        assert "Royal Mumbai Resort" in hotel_names
    
    def test_search_by_hotel_name(self):
        """Test searching hotels by name"""
        results = self.search_service.search_hotels(hotel_name="Royal")
        
        assert len(results) == 1
        assert results[0].name == "Royal Mumbai Resort"
    
    def test_search_by_city_and_name(self):
        """Test searching by both city and hotel name"""
        results = self.search_service.search_hotels(city="Mumbai", hotel_name="Grand")
        
        assert len(results) == 1
        assert results[0].name == "Mumbai Grand Hotel"
    
    def test_search_case_insensitive(self):
        """Test case-insensitive search"""
        results = self.search_service.search_hotels(city="mumbai")
        assert len(results) == 2
        
        results = self.search_service.search_hotels(hotel_name="ROYAL")
        assert len(results) == 1
    
    def test_search_with_limit(self):
        """Test search with result limit"""
        results = self.search_service.search_hotels(city="Mumbai", limit=1)
        assert len(results) == 1

class TestBookingService:
    def setup_method(self):
        """Setup test data"""
        self.booking_service = BookingService()
        self.db = self.booking_service.db
        
        # Clear existing data
        self.db.hotels.clear()
        self.db.rooms.clear()
        self.db.bookings.clear()
        
        # Create test hotel and room
        self.test_hotel = Hotel(
            name="Booking Test Hotel",
            city="Chennai",
            address="Test Address"
        )
        
        self.test_room = Room(
            hotel_id=self.test_hotel.id,
            room_number="201",
            room_type=RoomType.DOUBLE,
            price=8000,
            max_occupancy=4
        )
        
        self.test_hotel.rooms.append(self.test_room)
        self.db.hotels[self.test_hotel.id] = self.test_hotel
        self.db.rooms[self.test_room.id] = self.test_room
    
    def test_create_valid_booking(self):
        """Test creating a valid booking"""
        booking_request = BookingRequest(
            room_id=self.test_room.id,
            guest_name="Test Guest",
            guest_email="test@example.com",
            check_in_date=date.today() + timedelta(days=1),
            check_out_date=date.today() + timedelta(days=3)
        )
        
        booking = self.booking_service.create_booking(booking_request)
        
        assert booking.room_id == self.test_room.id
        assert booking.guest_name == "Test Guest"
        assert booking.total_price == 16000  # 2 nights * 8000
        assert booking.id in self.db.bookings
    
    def test_booking_nonexistent_room(self):
        """Test booking non-existent room"""
        booking_request = BookingRequest(
            room_id="nonexistent-room",
            guest_name="Test Guest",
            guest_email="test@example.com",
            check_in_date=date.today() + timedelta(days=1),
            check_out_date=date.today() + timedelta(days=3)
        )
        
        with pytest.raises(ValueError, match="Room not found"):
            self.booking_service.create_booking(booking_request)
    
    def test_booking_invalid_dates(self):
        """Test booking with invalid dates: check-in after check-out should fail"""
        # Check-in after check-out
        booking_request = BookingRequest(
            room_id=self.test_room.id,
            guest_name="Test Guest",
            guest_email="test@example.com",
            check_in_date=date.today() + timedelta(days=3),
            check_out_date=date.today() + timedelta(days=1)
        )
        
        with pytest.raises(ValueError, match="after or same as check-in"):
            self.booking_service.create_booking(booking_request)
    
    def test_booking_past_date(self):
        """Test booking with past date"""
        booking_request = BookingRequest(
            room_id=self.test_room.id,
            guest_name="Test Guest",
            guest_email="test@example.com",
            check_in_date=date.today() - timedelta(days=1),
            check_out_date=date.today() + timedelta(days=1)
        )
        
        with pytest.raises(ValueError, match="Check-in date cannot be in the past"):
            self.booking_service.create_booking(booking_request)
    
    def test_double_booking_prevention(self):
        """Test prevention of double booking"""
        # Create first booking
        booking_request_1 = BookingRequest(
            room_id=self.test_room.id,
            guest_name="Guest 1",
            guest_email="guest1@example.com",
            check_in_date=date.today() + timedelta(days=1),
            check_out_date=date.today() + timedelta(days=3)
        )
        
        booking_1 = self.booking_service.create_booking(booking_request_1)
        assert booking_1 is not None
        
        # Try to create overlapping booking
        booking_request_2 = BookingRequest(
            room_id=self.test_room.id,
            guest_name="Guest 2",
            guest_email="guest2@example.com",
            check_in_date=date.today() + timedelta(days=2),  # Overlaps with first booking
            check_out_date=date.today() + timedelta(days=4)
        )
        
        with pytest.raises(ValueError, match="Room is not available for the selected dates"):
            self.booking_service.create_booking(booking_request_2)
    
    def test_concurrent_booking_prevention(self):
        """Test prevention of concurrent bookings using threading"""
        booking_results = []
        exceptions = []
        
        def make_booking(guest_num):
            try:
                booking_request = BookingRequest(
                    room_id=self.test_room.id,
                    guest_name=f"Concurrent Guest {guest_num}",
                    guest_email=f"guest{guest_num}@example.com",
                    check_in_date=date.today() + timedelta(days=5),
                    check_out_date=date.today() + timedelta(days=7)
                )
                
                booking = self.booking_service.create_booking(booking_request)
                booking_results.append(booking)
            except Exception as e:
                exceptions.append(e)
        
        # Create multiple threads trying to book the same room simultaneously
        threads = []
        for i in range(5):
            thread = threading.Thread(target=make_booking, args=(i,))
            threads.append(thread)
        
        # Start all threads simultaneously
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Only one booking should succeed
        assert len(booking_results) == 1
        assert len(exceptions) == 4
        
        # All exceptions should be about room availability
        for exception in exceptions:
            assert "Room is not available" in str(exception)
    
    def test_cancel_booking(self):
        """Test booking cancellation"""
        # Create a booking
        booking_request = BookingRequest(
            room_id=self.test_room.id,
            guest_name="Cancellation Test",
            guest_email="cancel@example.com",
            check_in_date=date.today() + timedelta(days=10),
            check_out_date=date.today() + timedelta(days=12)
        )
        
        booking = self.booking_service.create_booking(booking_request)
        
        # Cancel the booking
        success = self.booking_service.cancel_booking(booking.id)
        assert success is True
        
        # Check that booking status is updated
        cancelled_booking = self.db.bookings[booking.id]
        assert cancelled_booking.status == "cancelled"

    def test_booking_same_day_allowed_and_charged_min_one_night(self):
        """Same-day check-in/out should be allowed and charged as 1 night"""
        booking_request = BookingRequest(
            room_id=self.test_room.id,
            guest_name="Edge Guest",
            guest_email="edge@example.com",
            check_in_date=date.today() + timedelta(days=1),
            check_out_date=date.today() + timedelta(days=1)
        )
        booking = self.booking_service.create_booking(booking_request)
        assert booking is not None
        assert booking.total_price == self.test_room.price  # 1 night minimum

def test_assignment3_simultaneous_booking_overlap():
    """Assignment 3: Simultaneous Booking - overlapping dates should fail for second booking"""
    booking_service = BookingService()
    db = booking_service.db
    db.hotels.clear()
    db.rooms.clear()
    db.bookings.clear()

    # Setup: Create a hotel and a room
    hotel = Hotel(name="Oceanview", city="Goa")
    room = Room(hotel_id=hotel.id, room_number="301", room_type=RoomType.SINGLE, price=1000, max_occupancy=1)
    hotel.rooms.append(room)
    db.hotels[hotel.id] = hotel
    db.rooms[room.id] = room

    # Use future-relative dates to avoid past date validation
    from datetime import timedelta
    base = date.today() + timedelta(days=365)  # one year in the future
    start1 = base.replace(day=min(2, 28))  # safe day selection
    end1 = base.replace(day=min(4, 28))
    start2 = base.replace(day=min(3, 28))
    end2 = base.replace(day=min(4, 28))

    # Booking 1
    booking1 = booking_service.create_booking(BookingRequest(
        room_id=room.id,
        guest_name="Alice",
        guest_email="alice@example.com",
        check_in_date=start1,
        check_out_date=end1
    ))
    assert booking1 is not None

    # Booking 2: overlapping should fail
    with pytest.raises(ValueError, match="Room is not available"):
        booking_service.create_booking(BookingRequest(
            room_id=room.id,
            guest_name="Bob",
            guest_email="bob@example.com",
            check_in_date=start2,
            check_out_date=end2
        ))


def test_assignment4_search_by_city_and_hotel_name():
    """Assignment 4: Search by city and hotel name should each return 1 result"""
    search_service = SearchService()
    db = search_service.db
    db.hotels.clear()

    hotel1 = Hotel(name="Oceanview", city="Goa")
    hotel2 = Hotel(name="Mountain Inn", city="Shimla")
    db.hotels[hotel1.id] = hotel1
    db.hotels[hotel2.id] = hotel2

    # Rebuild indexes after data changes
    search_service.rebuild_indexes()

    result_by_city = search_service.search_hotels(city="Goa")
    result_by_name = search_service.search_hotels(hotel_name="Oceanview")

    assert len(result_by_city) == 1, "Search by city should return 1 result"
    assert len(result_by_name) == 1, "Search by name should return 1 result"

def run_tests():
    """Run all unit tests"""
    print("🧪 Running Unit Tests for Hotel Booking Platform")
    print("=" * 60)
    
    # Run pytest programmatically
    import subprocess
    import sys
    
    result = subprocess.run([
        sys.executable, "-m", "pytest", __file__, "-v", "--tb=short"
    ], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0

if __name__ == "__main__":
    success = run_tests()
    if not success:
        print("❌ Some tests failed")
        exit(1)
    else:
        print("✅ All tests passed!")

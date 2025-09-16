"""
Business Logic Services for Hotel Room Booking Platform
Clean separation of concerns with proper error handling
"""

from typing import List, Optional
from datetime import date, datetime, timedelta
import threading
from collections import defaultdict

from models import Hotel, Room, Booking, BookingRequest, RoomType, BookingStatus
from database import DatabaseManager

class HotelService:
    """Service for hotel and room management"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def get_hotels(self, skip: int = 0, limit: int = 100) -> List[Hotel]:
        """Get hotels with pagination"""
        hotels = list(self.db.hotels.values())
        return hotels[skip:skip + limit]
    
    def get_hotel_by_id(self, hotel_id: str) -> Optional[Hotel]:
        """Get hotel by ID"""
        return self.db.hotels.get(hotel_id)
    
    def create_hotel(self, hotel: Hotel) -> Hotel:
        """Create a new hotel"""
        self.db.hotels[hotel.id] = hotel
        return hotel
    
    def get_hotel_rooms(self, hotel_id: str) -> List[Room]:
        """Get all rooms for a hotel"""
        hotel = self.db.hotels.get(hotel_id)
        return hotel.rooms if hotel else []
    
    def get_room_by_id(self, room_id: str) -> Optional[Room]:
        """Get room by ID"""
        return self.db.rooms.get(room_id)

class SearchService:
    """Service for hotel search with performance optimization"""
    
    def __init__(self):
        self.db = DatabaseManager()
        # Create indexes for fast searching
        self._city_index = defaultdict(list)
        self._name_index = defaultdict(list)
        # Simple in-memory cache: key -> (results, expires_at)
        self._cache = {}
        self._cache_ttl = timedelta(seconds=60)
        self._build_indexes()
    
    def _build_indexes(self):
        """Build search indexes for performance"""
        for hotel in self.db.hotels.values():
            # City index (case-insensitive)
            city_key = hotel.city.lower()
            self._city_index[city_key].append(hotel)
            
            # Name index (case-insensitive, partial matching)
            name_words = hotel.name.lower().split()
            for word in name_words:
                self._name_index[word].append(hotel)
    
    def _cache_key(self, city: Optional[str], hotel_name: Optional[str], limit: int) -> str:
        return f"city={city or ''}|name={hotel_name or ''}|limit={limit}"
    
    def _get_cached(self, key: str):
        entry = self._cache.get(key)
        if not entry:
            return None
        results, expires_at = entry
        if datetime.utcnow() > expires_at:
            # Expired
            self._cache.pop(key, None)
            return None
        return results
    
    def _set_cache(self, key: str, results: List[Hotel]):
        self._cache[key] = (results, datetime.utcnow() + self._cache_ttl)
    
    def search_hotels(self, city: Optional[str] = None, 
                     hotel_name: Optional[str] = None, 
                     limit: int = 50) -> List[Hotel]:
        """
        Search hotels with optimized performance for large datasets
        Uses indexed search for O(1) city lookup and O(k) name matching
        Caching: caches results for identical queries for a short TTL
        """
        cache_key = self._cache_key(city, hotel_name, limit)
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
        
        if not city and not hotel_name:
            results_list = list(self.db.hotels.values())[:limit]
            self._set_cache(cache_key, results_list)
            return results_list
        
        # Use ID sets to avoid unhashable model instances
        result_ids = set()
        
        # Search by city (exact match, case-insensitive)
        if city:
            city_key = city.lower()
            city_results = self._city_index.get(city_key, [])
            for hotel in city_results:
                result_ids.add(hotel.id)
        
        # Search by hotel name (partial match, case-insensitive)
        if hotel_name:
            name_words = hotel_name.lower().split()
            name_result_ids = set()
            
            for word in name_words:
                # Find hotels containing this word
                for indexed_word, hotels in self._name_index.items():
                    if word in indexed_word:
                        for h in hotels:
                            name_result_ids.add(h.id)
            
            if city:
                # Intersection: hotels that match both city and name
                result_ids = result_ids.intersection(name_result_ids)
            else:
                result_ids = name_result_ids
        
        # Convert to list and apply limit
        results_list = [self.db.hotels[h_id] for h_id in result_ids][:limit]
        self._set_cache(cache_key, results_list)
        return results_list
    
    def rebuild_indexes(self):
        """Rebuild search indexes (call when hotels are added/updated)"""
        self._city_index.clear()
        self._name_index.clear()
        self._build_indexes()
        # Invalidate cache on data/index changes
        self._cache.clear()

class BookingService:
    """Service for booking management with double-booking prevention"""
    
    def __init__(self):
        self.db = DatabaseManager()
        # Thread lock for preventing simultaneous bookings
        self._booking_lock = threading.Lock()
        # Simple per-guest rate limiter: email -> [timestamps]
        self._rate_limit_window = timedelta(seconds=60)
        self._rate_limit_max = 5  # max bookings per window per email
        self._requests_by_email = defaultdict(list)
    
    def _is_rate_limited(self, guest_email: str) -> bool:
        now = datetime.utcnow()
        window_start = now - self._rate_limit_window
        timestamps = self._requests_by_email[guest_email]
        # drop old timestamps
        self._requests_by_email[guest_email] = [t for t in timestamps if t >= window_start]
        if len(self._requests_by_email[guest_email]) >= self._rate_limit_max:
            return True
        self._requests_by_email[guest_email].append(now)
        return False
    
    def create_booking(self, booking_request: BookingRequest) -> Booking:
        """
        Create booking with double-booking prevention using thread locks
        This ensures thread-safe booking operations
        Rate limiting: restrict excessive booking attempts per guest email
        """
        with self._booking_lock:
            # Rate limiting check
            if self._is_rate_limited(booking_request.guest_email):
                raise ValueError("Rate limit exceeded. Please try again later.")
            
            # Validate room exists
            room = self.db.rooms.get(booking_request.room_id)
            if not room:
                raise ValueError("Room not found")
            
            # Validate dates
            if booking_request.check_in_date > booking_request.check_out_date:
                raise ValueError("Check-out date must be after or same as check-in date")
            
            if booking_request.check_in_date < date.today():
                raise ValueError("Check-in date cannot be in the past")
            
            # Check for overlapping bookings
            if self._has_overlapping_booking(booking_request.room_id, 
                                           booking_request.check_in_date, 
                                           booking_request.check_out_date):
                raise ValueError("Room is not available for the selected dates")
            
            # Calculate total price (charge minimum 1 night)
            nights = (booking_request.check_out_date - booking_request.check_in_date).days
            nights_charged = max(1, nights)
            total_price = room.price * nights_charged
            
            # Create booking
            booking = Booking(
                room_id=booking_request.room_id,
                hotel_id=room.hotel_id,
                guest_name=booking_request.guest_name,
                guest_email=booking_request.guest_email,
                check_in_date=booking_request.check_in_date,
                check_out_date=booking_request.check_out_date,
                total_price=total_price
            )
            
            # Store booking
            self.db.bookings[booking.id] = booking
            return booking
    
    def _has_overlapping_booking(self, room_id: str, check_in: date, check_out: date) -> bool:
        """Check if there are overlapping bookings for the room"""
        for booking in self.db.bookings.values():
            if (booking.room_id == room_id and 
                booking.status == BookingStatus.CONFIRMED and
                not (check_out <= booking.check_in_date or check_in >= booking.check_out_date)):
                return True
        return False
    
    def get_bookings(self, guest_name: Optional[str] = None) -> List[Booking]:
        """Get all bookings, optionally filtered by guest name"""
        bookings = list(self.db.bookings.values())
        if guest_name:
            bookings = [b for b in bookings if guest_name.lower() in b.guest_name.lower()]
        return sorted(bookings, key=lambda x: x.created_at, reverse=True)
    
    def get_booking_by_id(self, booking_id: str) -> Optional[Booking]:
        """Get booking by ID"""
        return self.db.bookings.get(booking_id)
    
    def cancel_booking(self, booking_id: str) -> bool:
        """Cancel a booking"""
        booking = self.db.bookings.get(booking_id)
        if booking:
            booking.status = BookingStatus.CANCELLED
            return True
        return False

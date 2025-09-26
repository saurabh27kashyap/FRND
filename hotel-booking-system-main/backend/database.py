"""
Database Manager for Hotel Room Booking Platform using SQLAlchemy ORM
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, Enum, Table, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, scoped_session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from typing import List
import random
import os

Base = declarative_base()

# Enum for RoomType
class RoomType(PyEnum):
    SINGLE = "Single"
    DOUBLE = "Double"
    DELUXE = "Deluxe"
    SUITE = "Suite"

class Hotel(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    city = Column(String(100), nullable=False)
    address = Column(String(200))
    star_rating = Column(Integer)
    description = Column(Text)
    amenities = Column(Text)  # Store amenities as JSON or comma-separated string

    rooms = relationship('Room', back_populates='hotel', cascade="all, delete-orphan")

class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    room_number = Column(String(20), nullable=False)
    room_type = Column(Enum(RoomType), nullable=False)
    price = Column(Integer)
    max_occupancy = Column(Integer)
    amenities = Column(Text)  # Store as comma-separated string

    hotel = relationship('Hotel', back_populates='rooms')
    bookings = relationship('Booking', back_populates='room', cascade="all, delete-orphan")

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    customer_name = Column(String(100))
    check_in = Column(Date)
    check_out = Column(Date)

    room = relationship('Room', back_populates='bookings')

# Database Manager
class DatabaseManager:
    """Database manager using SQLAlchemy."""

    def __init__(self, db_url=None):
        # Use SQLite by default
        if not db_url:
            db_url = os.environ.get("HOTEL_DB_URL", "sqlite:///hotels.db")
        self.engine = create_engine(db_url, echo=False, future=True)
        Base.metadata.create_all(self.engine)
        self.Session = scoped_session(sessionmaker(bind=self.engine))

    def add_hotel(self, hotel_data: dict, rooms_data: List[dict]):
        session = self.Session()
        try:
            hotel = Hotel(
                name=hotel_data["name"],
                city=hotel_data["city"],
                address=hotel_data.get("address", ""),
                star_rating=hotel_data.get("rating", 0),
                description=hotel_data.get("description", ""),
                amenities=",".join(hotel_data.get("amenities", [])),
            )
            session.add(hotel)
            session.flush()  # To get hotel.id

            for room_info in rooms_data:
                room = Room(
                    hotel_id=hotel.id,
                    room_number=room_info["room_number"],
                    room_type=RoomType(room_info["room_type"]),
                    price=room_info["price"],
                    max_occupancy=room_info.get("max_occupancy", 2),
                    amenities=",".join(room_info.get("amenities", []))
                )
                session.add(room)
            session.commit()
            return hotel.id
        except IntegrityError:
            session.rollback()
            raise
        finally:
            session.close()

    def get_hotels(self, city=None):
        session = self.Session()
        try:
            q = session.query(Hotel)
            if city:
                q = q.filter(Hotel.city == city)
            hotels = q.all()
            return hotels
        finally:
            session.close()

    def get_rooms_by_hotel(self, hotel_id):
        session = self.Session()
        try:
            rooms = session.query(Room).filter(Room.hotel_id == hotel_id).all()
            return rooms
        finally:
            session.close()

    def book_room(self, room_id, customer_name, check_in, check_out):
        session = self.Session()
        try:
            booking = Booking(
                room_id=room_id,
                customer_name=customer_name,
                check_in=check_in,
                check_out=check_out
            )
            session.add(booking)
            session.commit()
            return booking.id
        except IntegrityError:
            session.rollback()
            raise
        finally:
            session.close()

    def get_bookings(self, hotel_id=None, room_id=None):
        session = self.Session()
        try:
            q = session.query(Booking)
            if room_id:
                q = q.join(Room).filter(Room.id == room_id)
            elif hotel_id:
                q = q.join(Room).filter(Room.hotel_id == hotel_id)
            bookings = q.all()
            return bookings
        finally:
            session.close()

    # Add more methods as needed: update, delete, etc.

    def populate_sample_data(self):
        """Populate the database with sample hotels and rooms."""
        session = self.Session()
        try:
            # Only add if DB is empty
            if session.query(Hotel).count() > 0:
                print("Sample data already exists.")
                return
            hotel_data_list = [
                # Add sample hotel data as in your original file
                {"name": "The Taj Mahal Palace Mumbai", "city": "Mumbai", "address": "Apollo Bunder, Colaba", "rating": 5, 
                 "description": "Iconic luxury hotel overlooking the Gateway of India", 
                 "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Bar", "Valet Parking", "Concierge", "Business Center"]},
                # ... add more hotels as per your previous initial data
            ]
            for hotel_info in hotel_data_list:
                hotel = Hotel(
                    name=hotel_info["name"],
                    city=hotel_info["city"],
                    address=hotel_info["address"],
                    star_rating=hotel_info["rating"],
                    description=hotel_info["description"],
                    amenities=",".join(hotel_info["amenities"])
                )
                session.add(hotel)
                session.flush()
                # Add rooms
                room_count = random.randint(50, 150) if hotel_info['rating'] == 5 else random.randint(80, 200)
                for j in range(room_count):
                    room_type = random.choice(list(RoomType))
                    price = random.randint(8000, 25000) if hotel_info['rating'] == 5 else random.randint(3000, 12000)
                    room = Room(
                        hotel_id=hotel.id,
                        room_number=f"{random.randint(1, 10)}{j+1:02d}",
                        room_type=room_type,
                        price=price,
                        max_occupancy=2 if room_type == RoomType.SINGLE else random.randint(2, 4),
                        amenities=",".join(random.sample([
                            "AC", "Smart TV", "Mini Bar", "Balcony", "City View", "Sea View", 
                            "Mountain View", "WiFi", "Safe", "Coffee Machine", "Butler Service"
                        ], random.randint(5, 8)))
                    )
                    session.add(room)
            session.commit()
            print("Sample data populated.")
        finally:
            session.close()

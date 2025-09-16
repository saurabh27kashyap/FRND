// Mock data for hotel booking platform
// This replaces the backend API calls for frontend-only demo

export interface Hotel {
  id: string
  name: string
  city: string
  address: string
  star_rating: number
  description: string
  amenities: string[]
  rooms: Room[]
}

export interface Room {
  id: string
  hotel_id: string
  room_number: string
  room_type: string
  price: number
  max_occupancy: number
  amenities: string[]
  is_available: boolean
}

export const mockHotels: Hotel[] = [
  {
    id: "1",
    name: "The Taj Mahal Palace",
    city: "Mumbai",
    address: "Apollo Bunder, Colaba, Mumbai, Maharashtra 400001",
    star_rating: 5,
    description: "Iconic luxury hotel overlooking the Gateway of India with world-class amenities and heritage charm.",
    amenities: ["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar", "Concierge", "Valet Parking"],
    rooms: [
      {
        id: "1-1",
        hotel_id: "1",
        room_number: "101",
        room_type: "Single",
        price: 15000,
        max_occupancy: 1,
        amenities: ["WiFi", "AC", "TV", "Minibar"],
        is_available: true,
      },
      {
        id: "1-2",
        hotel_id: "1",
        room_number: "102",
        room_type: "Single",
        price: 15000,
        max_occupancy: 1,
        amenities: ["WiFi", "AC", "TV", "Minibar"],
        is_available: false,
      },
      {
        id: "1-3",
        hotel_id: "1",
        room_number: "201",
        room_type: "Double",
        price: 25000,
        max_occupancy: 2,
        amenities: ["WiFi", "AC", "TV", "Minibar", "Balcony"],
        is_available: true,
      },
      {
        id: "1-4",
        hotel_id: "1",
        room_number: "202",
        room_type: "Double",
        price: 25000,
        max_occupancy: 2,
        amenities: ["WiFi", "AC", "TV", "Minibar", "Balcony"],
        is_available: true,
      },
      {
        id: "1-5",
        hotel_id: "1",
        room_number: "301",
        room_type: "Suite",
        price: 45000,
        max_occupancy: 4,
        amenities: ["WiFi", "AC", "TV", "Minibar", "Living Room", "Ocean View"],
        is_available: true,
      },
      {
        id: "1-6",
        hotel_id: "1",
        room_number: "302",
        room_type: "Suite",
        price: 45000,
        max_occupancy: 4,
        amenities: ["WiFi", "AC", "TV", "Minibar", "Living Room", "Ocean View"],
        is_available: false,
      },
    ],
  },
  {
    id: "2",
    name: "The Oberoi",
    city: "New Delhi",
    address: "Dr. Zakir Hussain Marg, New Delhi, Delhi 110003",
    star_rating: 5,
    description: "Elegant luxury hotel in the heart of Delhi with impeccable service and sophisticated dining.",
    amenities: ["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar", "Business Center"],
    rooms: [
      {
        id: "2-1",
        hotel_id: "2",
        room_number: "101",
        room_type: "Single",
        price: 12000,
        max_occupancy: 1,
        amenities: ["WiFi", "AC", "TV", "Minibar"],
        is_available: true,
      },
      {
        id: "2-2",
        hotel_id: "2",
        room_number: "201",
        room_type: "Double",
        price: 22000,
        max_occupancy: 2,
        amenities: ["WiFi", "AC", "TV", "Minibar", "Garden View"],
        is_available: true,
      },
      {
        id: "2-3",
        hotel_id: "2",
        room_number: "202",
        room_type: "Double",
        price: 22000,
        max_occupancy: 2,
        amenities: ["WiFi", "AC", "TV", "Minibar", "Garden View"],
        is_available: false,
      },
      {
        id: "2-4",
        hotel_id: "2",
        room_number: "301",
        room_type: "Suite",
        price: 40000,
        max_occupancy: 4,
        amenities: ["WiFi", "AC", "TV", "Minibar", "Living Room", "Butler Service"],
        is_available: true,
      },
    ],
  },
  {
    id: "3",
    name: "The Leela Palace",
    city: "Bangalore",
    address: "23, Kodihalli, HAL Airport Road, Bengaluru, Karnataka 560008",
    star_rating: 5,
    description: "Royal luxury hotel with opulent interiors and exceptional hospitality in the Garden City.",
    amenities: ["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar", "Airport Shuttle"],
    rooms: [
      {
        id: "3-1",
        hotel_id: "3",
        room_number: "101",
        room_type: "Single",
        price: 10000,
        max_occupancy: 1,
        amenities: ["WiFi", "AC", "TV", "Minibar"],
        is_available: true,
      },
      {
        id: "3-2",
        hotel_id: "3",
        room_number: "201",
        room_type: "Double",
        price: 18000,
        max_occupancy: 2,
        amenities: ["WiFi", "AC", "TV", "Minibar", "Club Access"],
        is_available: true,
      },
      {
        id: "3-3",
        hotel_id: "3",
        room_number: "301",
        room_type: "Suite",
        price: 35000,
        max_occupancy: 4,
        amenities: ["WiFi", "AC", "TV", "Minibar", "Living Room", "Royal Decor"],
        is_available: false,
      },
    ],
  },
  {
    id: "4",
    name: "ITC Grand Chola",
    city: "Chennai",
    address: "63, Mount Road, Guindy, Chennai, Tamil Nadu 600032",
    star_rating: 5,
    description: "Magnificent hotel inspired by Chola architecture with world-class facilities and dining.",
    amenities: ["WiFi", "Pool", "Spa", "Gym", "Multiple Restaurants", "Bar", "Business Center"],
    rooms: [
      {
        id: "4-1",
        hotel_id: "4",
        room_number: "101",
        room_type: "Single",
        price: 8000,
        max_occupancy: 1,
        amenities: ["WiFi", "AC", "TV", "Minibar"],
        is_available: true,
      },
      {
        id: "4-2",
        hotel_id: "4",
        room_number: "201",
        room_type: "Double",
        price: 15000,
        max_occupancy: 2,
        amenities: ["WiFi", "AC", "TV", "Minibar", "Executive Lounge"],
        is_available: true,
      },
      {
        id: "4-3",
        hotel_id: "4",
        room_number: "301",
        room_type: "Suite",
        price: 30000,
        max_occupancy: 4,
        amenities: ["WiFi", "AC", "TV", "Minibar", "Living Room", "Chola Architecture"],
        is_available: true,
      },
    ],
  },
  {
    id: "5",
    name: "The Ritz-Carlton",
    city: "Pune",
    address: "Airport Road, Yerawada, Pune, Maharashtra 411006",
    star_rating: 5,
    description: "Contemporary luxury hotel with stunning city views and exceptional service standards.",
    amenities: ["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar", "Airport Shuttle"],
    rooms: [
      {
        id: "5-1",
        hotel_id: "5",
        room_number: "101",
        room_type: "Single",
        price: 9000,
        max_occupancy: 1,
        amenities: ["WiFi", "AC", "TV", "Minibar"],
        is_available: true,
      },
      {
        id: "5-2",
        hotel_id: "5",
        room_number: "201",
        room_type: "Double",
        price: 16000,
        max_occupancy: 2,
        amenities: ["WiFi", "AC", "TV", "Minibar", "City View"],
        is_available: false,
      },
      {
        id: "5-3",
        hotel_id: "5",
        room_number: "301",
        room_type: "Suite",
        price: 32000,
        max_occupancy: 4,
        amenities: ["WiFi", "AC", "TV", "Minibar", "Living Room", "Premium City View"],
        is_available: true,
      },
    ],
  },
  {
    id: "6",
    name: "Hyatt Regency",
    city: "Kolkata",
    address: "JA-1, Sector III, Salt Lake City, Kolkata, West Bengal 700098",
    star_rating: 5,
    description: "Modern luxury hotel in Salt Lake with excellent connectivity and premium amenities.",
    amenities: ["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar", "Business Center"],
    rooms: [
      {
        id: "6-1",
        hotel_id: "6",
        room_number: "101",
        room_type: "Single",
        price: 7000,
        max_occupancy: 1,
        amenities: ["WiFi", "AC", "TV", "Minibar"],
        is_available: true,
      },
      {
        id: "6-2",
        hotel_id: "6",
        room_number: "201",
        room_type: "Double",
        price: 12000,
        max_occupancy: 2,
        amenities: ["WiFi", "AC", "TV", "Minibar", "Lake View"],
        is_available: true,
      },
      {
        id: "6-3",
        hotel_id: "6",
        room_number: "301",
        room_type: "Suite",
        price: 25000,
        max_occupancy: 4,
        amenities: ["WiFi", "AC", "TV", "Minibar", "Living Room", "Regency Club Access"],
        is_available: true,
      },
    ],
  },
]

export const searchHotels = (searchParams: { city?: string; hotel_name?: string }): Hotel[] => {
  let results = mockHotels

  if (searchParams.city) {
    results = results.filter((hotel) => hotel.city.toLowerCase().includes(searchParams.city!.toLowerCase()))
  }

  if (searchParams.hotel_name) {
    results = results.filter((hotel) => hotel.name.toLowerCase().includes(searchParams.hotel_name!.toLowerCase()))
  }

  return results
}

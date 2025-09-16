// API client for hotel booking platform
// Centralized API calls with proper error handling

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

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

export interface Booking {
  id: string
  room_id: string
  hotel_id: string
  guest_name: string
  guest_email: string
  check_in_date: string
  check_out_date: string
  total_price: number
  status: string
  created_at: string
}

export interface SearchRequest {
  city?: string
  hotel_name?: string
  limit?: number
}

export interface BookingRequest {
  room_id: string
  guest_name: string
  guest_email: string
  check_in_date: string
  check_out_date: string
}

class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message)
    this.name = "ApiError"
  }
}

async function apiRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`

  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: "Unknown error" }))
    throw new ApiError(response.status, errorData.detail || `HTTP ${response.status}`)
  }

  return response.json()
}

export const hotelApi = {
  // Search hotels
  searchHotels: async (searchParams: SearchRequest): Promise<Hotel[]> => {
    return apiRequest<Hotel[]>("/api/search", {
      method: "POST",
      body: JSON.stringify(searchParams),
    })
  },

  // Get all hotels
  getHotels: async (skip = 0, limit = 100): Promise<Hotel[]> => {
    return apiRequest<Hotel[]>(`/api/hotels?skip=${skip}&limit=${limit}`)
  },

  // Get specific hotel
  getHotel: async (hotelId: string): Promise<Hotel> => {
    return apiRequest<Hotel>(`/api/hotels/${hotelId}`)
  },

  // Get hotel rooms
  getHotelRooms: async (hotelId: string): Promise<Room[]> => {
    return apiRequest<Room[]>(`/api/hotels/${hotelId}/rooms`)
  },

  // Create booking
  createBooking: async (bookingData: BookingRequest): Promise<Booking> => {
    return apiRequest<Booking>("/api/bookings", {
      method: "POST",
      body: JSON.stringify(bookingData),
    })
  },

  // Get bookings
  getBookings: async (guestName?: string): Promise<Booking[]> => {
    const params = guestName ? `?guest_name=${encodeURIComponent(guestName)}` : ""
    return apiRequest<Booking[]>(`/api/bookings${params}`)
  },

  // Get specific booking
  getBooking: async (bookingId: string): Promise<Booking> => {
    return apiRequest<Booking>(`/api/bookings/${bookingId}`)
  },

  // Cancel booking
  cancelBooking: async (bookingId: string): Promise<{ message: string }> => {
    return apiRequest<{ message: string }>(`/api/bookings/${bookingId}`, {
      method: "DELETE",
    })
  },

  // Performance test
  performanceTest: async (): Promise<{
    results_count: number
    execution_time_ms: number
    total_hotels_in_db: number
  }> => {
    return apiRequest("/api/performance/search")
  },

  // Health check
  healthCheck: async (): Promise<{ status: string; timestamp: string }> => {
    return apiRequest("/health")
  },
}

export { ApiError }

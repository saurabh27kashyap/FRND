"use client"

// Custom hooks for booking management
// Handles booking operations with proper state management and room availability

import { useState, useCallback } from "react"
import { mockHotels } from "@/lib/mock-data"

export interface BookingRequest {
  room_id: string
  guest_name: string
  guest_email: string
  check_in_date: string
  check_out_date: string
}

export interface Booking {
  id: string
  room_id: string
  guest_name: string
  guest_email: string
  check_in_date: string
  check_out_date: string
  status: "confirmed" | "cancelled"
  created_at: string
  total_price: number
}

// Mock booking storage
let mockBookings: Booking[] = []

const bookingLocks = new Set<string>()

function datesOverlap(start1: string, end1: string, start2: string, end2: string): boolean {
  const s1 = new Date(start1)
  const e1 = new Date(end1)
  const s2 = new Date(start2)
  const e2 = new Date(end2)

  return s1 < e2 && s2 < e1
}

function hasConflictingBooking(roomId: string, checkIn: string, checkOut: string): boolean {
  return mockBookings.some(
    (booking) =>
      booking.room_id === roomId &&
      booking.status === "confirmed" &&
      datesOverlap(booking.check_in_date, booking.check_out_date, checkIn, checkOut),
  )
}

export function useBooking() {
  const [isCreating, setIsCreating] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const createBooking = useCallback(async (bookingData: BookingRequest): Promise<Booking> => {
    setIsCreating(true)
    setError(null)

    const lockKey = `${bookingData.room_id}_${bookingData.check_in_date}_${bookingData.check_out_date}`

    if (bookingLocks.has(lockKey)) {
      setIsCreating(false)
      const errorMessage = "Another booking is being processed for this room and dates. Please try again."
      setError(errorMessage)
      throw new Error(errorMessage)
    }

    bookingLocks.add(lockKey)

    try {
      const checkIn = new Date(bookingData.check_in_date)
      const checkOut = new Date(bookingData.check_out_date)
      const today = new Date()
      today.setHours(0, 0, 0, 0)

      if (checkIn < today) {
        throw new Error("Check-in date cannot be in the past")
      }

      if (checkOut <= checkIn) {
        throw new Error("Check-out date must be after check-in date")
      }

      const nights = Math.ceil((checkOut.getTime() - checkIn.getTime()) / (1000 * 60 * 60 * 24))
      if (nights > 30) {
        throw new Error("Maximum stay duration is 30 nights")
      }

      if (hasConflictingBooking(bookingData.room_id, bookingData.check_in_date, bookingData.check_out_date)) {
        throw new Error("This room is already booked for the selected dates. Please choose different dates.")
      }

      await new Promise((resolve) => setTimeout(resolve, 1000))

      let roomPrice = 25000 // Default fallback
      let roomFound = false

      for (const hotel of mockHotels) {
        const room = hotel.rooms.find((r) => r.id === bookingData.room_id)
        if (room) {
          roomPrice = room.price
          roomFound = true
          break
        }
      }

      if (!roomFound) {
        throw new Error("Room not found")
      }

      // Calculate total price
      const totalPrice = nights * roomPrice

      const booking: Booking = {
        id: `booking_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        room_id: bookingData.room_id,
        guest_name: bookingData.guest_name,
        guest_email: bookingData.guest_email,
        check_in_date: bookingData.check_in_date,
        check_out_date: bookingData.check_out_date,
        status: "confirmed",
        created_at: new Date().toISOString(),
        total_price: totalPrice,
      }

      // Store in mock storage
      mockBookings.push(booking)

      return booking
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to create booking. Please try again."
      setError(errorMessage)
      console.error("Booking creation failed:", err)
      throw new Error(errorMessage)
    } finally {
      bookingLocks.delete(lockKey)
      setIsCreating(false)
    }
  }, [])

  return {
    isCreating,
    error,
    createBooking,
  }
}

export function useRoomAvailability() {
  const checkAvailability = useCallback((roomId: string, checkIn: string, checkOut: string): boolean => {
    return !hasConflictingBooking(roomId, checkIn, checkOut)
  }, [])

  const getBookedDates = useCallback((roomId: string): Array<{ start: string; end: string }> => {
    return mockBookings
      .filter((booking) => booking.room_id === roomId && booking.status === "confirmed")
      .map((booking) => ({
        start: booking.check_in_date,
        end: booking.check_out_date,
      }))
  }, [])

  return {
    checkAvailability,
    getBookedDates,
  }
}

export function useBookingList() {
  const [bookings, setBookings] = useState<Booking[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchBookings = useCallback(async (guestName?: string) => {
    setIsLoading(true)
    setError(null)

    try {
      await new Promise((resolve) => setTimeout(resolve, 500))

      let filteredBookings = mockBookings
      if (guestName) {
        filteredBookings = mockBookings.filter((booking) =>
          booking.guest_name.toLowerCase().includes(guestName.toLowerCase()),
        )
      }

      setBookings(filteredBookings)
      return filteredBookings
    } catch (err) {
      const errorMessage = "Failed to load bookings."
      setError(errorMessage)
      setBookings([])
      throw new Error(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }, [])

  const cancelBooking = useCallback(async (bookingId: string) => {
    try {
      await new Promise((resolve) => setTimeout(resolve, 500))

      mockBookings = mockBookings.map((booking) =>
        booking.id === bookingId ? { ...booking, status: "cancelled" as const } : booking,
      )

      // Update local state
      setBookings((prev) =>
        prev.map((booking) => (booking.id === bookingId ? { ...booking, status: "cancelled" as const } : booking)),
      )

      return true
    } catch (err) {
      const errorMessage = "Failed to cancel booking."
      setError(errorMessage)
      throw new Error(errorMessage)
    }
  }, [])

  return {
    bookings,
    isLoading,
    error,
    fetchBookings,
    cancelBooking,
  }
}

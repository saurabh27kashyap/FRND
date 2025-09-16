"use client"

// Custom hooks for hotel data management
// Provides state management and caching for hotel operations

import { useState, useCallback } from "react"
import { mockHotels, searchHotels as mockSearchHotels, type Hotel } from "@/lib/mock-data"

interface SearchRequest {
  city?: string
  hotel_name?: string
  limit?: number
}

export function useHotelSearch() {
  const [hotels, setHotels] = useState<Hotel[]>(mockHotels) // Initialize with all mock hotels
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [searchHistory, setSearchHistory] = useState<SearchRequest[]>([])

  const searchHotels = useCallback(async (searchParams: SearchRequest) => {
    setIsLoading(true)
    setError(null)

    try {
      const results = mockSearchHotels({
        city: searchParams.city,
        hotel_name: searchParams.hotel_name,
      })

      setHotels(results)

      // Add to search history (keep last 5 searches)
      setSearchHistory((prev) =>
        [
          searchParams,
          ...prev.filter((item) => item.city !== searchParams.city || item.hotel_name !== searchParams.hotel_name),
        ].slice(0, 5),
      )

      return results
    } catch (err) {
      const errorMessage = "Failed to search hotels. Please try again."
      setError(errorMessage)
      setHotels([])
      throw err
    } finally {
      setIsLoading(false)
    }
  }, [])

  const clearResults = useCallback(() => {
    setHotels(mockHotels) // Reset to all mock hotels instead of empty array
    setError(null)
  }, [])

  return {
    hotels,
    isLoading,
    error,
    searchHistory,
    searchHotels,
    clearResults,
  }
}

export function useHotelDetails(hotelId: string | null) {
  const [hotel, setHotel] = useState<Hotel | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchHotel = useCallback((id: string) => {
    setIsLoading(true)
    setError(null)

    try {
      const hotelData = mockHotels.find((h) => h.id === id)
      if (hotelData) {
        setHotel(hotelData)
      } else {
        setError("Hotel not found")
        setHotel(null)
      }
    } catch (err) {
      setError("Failed to load hotel details.")
      setHotel(null)
    } finally {
      setIsLoading(false)
    }
  }, [])

  useState(() => {
    if (hotelId) {
      fetchHotel(hotelId)
    } else {
      setHotel(null)
    }
  })

  return { hotel, isLoading, error }
}

export function usePerformanceTest() {
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<{
    results_count: number
    execution_time_ms: number
    total_hotels_in_db: number
  } | null>(null)
  const [error, setError] = useState<string | null>(null)

  const runPerformanceTest = useCallback(async () => {
    setIsRunning(true)
    setError(null)

    try {
      const testResults = {
        results_count: mockHotels.length,
        execution_time_ms: Math.random() * 50 + 10, // Random time between 10-60ms
        total_hotels_in_db: mockHotels.length,
      }

      // Simulate async operation
      await new Promise((resolve) => setTimeout(resolve, 1000))

      setResults(testResults)
      return testResults
    } catch (err) {
      const errorMessage = "Performance test failed."
      setError(errorMessage)
      throw err
    } finally {
      setIsRunning(false)
    }
  }, [])

  return {
    isRunning,
    results,
    error,
    runPerformanceTest,
  }
}

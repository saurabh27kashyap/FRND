"use client"

import { useState } from "react"
import { SearchSection } from "@/components/search-section"
import { HotelList } from "@/components/hotel-list"
import { BookingModal } from "@/components/booking-modal"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { PerformanceTest } from "@/components/performance-test"
import { BookingHistory } from "@/components/booking-history"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useHotelSearch } from "@/hooks/use-hotels"

export default function HomePage() {
  const [selectedRoom, setSelectedRoom] = useState<any>(null)
  const { hotels, isLoading, error, searchHotels, clearResults } = useHotelSearch()

  const handleSearch = async (searchParams: { city?: string; hotelName?: string }) => {
    try {
      await searchHotels({
        city: searchParams.city,
        hotel_name: searchParams.hotelName,
        limit: 50,
      })
    } catch (err) {
      console.error("Search failed:", err)
    }
  }

  const handleBookRoom = (room: any) => {
    setSelectedRoom(room)
  }

  const handleCloseBooking = () => {
    setSelectedRoom(null)
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="container mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-foreground mb-4 text-balance">Find Your Perfect Stay</h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto text-pretty">
            Discover amazing hotels across India with our professional booking platform. Search by city or hotel name to
            find the perfect accommodation for your needs.
          </p>
        </div>

        <Tabs defaultValue="search" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="search">Search Hotels</TabsTrigger>
            <TabsTrigger value="bookings">My Bookings</TabsTrigger>
            <TabsTrigger value="performance">Performance Test</TabsTrigger>
          </TabsList>

          <TabsContent value="search" className="space-y-6">
            <SearchSection onSearch={handleSearch} isLoading={isLoading} />

            {error && (
              <div className="bg-destructive/10 border border-destructive/20 text-destructive px-4 py-3 rounded-lg">
                <p className="font-medium">Search Error</p>
                <p className="text-sm">{error}</p>
              </div>
            )}

            <HotelList hotels={hotels} onBookRoom={handleBookRoom} isLoading={isLoading} />
          </TabsContent>

          <TabsContent value="bookings">
            <BookingHistory />
          </TabsContent>

          <TabsContent value="performance">
            <PerformanceTest />
          </TabsContent>
        </Tabs>
      </main>

      <Footer />

      {selectedRoom && <BookingModal room={selectedRoom} onClose={handleCloseBooking} />}
    </div>
  )
}

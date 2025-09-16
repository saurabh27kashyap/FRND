"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { useBookingList } from "@/hooks/use-bookings"
import { Calendar, User, MapPin, CreditCard, X } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

export function BookingHistory() {
  const [searchName, setSearchName] = useState("")
  const { bookings, isLoading, error, fetchBookings, cancelBooking } = useBookingList()
  const { toast } = useToast()

  useEffect(() => {
    fetchBookings()
  }, [fetchBookings])

  const handleSearch = () => {
    fetchBookings(searchName.trim() || undefined)
  }

  const handleCancelBooking = async (bookingId: string, guestName: string) => {
    try {
      await cancelBooking(bookingId)
      toast({
        title: "Booking Cancelled",
        description: `Booking for ${guestName} has been cancelled successfully.`,
      })
    } catch (err) {
      toast({
        title: "Cancellation Failed",
        description: "Unable to cancel booking. Please try again.",
        variant: "destructive",
      })
    }
  }

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case "confirmed":
        return "bg-green-100 text-green-800 border-green-200"
      case "cancelled":
        return "bg-red-100 text-red-800 border-red-200"
      case "pending":
        return "bg-yellow-100 text-yellow-800 border-yellow-200"
      default:
        return "bg-gray-100 text-gray-800 border-gray-200"
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Calendar className="h-5 w-5 text-primary" />
          Booking History
        </CardTitle>
        <div className="flex gap-2">
          <Input
            placeholder="Search by guest name..."
            value={searchName}
            onChange={(e) => setSearchName(e.target.value)}
            className="max-w-xs"
          />
          <Button onClick={handleSearch} variant="outline">
            Search
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {isLoading && (
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="animate-pulse">
                <div className="h-24 bg-muted rounded-lg"></div>
              </div>
            ))}
          </div>
        )}

        {error && <div className="text-center py-8 text-destructive">Error: {error}</div>}

        {!isLoading && !error && bookings.length === 0 && (
          <div className="text-center py-8 text-muted-foreground">
            No bookings found. Try searching with a different name or make a new booking.
          </div>
        )}

        {!isLoading && bookings.length > 0 && (
          <div className="space-y-4">
            {bookings.map((booking) => (
              <div key={booking.id} className="border border-border rounded-lg p-4">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <h4 className="font-medium text-foreground">Booking #{booking.id.slice(0, 8)}</h4>
                      <Badge className={getStatusColor(booking.status)}>
                        {booking.status.charAt(0).toUpperCase() + booking.status.slice(1)}
                      </Badge>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                      <div className="space-y-2">
                        <div className="flex items-center gap-2 text-muted-foreground">
                          <User className="h-4 w-4" />
                          <span>{booking.guest_name}</span>
                        </div>
                        <div className="flex items-center gap-2 text-muted-foreground">
                          <MapPin className="h-4 w-4" />
                          <span>Room {booking.room_id.slice(0, 8)}</span>
                        </div>
                      </div>

                      <div className="space-y-2">
                        <div className="flex items-center gap-2 text-muted-foreground">
                          <Calendar className="h-4 w-4" />
                          <span>
                            {booking.check_in_date} to {booking.check_out_date}
                          </span>
                        </div>
                        <div className="flex items-center gap-2 text-muted-foreground">
                          <CreditCard className="h-4 w-4" />
                          <span className="font-medium text-primary">₹{booking.total_price.toLocaleString()}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {booking.status === "confirmed" && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleCancelBooking(booking.id, booking.guest_name)}
                      className="text-destructive hover:bg-destructive hover:text-destructive-foreground"
                    >
                      <X className="h-4 w-4 mr-1" />
                      Cancel
                    </Button>
                  )}
                </div>

                <div className="text-xs text-muted-foreground">
                  Booked on {new Date(booking.created_at).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  )
}

"use client"

import type React from "react"

import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Calendar, Users, MapPin, Star, X } from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import { useBooking, useRoomAvailability } from "@/hooks/use-bookings"

interface BookingModalProps {
  room: any
  onClose: () => void
}

export function BookingModal({ room, onClose }: BookingModalProps) {
  const [formData, setFormData] = useState({
    guestName: "",
    guestEmail: "",
    checkInDate: "",
    checkOutDate: "",
  })

  const { isCreating, error, createBooking } = useBooking()
  const { checkAvailability, getBookedDates } = useRoomAvailability()
  const { toast } = useToast()

  const handleInputChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  const calculateTotalPrice = () => {
    if (!formData.checkInDate || !formData.checkOutDate) return 0
    const checkIn = new Date(formData.checkInDate)
    const checkOut = new Date(formData.checkOutDate)
    const nights = Math.ceil((checkOut.getTime() - checkIn.getTime()) / (1000 * 60 * 60 * 24))
    return nights > 0 ? nights * room.price : 0
  }

  const isDateRangeAvailable = () => {
    if (!formData.checkInDate || !formData.checkOutDate) return true
    return checkAvailability(room.id, formData.checkInDate, formData.checkOutDate)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!isDateRangeAvailable()) {
      toast({
        title: "Dates Not Available",
        description: "The selected dates conflict with existing bookings. Please choose different dates.",
        variant: "destructive",
      })
      return
    }

    try {
      const booking = await createBooking({
        room_id: room.id,
        guest_name: formData.guestName,
        guest_email: formData.guestEmail,
        check_in_date: formData.checkInDate,
        check_out_date: formData.checkOutDate,
      })

      toast({
        title: "Booking Confirmed!",
        description: `Your booking for ${room.hotel.name} has been confirmed. Booking ID: ${booking.id.slice(0, 8)}`,
      })
      onClose()
    } catch (err) {
      toast({
        title: "Booking Failed",
        description: error || "Unable to complete booking. Please try again.",
        variant: "destructive",
      })
    }
  }

  const totalPrice = calculateTotalPrice()
  const nights =
    formData.checkInDate && formData.checkOutDate
      ? Math.ceil(
          (new Date(formData.checkOutDate).getTime() - new Date(formData.checkInDate).getTime()) /
            (1000 * 60 * 60 * 24),
        )
      : 0

  const dateRangeAvailable = isDateRangeAvailable()
  const bookedDates = getBookedDates(room.id)

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-xl font-bold text-foreground flex items-center justify-between">
            Book Your Stay
            <Button variant="ghost" size="sm" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-6">
          {/* Hotel & Room Details */}
          <Card>
            <CardContent className="p-4">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h3 className="font-bold text-lg text-foreground flex items-center gap-2">
                    {room.hotel.name}
                    <div className="flex items-center">
                      {[...Array(room.hotel.star_rating)].map((_, i) => (
                        <Star key={i} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                      ))}
                    </div>
                  </h3>
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <MapPin className="h-4 w-4" />
                    <span>{room.hotel.city}</span>
                  </div>
                </div>
              </div>

              <div className="bg-muted p-3 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-foreground">
                    {room.room_type} - Room {room.room_number}
                  </span>
                  <div className="flex items-center gap-1 text-sm text-muted-foreground">
                    <Users className="h-4 w-4" />
                    <span>Max {room.max_occupancy} guests</span>
                  </div>
                </div>
                <div className="flex flex-wrap gap-1 mb-2">
                  {room.amenities.map((amenity: string) => (
                    <Badge key={amenity} variant="outline" className="text-xs">
                      {amenity}
                    </Badge>
                  ))}
                </div>
                <div className="text-right">
                  <span className="text-lg font-bold text-primary">₹{room.price.toLocaleString()}</span>
                  <span className="text-sm text-muted-foreground ml-1">per night</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {bookedDates.length > 0 && (
            <Card className="bg-yellow-50 border-yellow-200">
              <CardContent className="p-4">
                <h4 className="font-medium text-foreground mb-2">Currently Booked Dates</h4>
                <div className="space-y-1 text-sm">
                  {bookedDates.map((booking, index) => (
                    <div key={index} className="flex justify-between">
                      <span>
                        {new Date(booking.start).toLocaleDateString()} - {new Date(booking.end).toLocaleDateString()}
                      </span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Booking Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="guestName">Full Name *</Label>
                <Input
                  id="guestName"
                  required
                  value={formData.guestName}
                  onChange={(e) => handleInputChange("guestName", e.target.value)}
                  placeholder="Enter your full name"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="guestEmail">Email Address *</Label>
                <Input
                  id="guestEmail"
                  type="email"
                  required
                  value={formData.guestEmail}
                  onChange={(e) => handleInputChange("guestEmail", e.target.value)}
                  placeholder="Enter your email"
                />
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="checkInDate" className="flex items-center gap-2">
                  <Calendar className="h-4 w-4" />
                  Check-in Date *
                </Label>
                <Input
                  id="checkInDate"
                  type="date"
                  required
                  min={new Date().toISOString().split("T")[0]}
                  value={formData.checkInDate}
                  onChange={(e) => handleInputChange("checkInDate", e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="checkOutDate" className="flex items-center gap-2">
                  <Calendar className="h-4 w-4" />
                  Check-out Date *
                </Label>
                <Input
                  id="checkOutDate"
                  type="date"
                  required
                  min={formData.checkInDate || new Date().toISOString().split("T")[0]}
                  value={formData.checkOutDate}
                  onChange={(e) => handleInputChange("checkOutDate", e.target.value)}
                />
              </div>
            </div>

            {/* Price Summary */}
            {totalPrice > 0 && (
              <Card className="bg-primary/5 border-primary/20">
                <CardContent className="p-4">
                  <h4 className="font-medium text-foreground mb-2">Booking Summary</h4>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span>Room rate per night:</span>
                      <span>₹{room.price.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Number of nights:</span>
                      <span>{nights}</span>
                    </div>
                    <div className="border-t border-primary/20 pt-1 mt-2">
                      <div className="flex justify-between font-bold text-base">
                        <span>Total Amount:</span>
                        <span className="text-primary">₹{totalPrice.toLocaleString()}</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {formData.checkInDate && formData.checkOutDate && !dateRangeAvailable && (
              <div className="bg-destructive/10 border border-destructive/20 text-destructive px-4 py-3 rounded-lg">
                <p className="text-sm font-medium">⚠️ Selected dates are not available</p>
                <p className="text-sm">
                  This room is already booked for the selected dates. Please choose different dates.
                </p>
              </div>
            )}

            {error && (
              <div className="bg-destructive/10 border border-destructive/20 text-destructive px-4 py-3 rounded-lg">
                <p className="text-sm">{error}</p>
              </div>
            )}

            <div className="flex gap-3 pt-4">
              <Button type="button" variant="outline" onClick={onClose} className="flex-1 bg-transparent">
                Cancel
              </Button>
              <Button
                type="submit"
                disabled={isCreating || !totalPrice || !dateRangeAvailable}
                className="flex-1 bg-secondary hover:bg-secondary/90 text-secondary-foreground"
              >
                {isCreating ? (
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 border-2 border-secondary-foreground border-t-transparent rounded-full animate-spin" />
                    Processing...
                  </div>
                ) : (
                  `Confirm Booking - ₹${totalPrice.toLocaleString()}`
                )}
              </Button>
            </div>
          </form>
        </div>
      </DialogContent>
    </Dialog>
  )
}

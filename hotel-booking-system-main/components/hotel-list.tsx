"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { MapPin, Star, Users, Wifi, Car, Utensils, Dumbbell } from "lucide-react"

interface Hotel {
  id: string
  name: string
  city: string
  address: string
  star_rating: number
  description: string
  amenities: string[]
  rooms: Room[]
}

interface Room {
  id: string
  room_number: string
  room_type: string
  price: number
  max_occupancy: number
  amenities: string[]
  is_available: boolean
}

interface HotelListProps {
  hotels: Hotel[]
  onBookRoom: (room: Room & { hotel: Hotel }) => void
  isLoading: boolean
}

const amenityIcons: Record<string, any> = {
  WiFi: Wifi,
  Parking: Car,
  Restaurant: Utensils,
  Gym: Dumbbell,
}

export function HotelList({ hotels, onBookRoom, isLoading }: HotelListProps) {
  const [expandedHotels, setExpandedHotels] = useState<Set<string>>(new Set())

  const toggleHotelExpansion = (hotelId: string) => {
    const newExpanded = new Set(expandedHotels)
    if (newExpanded.has(hotelId)) {
      newExpanded.delete(hotelId)
    } else {
      newExpanded.add(hotelId)
    }
    setExpandedHotels(newExpanded)
  }

  if (isLoading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <Card key={i} className="animate-pulse">
            <CardContent className="p-6">
              <div className="h-6 bg-muted rounded mb-2"></div>
              <div className="h-4 bg-muted rounded w-2/3 mb-4"></div>
              <div className="h-20 bg-muted rounded"></div>
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  if (hotels.length === 0) {
    return (
      <Card className="text-center py-12">
        <CardContent>
          <div className="text-muted-foreground mb-4">
            <MapPin className="h-12 w-12 mx-auto mb-4 opacity-50" />
            <h3 className="text-lg font-medium mb-2">No hotels found</h3>
            <p>Try searching with different criteria or check popular cities above.</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-foreground">Search Results ({hotels.length} hotels found)</h2>
      </div>

      <div className="space-y-4">
        {hotels.map((hotel) => (
          <Card key={hotel.id} className="shadow-md hover:shadow-lg transition-shadow">
            <CardHeader className="pb-4">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle className="text-xl text-foreground mb-2 flex items-center gap-2">
                    {hotel.name}
                    <div className="flex items-center">
                      {[...Array(hotel.star_rating)].map((_, i) => (
                        <Star key={i} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                      ))}
                    </div>
                  </CardTitle>
                  <div className="flex items-center gap-2 text-muted-foreground mb-2">
                    <MapPin className="h-4 w-4" />
                    <span>
                      {hotel.address}, {hotel.city}
                    </span>
                  </div>
                  <p className="text-sm text-muted-foreground mb-3">{hotel.description}</p>

                  <div className="flex flex-wrap gap-2 mb-4">
                    {hotel.amenities.slice(0, 4).map((amenity) => {
                      const Icon = amenityIcons[amenity]
                      return (
                        <Badge key={amenity} variant="secondary" className="text-xs">
                          {Icon && <Icon className="h-3 w-3 mr-1" />}
                          {amenity}
                        </Badge>
                      )
                    })}
                    {hotel.amenities.length > 4 && (
                      <Badge variant="outline" className="text-xs">
                        +{hotel.amenities.length - 4} more
                      </Badge>
                    )}
                  </div>
                </div>

                <div className="text-right">
                  <Button
                    variant="outline"
                    onClick={() => toggleHotelExpansion(hotel.id)}
                    className="border-primary text-primary hover:bg-primary hover:text-primary-foreground"
                  >
                    {expandedHotels.has(hotel.id) ? "Hide Rooms" : "View Rooms"}
                  </Button>
                </div>
              </div>
            </CardHeader>

            {expandedHotels.has(hotel.id) && (
              <CardContent className="pt-0">
                <div className="border-t border-border pt-4">
                  <h4 className="font-medium text-foreground mb-3">Available Rooms</h4>
                  <div className="grid gap-3">
                    {hotel.rooms.slice(0, 6).map((room) => (
                      <div key={room.id} className="flex items-center justify-between p-4 bg-muted rounded-lg">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <span className="font-medium text-foreground">
                              {room.room_type} - Room {room.room_number}
                            </span>
                            <div className="flex items-center gap-1 text-sm text-muted-foreground">
                              <Users className="h-4 w-4" />
                              <span>Max {room.max_occupancy} guests</span>
                            </div>
                          </div>
                          <div className="flex flex-wrap gap-1">
                            {room.amenities.map((amenity) => (
                              <Badge key={amenity} variant="outline" className="text-xs">
                                {amenity}
                              </Badge>
                            ))}
                          </div>
                        </div>

                        <div className="text-right">
                          <div className="text-lg font-bold text-primary mb-1">₹{room.price.toLocaleString()}</div>
                          <div className="text-xs text-muted-foreground mb-2">per night</div>
                          <Button
                            size="sm"
                            onClick={() => onBookRoom({ ...room, hotel })}
                            disabled={!room.is_available}
                            className="bg-secondary hover:bg-secondary/90 text-secondary-foreground"
                          >
                            {room.is_available ? "Book Now" : "Not Available"}
                          </Button>
                        </div>
                      </div>
                    ))}
                    {hotel.rooms.length > 6 && (
                      <div className="text-center text-sm text-muted-foreground">
                        +{hotel.rooms.length - 6} more rooms available
                      </div>
                    )}
                  </div>
                </div>
              </CardContent>
            )}
          </Card>
        ))}
      </div>
    </div>
  )
}

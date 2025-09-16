"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { Search, MapPin, Building, Clock } from "lucide-react"

interface SearchSectionProps {
  onSearch: (params: { city?: string; hotelName?: string }) => void
  isLoading: boolean
}

export function SearchSection({ onSearch, isLoading }: SearchSectionProps) {
  const [city, setCity] = useState("")
  const [hotelName, setHotelName] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (city.trim() || hotelName.trim()) {
      onSearch({
        city: city.trim() || undefined,
        hotelName: hotelName.trim() || undefined,
      })
    }
  }

  const popularCities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Goa", "Jaipur", "Hyderabad", "Pune"]

  return (
    <Card className="mb-8 shadow-lg">
      <CardContent className="p-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground flex items-center gap-2">
                <MapPin className="h-4 w-4 text-primary" />
                Search by City
              </label>
              <Input
                placeholder="Enter city name (e.g., Mumbai, Delhi)"
                value={city}
                onChange={(e) => setCity(e.target.value)}
                className="bg-input border-border focus:ring-primary"
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground flex items-center gap-2">
                <Building className="h-4 w-4 text-primary" />
                Search by Hotel Name
              </label>
              <Input
                placeholder="Enter hotel name"
                value={hotelName}
                onChange={(e) => setHotelName(e.target.value)}
                className="bg-input border-border focus:ring-primary"
              />
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
            <div className="flex flex-wrap gap-2">
              <span className="text-sm text-muted-foreground">Popular cities:</span>
              {popularCities.map((popularCity) => (
                <Button
                  key={popularCity}
                  variant="outline"
                  size="sm"
                  type="button"
                  onClick={() => setCity(popularCity)}
                  className="text-xs border-border hover:bg-primary hover:text-primary-foreground"
                >
                  {popularCity}
                </Button>
              ))}
            </div>

            <Button
              type="submit"
              disabled={isLoading || (!city.trim() && !hotelName.trim())}
              className="bg-primary hover:bg-primary/90 text-primary-foreground min-w-[120px]"
            >
              {isLoading ? (
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-primary-foreground border-t-transparent rounded-full animate-spin" />
                  Searching...
                </div>
              ) : (
                <div className="flex items-center gap-2">
                  <Search className="h-4 w-4" />
                  Search Hotels
                </div>
              )}
            </Button>
          </div>

          <div className="bg-muted/50 p-3 rounded-lg">
            <div className="flex items-start gap-2 text-sm text-muted-foreground">
              <Clock className="h-4 w-4 mt-0.5 flex-shrink-0" />
              <div>
                <p className="font-medium mb-1">Search Tips:</p>
                <ul className="space-y-1 text-xs">
                  <li>• Search by city to find all hotels in that location</li>
                  <li>• Search by hotel name for specific properties</li>
                  <li>• Combine both for more precise results</li>
                  <li>• Our system can search through 1M+ hotel records instantly</li>
                </ul>
              </div>
            </div>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}

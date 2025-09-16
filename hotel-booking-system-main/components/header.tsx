import { Building2, Phone, Mail } from "lucide-react"

export function Header() {
  return (
    <header className="bg-card border-b border-border">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-primary text-primary-foreground p-2 rounded-lg">
              <Building2 className="h-6 w-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-foreground">HotelBooking Pro</h1>
              <p className="text-sm text-muted-foreground">Professional Hotel Booking Platform</p>
            </div>
          </div>

          <div className="hidden md:flex items-center gap-6 text-sm text-muted-foreground">
            <div className="flex items-center gap-2">
              <Phone className="h-4 w-4" />
              <span>+91 1800-123-4567</span>
            </div>
            <div className="flex items-center gap-2">
              <Mail className="h-4 w-4" />
              <span>support@hotelbooking.com</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

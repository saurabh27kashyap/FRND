import { Building2, Github, Mail, Phone } from "lucide-react"

export function Footer() {
  return (
    <footer className="bg-card border-t border-border mt-16">
      <div className="container mx-auto px-4 py-8">
        <div className="grid md:grid-cols-3 gap-8">
          <div>
            <div className="flex items-center gap-3 mb-4">
              <div className="bg-primary text-primary-foreground p-2 rounded-lg">
                <Building2 className="h-5 w-5" />
              </div>
              <div>
                <h3 className="font-bold text-foreground">HotelBooking Pro</h3>
                <p className="text-sm text-muted-foreground">Professional Booking Platform</p>
              </div>
            </div>
            <p className="text-sm text-muted-foreground">
              Your trusted partner for hotel bookings across India. Clean architecture, reliable service, and
              professional support.
            </p>
          </div>

          <div>
            <h4 className="font-medium text-foreground mb-3">Contact Information</h4>
            <div className="space-y-2 text-sm text-muted-foreground">
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

          <div>
            <h4 className="font-medium text-foreground mb-3">Technical Details</h4>
            <div className="space-y-2 text-sm text-muted-foreground">
              <p>Built with clean architecture principles</p>
              <p>Python FastAPI backend + React frontend</p>
              <p>Optimized for performance and scalability</p>
              <div className="flex items-center gap-2 mt-3">
                <Github className="h-4 w-4" />
                <span>Open source implementation</span>
              </div>
            </div>
          </div>
        </div>

        <div className="border-t border-border mt-8 pt-6 text-center text-sm text-muted-foreground">
          <p>&copy; 2024 HotelBooking Pro. Built with clean architecture and modern technologies.</p>
        </div>
      </div>
    </footer>
  )
}

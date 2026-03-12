import { MapContainer, TileLayer, ZoomControl } from "react-leaflet"

export default function RiderMap() {

  const position = [30.3165, 78.0322] // Dehradun

  return (
    <div className="w-full h-full z-0 relative">

      <MapContainer
        center={position}
        zoom={13}
        scrollWheelZoom={true}
        zoomControl={false}
        className="w-full h-full"
      >

        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <ZoomControl position="topright" />

      </MapContainer>

    </div>
  )
}
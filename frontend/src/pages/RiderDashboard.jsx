import RiderSidebar from "../components/rider/RiderSidebar";
import RiderStatus from "../components/rider/RiderStatus";
import RiderMap from "../components/rider/RiderMap";


export default function RiderDashboard(){
    return (
        
        <div className="flex h-screen bg-slate-900">

            {/* Sidebar */}
            <RiderSidebar />

            {/* Map Section */}
            <div className="flex-1 relative">
                <RiderMap />

                {/* Ride Status */}
                <div className="absolute bottom-6 left-1/2 transform -translate-x-1/2 w-full max-w-xl px-4">
                    <RiderStatus />
                </div>
            </div>
            
        </div>
        
    );
}
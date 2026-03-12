import DriverSidebar from "../components/driver/DriverSidebar";
import DriverMap from "../components/driver/DriverMap";
import DriverStatus from "../components/driver/DriverStatus";

export default function DriverDashboard(){

    return (
        <div className="h-screen flex bg-slate-900 text-white">

            {/* Sidebar */}
            <DriverSidebar />

            {/* Map Section */}
            <div className="flex-1 relative">
                <DriverMap />

                {/* Ride Status */}
                <div className="absolute bottom-6 left-1/2 transform -translate-x-1/2 w-full max-w-xl px-4">
                    <DriverStatus />
                </div>
            </div>
        </div>
    );
}
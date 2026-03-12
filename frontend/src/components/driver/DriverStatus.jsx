import { Car } from "lucide-react";

export default function RiderStatus(){

    return (
        <div className="bg-slate-900 text-white p-4 rounded-xl shadow-xl flex items-center justify-between">
            <div className="flex items-center gap-3">
                <Car className="text-cyan-400" />
                <span>Arriving at pickup in 3 mins</span>
            </div>

            <button className="text-cyan-400 hover:text-white">→</button>
        </div>
    );
}
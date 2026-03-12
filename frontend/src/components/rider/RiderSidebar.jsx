import { Car, Clock, CreditCard, UserCircle, Menu, X, LogOut } from "lucide-react";
import { useState } from "react";
import { useAuth } from "../../context/authContext";

export default function RiderSidebar() {
    const [open, setOpen] = useState(false);
    const { user, logout } = useAuth();

    return (
        <>
            {/* Mobile Menu Button */}
            <button className="md:hidden fixed top-4 left-4 z-50 text-white" onClick={() => setOpen(true)}>
                <Menu className="bg-gradient-to-br from-slate-800 to-blue-900 hover:cursor-pointer" size={28} />
            </button>

            {/* Overlay */}
            {open && (
                <div
                    className="fixed inset-0 bg-black/40 z-40 md:hidden"
                    onClick={() => setOpen(false)}
                />
            )}

            {/* Sidebar */}
            <div className={`fixed md:relative top-0 left-0 h-screen w-64 bg-slate-950 text-white 
                flex flex-col p-6 transform transition-transform duration-300 z-50
                ${open ? "translate-x-0" : "-translate-x-full"} md:translate-x-0`}>

                {/* Close Button (mobile only) */}
                <button className="md:hidden absolute top-4 right-4 hover:cursor-pointer" onClick={() => setOpen(false)}>
                    <X size={22} />
                </button>

                {/* Logo */}
                <h1 className="text-2xl font-bold mb-10">
                    Cab<span className="text-cyan-400">Zy</span>
                </h1>

                <div className="relative mt-2">
                    <div className="flex items-center gap-2 mb-2 text-white text-lg font-semibold">
                        <UserCircle className="w-4 h-4" />
                        <span>{user?.name || "Guest"}</span>
                    </div>
                    {/* <p className="text-xs text-gray-400">{user?.email}</p> ✅ SHOW EMAIL */}
                </div>

                {/* Menu */}
                <nav className="flex flex-col gap-6 mt-4">
                    <button className="flex items-center gap-3 bg-cyan-400 text-white px-4 py-3 rounded-lg hover:cursor-pointer">
                        <Car size={18} />
                        Book a Ride
                    </button>

                    <button className="flex items-center gap-3 font-semibold text-slate-300 hover:text-cyan-400 hover:cursor-pointer">
                        <Clock size={18} />
                        Ride History
                    </button>

                    <button className="flex items-center gap-3 font-semibold text-slate-300 hover:text-cyan-400 hover:cursor-pointer">
                        <CreditCard size={18} />
                        Payment Methods
                    </button>
                </nav>

                <button 
                    onClick={logout}
                    className="mt-auto flex items-center gap-3 text-white hover:cursor-pointer hover:text-cyan-400"
                >
                    <LogOut size={20} />
                    <span>Logout</span>
                </button>
            </div>
        </>
    );
}
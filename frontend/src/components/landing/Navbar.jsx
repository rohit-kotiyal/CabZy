import { Link } from "react-router-dom";
import { Menu } from "lucide-react";

export default function Navbar(){
    return (
        <nav className="w-full absolute top-0 left-0 z-50">
            <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">

                {/* Logo */}
                <Link to="/" className="flex items-center space-x-3">
                    <h1 className="text-3xl font-bold text-white">
                        Cab<span className="text-cyan-400">Zy</span>
                    </h1>
                </Link>

                {/* Nav Links */}
                <div className="hidden md:flex items-center space-x-8 text-white font-medium">
                    <Link to="/about" className="hover:text-cyan-400 transition">About</Link>
                    <Link to="/contact" className="hover:text-cyan-400 transition">Contact Us</Link>
                    <Link to="/register" className="border-2 border-cyan-500 text-cyan-400 px-6 py-2.5 rounded-lg hover:bg-cyan-500 hover:text-white transition font-semibold">Sign Up</Link>
                    <Link to="/login" className="bg-cyan-500 px-6 py-2.5 rounded-lg hover:bg-cyan-600 transition font-semibold shadow-lg">Sign In</Link>
                </div>


                {/* Mobile Menu Button */}
                <button className="md:hidden text-white">
                    <Menu size={24}></Menu>
                </button>

            </div>
        </nav>
    );
}
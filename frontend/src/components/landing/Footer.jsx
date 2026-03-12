import { FaFacebookF, FaTwitter, FaInstagram } from "react-icons/fa";
import { Link } from "react-router-dom";

export default function Footer(){
    
    return (
        <footer className="bg-slate-900 text-white">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 sm:py-12">

                {/* Main Footer Section */}
                <div className="flex flex-col md:flex-row items-center md:items-start justify-between gap-8 mb-8">

                    {/* Logo Section */}
                    <div className="flex items-center gap-3">
                        <h1 className="text-xl md:text-2xl font-bold text-white">
                            Cab<span className="text-cyan-400">Zy</span>
                        </h1>
                    </div>

                    {/* Navigation Links */}
                    <nav className="flex flex-wrap items-center justify-center gap-4 md:gap-8">
                        <Link to="/privacy" className="text-gray-300 hover:text-cyan-400 transition-colors text-sm md:text-base">Privacy Policy</Link>
                        <Link to="/terms" className="text-gray-300 hover:text-cyan-400 transition-colors text-sm md:text-base">Terms & Conditions</Link>
                    </nav>

                    {/* Social Media Links */}
                    <div className="flex items-center gap-3 md:gap-4">
                        <a 
                            href="#" 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="w-10 h-10 bg-blue-600 hover:bg-blue-700 rounded-lg flex items-center justify-center transition-all hover:scale-110"
                        >
                            <FaFacebookF size={20} />
                        </a>
                        <a 
                            href="#" 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="w-10 h-10 bg-sky-500 hover:bg-sky-600 rounded-lg flex items-center justify-center transition-all hover:scale-110"
                        >
                            <FaTwitter size={20} />
                        </a>
                        <a 
                            href="#" 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="w-10 h-10 bg-linear-to-br from-purple-600 via-p
                            
                            
                            
                            
                            
                            
                            
                            ink-600 to-orange-500 hover:opacity-90 rounded-lg flex items-center justify-center transition-all hover:scale-110"
                        >
                            <FaInstagram size={20} />
                        </a>
                    </div>
                </div>

                {/* Copyright Section */}
                <div className="border-t border-slate-700 pt-6 sm:pt-8 text-center">
                    <p className="text-gray-400 text-xs sm:text-sm">
                        © 2026 CabZy. All rights reserved.
                    </p>
                </div>
            </div>
        </footer>        
    );
}
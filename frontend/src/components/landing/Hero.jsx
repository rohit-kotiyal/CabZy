import { Car, Gauge, MapPin, Navigation, Shield, FileText } from "lucide-react";
import { Link } from "react-router-dom";


export default function Hero(){
    return (
        <>
            <section className="relative min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 overflow-hidden pt-20">
                <div className="relative max-w-7xl mx-auto px-4 sm:px-6 pt-20 sm:pt-32 pb-20 flex flex-col md:flex-row items-center justify-between gap-8 md:gap-12">

                    {/* Left Content */}
                    <div className="flex-1 text-white z-10 text-center md:text-left">
                        <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold mb-4 leading-tight">Book Rides Instantly.</h1>
                        <p className="text-lg sm:text-xl md:text-2xl text-gray-300 mb-8 md:mb-10">Safe. Fast. Reliable.</p>

                        {/* CTA Buttons */}
                        <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center md:justify-start">
                            <Link to="/book" className="bg-cyan-500 hover:bg-cyan-600 text-white px-6 sm:px-8 py-3 sm:py-4 rounded-lg font-semibold flex items-center justify-center gap-3 transition-all hover:scale-105 text-sm sm:text-base">
                                <Car size={20} />
                                Book a Ride
                            </Link>
                            <Link to="/driver" className="bg-slate-700 hover:bg-slate-600 text-white px-6 sm:px-8 py-3 sm:py-4 rounded-lg font-semibold flex items-center justify-center gap-3 transition-all hover:scale-105 border border-slate-600 text-sm sm:text-base">
                                <Gauge size={20} />
                                Become a Driver
                            </Link>
                        </div>
                    </div>


                    {/* Right Content - Phone Mockup */}
                    <div className="flex-1 relative w-full md:w-auto">
                        <div className="max-w-[280px] sm:max-w-xs mx-auto relative mt-8 md:-mt-15 lg:-mt-22">

                            {/* Phone Frame */}
                            <div className="relative bg-black rounded-[2.5rem] sm:rounded-[3rem] p-2 sm:p-3 shadow-2xl border-2 sm:border-4 border-slate-700 transform hover:scale-105 transition-transform duration-300">
                                
                                {/* Notch */}
                                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-24 sm:w-32 h-5 sm:h-6 bg-black rounded-b-2xl z-20"></div>
                                
                                {/* Phone Screen */}
                                <div className="bg-white rounded-[2rem] sm:rounded-[2.5rem] h-[480px] sm:h-[550px] relative overflow-hidden">
                                    
                                    {/* Map Background SVG */}
                                    <svg className="absolute inset-0 w-full h-full" viewBox="0 0 300 650" preserveAspectRatio="xMidYMid slice">
                                        <defs>
                                            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                                                <rect width="40" height="40" fill="#f0f9ff" />
                                                <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#e0f2fe" strokeWidth="1"/>
                                            </pattern>
                                        </defs>
                                        
                                        {/* Grid background */}
                                        <rect width="100%" height="100%" fill="url(#grid)"/>
                                        
                                        {/* Map streets */}
                                        <path d="M 0 150 L 300 150" stroke="#cbd5e1" strokeWidth="3" opacity="0.6"/>
                                        <path d="M 0 250 L 300 250" stroke="#cbd5e1" strokeWidth="2" opacity="0.6"/>
                                        <path d="M 0 350 L 300 350" stroke="#cbd5e1" strokeWidth="3" opacity="0.6"/>
                                        <path d="M 0 450 L 300 450" stroke="#cbd5e1" strokeWidth="2" opacity="0.6"/>
                                        
                                        <path d="M 100 0 L 100 650" stroke="#cbd5e1" strokeWidth="2" opacity="0.6"/>
                                        <path d="M 200 0 L 200 650" stroke="#cbd5e1" strokeWidth="3" opacity="0.6"/>
                                        
                                        {/* Park areas */}
                                        <rect x="20" y="180" width="60" height="50" fill="#86efac" opacity="0.3" rx="5"/>
                                        <rect x="220" y="280" width="60" height="60" fill="#86efac" opacity="0.3" rx="5"/>
                                        
                                        {/* Buildings */}
                                        <rect x="110" y="160" width="30" height="40" fill="#94a3b8" opacity="0.4"/>
                                        <rect x="210" y="160" width="40" height="50" fill="#94a3b8" opacity="0.4"/>
                                        <rect x="30" y="360" width="35" height="45" fill="#94a3b8" opacity="0.4"/>
                                        <rect x="210" y="460" width="30" height="40" fill="#94a3b8" opacity="0.4"/>
                                        
                                        {/* Route Path - Curved line from top to bottom */}
                                        <path 
                                            d="M 150 120 Q 80 280 150 350 Q 220 420 140 550" 
                                            stroke="#06b6d4" 
                                            strokeWidth="5" 
                                            fill="none" 
                                            strokeDasharray="10 10" 
                                            strokeLinecap="round"
                                            opacity="0.9"
                                        />
                                    </svg>

                                    {/* Pickup Location Pin (Top - Cyan) */}
                                    <div className="absolute top-20 sm:top-24 left-1/2 -translate-x-1/2 z-10 animate-bounce" style={{animationDuration: '2s'}}>
                                        <MapPin className="w-8 sm:w-10 h-8 sm:h-10 text-cyan-500 fill-cyan-500 drop-shadow-lg" />
                                    </div>

                                    {/* Drop Location Pin (Bottom - Dark) */}
                                    <div className="absolute bottom-20 sm:bottom-24 left-[35%] z-10">
                                        <MapPin className="w-10 sm:w-12 h-10 sm:h-12 text-slate-800 fill-slate-800 drop-shadow-lg" />
                                    </div>

                                    {/* Car Icon on Route */}
                                    <div className="absolute top-[45%] left-1/2 -translate-x-1/2 z-10 transform -rotate-12">
                                        <div className="text-3xl sm:text-4xl drop-shadow-lg">🚗</div>
                                    </div>

                                    {/* Top Card - Pickup Location */}
                                    <div className="absolute top-3 sm:top-4 left-3 sm:left-4 right-3 sm:right-4 bg-white rounded-lg sm:rounded-xl shadow-lg p-3 sm:p-4 flex items-center gap-2 sm:gap-3 z-20 backdrop-blur-sm bg-opacity-95">
                                        <div className="bg-cyan-100 p-1.5 sm:p-2 rounded-lg">
                                            <Navigation className="w-4 sm:w-5 h-4 sm:h-5 text-cyan-600" />
                                        </div>
                                        <div className="flex-1">
                                            <p className="text-[10px] sm:text-xs text-gray-500 font-medium">Pick-up Location</p>
                                            <p className="text-xs sm:text-sm font-semibold text-gray-800">New Delhi, India</p>
                                        </div>
                                    </div>

                                    {/* Bottom Button */}
                                    <div className="absolute bottom-4 sm:bottom-6 left-3 sm:left-4 right-3 sm:right-4 z-20">
                                        <button className="w-full bg-gradient-to-r from-cyan-500 to-cyan-600 text-white py-3 sm:py-4 rounded-lg sm:rounded-xl font-bold text-base sm:text-lg shadow-xl hover:shadow-2xl transition-all hover:scale-105 flex items-center justify-center gap-2">
                                            Request Ride
                                            <span className="text-lg sm:text-xl">→</span>
                                        </button>
                                    </div>

                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="bg-gray-50 py-12 sm:py-16 md:py-20">
                <div className="max-w-7xl mx-auto px-4 sm:px-6">
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 sm:gap-10 md:gap-12">

                        {/* Live Tracking */}
                        <div className="flex items-start gap-3 sm:gap-4 group hover:transform hover:scale-105 transition-all">
                            <div className="bg-cyan-100 p-3 sm:p-4 rounded-xl sm:rounded-2xl group-hover:bg-cyan-200 transition-colors flex-shrink-0">
                                <MapPin className="w-8 sm:w-10 h-8 sm:h-10 text-cyan-600" />
                            </div>
                            <div>
                                <h3 className="text-xl sm:text-2xl font-bold text-slate-900 mb-1 sm:mb-2">Live Tracking</h3>
                                <p className="text-sm sm:text-base text-gray-600 leading-relaxed">Track your ride in real-time from start to finish.</p>
                            </div>
                        </div>

                        {/* Secure Payments */}
                        <div className="flex items-start gap-3 sm:gap-4 group hover:transform hover:scale-105 transition-all">
                            <div className="bg-cyan-100 p-3 sm:p-4 rounded-xl sm:rounded-2xl group-hover:bg-cyan-200 transition-colors flex-shrink-0">
                                <Shield className="w-8 sm:w-10 h-8 sm:h-10 text-cyan-600" />
                            </div>
                            <div>
                                <h3 className="text-xl sm:text-2xl font-bold text-slate-900 mb-1 sm:mb-2">Secure Payments</h3>
                                <p className="text-sm sm:text-base text-gray-600 leading-relaxed">Pay seamlessly and securely through the app.</p>
                            </div>
                        </div>

                        {/* Ride History */}
                        <div className="flex items-start gap-3 sm:gap-4 group hover:transform hover:scale-105 transition-all sm:col-span-2 md:col-span-1">
                            <div className="bg-cyan-100 p-3 sm:p-4 rounded-xl sm:rounded-2xl group-hover:bg-cyan-200 transition-colors flex-shrink-0">
                                <FileText className="w-8 sm:w-10 h-8 sm:h-10 text-cyan-600" />
                            </div>
                            <div>
                                <h3 className="text-xl sm:text-2xl font-bold text-slate-900 mb-1 sm:mb-2">Ride History</h3>
                                <p className="text-sm sm:text-base text-gray-600 leading-relaxed">View and manage all your past rides easily.</p>
                            </div>
                        </div>

                    </div>
                </div>
            </section>
        </>
    );
}
import { Mail, Lock, User, Phone, UserCircle } from "lucide-react";
import { Link } from "react-router-dom";


export default function Register(){
    return (
        <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-slate-900 to-slate-800">
            <div className="w-full max-w-2xl bg-slate-900/80 backdrop-blur-xl p-10 rounded-2xl shadow-xl">
                <Link to="/">
                    <h1 className="text-3xl text-white font-bold text-center mb-8">
                    Cab<span className="text-cyan-400">Zy</span>
                    </h1>
                </Link>

                <h1 className="text-2xl text-white text-center font-bold mb-8"><span>Join<span className="text-cyan-400">Us</span></span></h1>

                <form className="space-y-4">

                    <div className="grid grid-cols-2 gap-4">
                        {/* Name */}
                        <div className="relative">
                            <label className="flex items-center gap-2 mb-2 text-white text-lg font-semibold">
                                <User className="w-4 h-4" />
                                <span>Na<span className="text-cyan-400">me</span></span>
                            </label>
                            <input type="text" placeholder="Enter your name" className="w-full p-3 bg-slate-800 rounded-lg text-white outline-none" />
                        </div>

                        {/* Role */}
                        <div className="relative">
                            <label className="flex items-center gap-2 mb-2 text-white text-lg font-semibold">
                                <UserCircle className="w-4 h-4" />
                                <span>Ro<span className="text-cyan-400">le</span></span>
                            </label>
                            <select type="text" placeholder="Enter your name" className="w-full p-3 bg-slate-800 rounded-lg text-white outline-none">
                                <option value="rider">Rider</option>
                                <option value="driver">Driver</option>
                            </select>
                        </div>
                    

                        {/* Email */}
                        <div className="relative">
                            <label className="flex items-center gap-2 mb-2 text-white text-lg font-semibold">
                                <Mail className="w-4 h-4" />
                                <span>Ema<span className="text-cyan-400">il</span></span>
                            </label>
                            <input type="email" name="email" placeholder="Enter your email" className="w-full p-3 bg-slate-800 rounded-lg text-white outline-none" />
                        </div>

                        {/* Contact */}
                        <div className="relative">
                            <label className="flex items-center gap-2 mb-2 text-white text-lg font-semibold">
                                <Phone className="w-4 h-4" />
                                <span>Conta<span className="text-cyan-400">ct</span></span>
                            </label>
                            <input type="tel" placeholder="Enter your number" className="w-full p-3 bg-slate-800 rounded-lg text-white outline-none" />
                        </div>

                        {/* Password */}
                        <div className="relative">
                            <label className="flex items-center gap-2 mb-2 text-white text-lg font-semibold">
                                <Lock className="w-4 h-4" />
                                <span>Passwo<span className="text-cyan-400">rd</span></span>
                            </label>
                            <input type="password" name="password" placeholder="Enter your password" className="w-full p-3 bg-slate-800 rounded-lg text-white outline-none" />
                        </div>

                        {/* Confirm Password */}
                        <div className="relative">
                            <label className="flex items-center gap-2 mb-2 text-white text-lg font-semibold">
                                <Lock className="w-4 h-4" />
                                <span>Confirm Passwo<span className="text-cyan-400">rd</span></span>
                            </label>
                            <input type="password" name="password" placeholder="Confirm password" className="w-full p-3 bg-slate-800 rounded-lg text-white outline-none" />
                        </div>
                    </div>


                    {/* Register */}
                    <button className="w-full bg-cyan-500 hover:bg-cyan-600 transition rounded-lg p-3 text-white font-semibold hover:cursor-pointer">Sign Up</button>
                </form>

                <div className="text-center text-gray-400 mt-6 text-sm">Or Sign Up With</div>
                <div className="flex gap-4 mt-4">
                    <button className="flex-1 bg-linear-to-br from-[#EA4335] to-[#C5221F] text-white py-2 rounded-lg hover:cursor-pointer">Google</button>
                    <button className="flex-1 bg-linear-to-br from-gray-800 to-[#1C1C1E] text-white py-2 rounded-lg hover:cursor-pointer">Apple</button>
                </div>
                <p className="text-center text-gray-400 text-sm mt-6">
                    Already have an account?{" "}
                    <Link to="/login" className="text-cyan-400">Sign In</Link>
                </p>
            </div>
        </div>
    );
}
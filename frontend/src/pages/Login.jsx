import { Mail, Lock } from "lucide-react";
import { Link } from "react-router-dom";


export default function Login(){

    return (
        
        <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-slate-900 to-slate-800">
            <div className="bg-slate-900/80 backdrop-blur-xl p-10 rounded-2xl shadow-xl w-100">
                <Link to="/">
                    <h1 className="text-3xl text-white font-bold text-center mb-8">
                    Cab<span className="text-cyan-400">Zy</span>
                    </h1>
                </Link>

                <form action="" className="space-y-4">
                    <div className="relative">
                        <label className="flex items-center gap-2 mb-2 text-white text-lg font-semibold">
                            <Mail className="w-4 h-4" />
                            <span>Ema<span className="text-cyan-400">il</span></span>
                        </label>
                        <input type="email" name="email" required placeholder="Enter your email" className="w-full p-3 bg-slate-800 rounded-lg text-white outline-none" />
                    </div>

                    <div className="relative">
                        <label className="flex items-center gap-2 mb-2 text-white text-lg font-semibold">
                            <Lock className="w-4 h-4" />
                            <span>Passwo<span className="text-cyan-400">rd</span></span>
                        </label>
                        <input type="password" placeholder="Enter your password" className="w-full p-3 bg-slate-800 rounded-lg text-white outline-none" />
                    </div>
                    <button className="w-full bg-cyan-500 hover:bg-cyan-600 transition rounded-lg p-3 text-white font-semibold hover:cursor-pointer">Sign In</button>
                </form>

                <div className="flex items-center justify-between text-sm mt-6">
                    <label className="flex items-center text-gray-400">
                        <input type="checkbox" className="mr-2"/>
                        Remember Me
                    </label>
                    <Link to="/forgot-password" className="text-cyan-400 hover:underline">Forgot Password?</Link>
                </div>

                <div className="text-center text-gray-400 mt-6 text-sm">Or Sign In With</div>
                <div className="flex gap-4 mt-4">
                    <button className="flex-1 bg-linear-to-br from-[#EA4335] to-[#C5221F] text-white py-2 rounded-lg hover:cursor-pointer">Google</button>
                    <button className="flex-1 bg-linear-to-br from-gray-800 to-[#1C1C1E] text-white py-2 rounded-lg hover:cursor-pointer">Apple</button>
                </div>
                <p className="text-center text-gray-400 text-sm mt-6">
                    Don't have an account?{" "}
                    <Link to="/register" className="text-cyan-400">Sign Up</Link>
                </p>
            </div>
        </div>
    );
}
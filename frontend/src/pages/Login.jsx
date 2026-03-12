import { Mail, Lock, AlertCircle } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { loginUser, getCurrentUser } from "../api/auth";
import { useAuth } from "../context/authContext"; 

export default function Login() {
    const [formData, setFormData] = useState({
        email: "",
        password: ""
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [rememberMe, setRememberMe] = useState(false);
    const navigate = useNavigate();
    const { login } = useAuth(); 

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
        
        if (error) {
            setError("");
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!formData.email || !formData.password) {
            setError("Please enter both email and password");
            return;
        }

        setLoading(true);
        setError("");

        try {
            // Call login API
            const response = await loginUser(formData);
            const token = response.data.access_token;
            
            // Store token in localStorage first
            localStorage.setItem("token", token);
            login(token);
            
            // Fetch user data to determine role
            const userResponse = await getCurrentUser();
            const userRole = userResponse.data.role;
            
            // Navigate based on role
            const targetPath = userRole === "rider" ? "/rider-dashboard" : "/driver-dashboard";
            navigate(targetPath, { replace: true });
            
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.detail || "Login failed. Please check your credentials.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800">
            <div className="bg-slate-900/80 backdrop-blur-xl p-10 rounded-2xl shadow-xl w-full max-w-md mx-4">
                
                <Link to="/">
                    <h1 className="text-3xl text-white font-bold text-center mb-8">
                        Cab<span className="text-cyan-400">Zy</span>
                    </h1>
                </Link>

                <h2 className="text-2xl text-white text-center font-bold mb-8">
                    Welcome <span className="text-cyan-400">Back</span>
                </h2>

                {/* Error Message */}
                {error && (
                    <div className="bg-red-500/10 border border-red-500 text-red-400 p-3 rounded-lg mb-4 flex items-center gap-2">
                        <AlertCircle className="w-5 h-5" />
                        <span>{error}</span>
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-4">
                    
                    {/* Email */}
                    <div className="relative">
                        <label className="flex items-center gap-2 mb-2 text-white text-lg font-semibold">
                            <Mail className="w-4 h-4" />
                            <span>Ema<span className="text-cyan-400">il</span></span>
                        </label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            required
                            placeholder="Enter your email"
                            className={`w-full p-3 bg-slate-800 rounded-lg text-white outline-none ${
                                error ? 'border-2 border-red-500' : ''
                            }`}
                        />
                    </div>

                    {/* Password */}
                    <div className="relative">
                        <label className="flex items-center gap-2 mb-2 text-white text-lg font-semibold">
                            <Lock className="w-4 h-4" />
                            <span>Passwo<span className="text-cyan-400">rd</span></span>
                        </label>
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            required
                            placeholder="Enter your password"
                            className={`w-full p-3 bg-slate-800 rounded-lg text-white outline-none ${
                                error ? 'border-2 border-red-500' : ''
                            }`}
                        />
                    </div>

                    {/* Sign In Button */}
                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-cyan-500 hover:bg-cyan-600 disabled:bg-cyan-700 disabled:cursor-not-allowed transition rounded-lg p-3 text-white font-semibold hover:cursor-pointer"
                    >
                        {loading ? "Signing In..." : "Sign In"}
                    </button>
                </form>

                {/* Remember Me & Forgot Password */}
                <div className="flex items-center justify-between text-sm mt-6">
                    <label className="flex items-center text-gray-400 cursor-pointer">
                        <input
                            type="checkbox"
                            checked={rememberMe}
                            onChange={(e) => setRememberMe(e.target.checked)}
                            className="mr-2"
                        />
                        Remember Me
                    </label>
                    <Link to="/forgot-password" className="text-cyan-400 hover:underline">
                        Forgot Password?
                    </Link>
                </div>

                {/* Social Login */}
                <div className="text-center text-gray-400 mt-6 text-sm">
                    Or Sign In With
                </div>
                
                <div className="flex gap-4 mt-4">
                    <button className="flex-1 bg-linear-to-br from-[#EA4335] to-[#C5221F] text-white py-2 rounded-lg hover:opacity-90 transition hover:cursor-pointer">
                        Google
                    </button>
                    <button className="flex-1 bg-linear-to-br from-gray-800 to-[#1C1C1E] text-white py-2 rounded-lg hover:opacity-90 transition hover:cursor-pointer">
                        Apple
                    </button>
                </div>

                {/* Sign Up Link */}
                <p className="text-center text-gray-400 text-sm mt-6">
                    Don't have an account?{" "}
                    <Link to="/register" className="text-cyan-400 hover:underline">
                        Sign Up
                    </Link>
                </p>
            </div>
        </div>
    );
}
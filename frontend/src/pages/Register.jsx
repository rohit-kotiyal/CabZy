import { Mail, Lock, User, Phone, UserCircle, AlertCircle } from "lucide-react";
import { Link } from "react-router-dom";
import { useState } from "react";
import OTPVerification from "../components/auth/OTPVerification";
import { registerUser } from "../api/auth";

export default function Register() {

    const [formData, setFormData] = useState({
        name: "",
        role: "rider",
        email: "",
        phone: "",
        password: "",
        confirmPassword: ""
    });
    
    const [showOTP, setShowOTP] = useState(false);
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({});

    const validateForm = () => {
        const newErrors = {};

        // Name validation
        if (!formData.name.trim()) {
            newErrors.name = "Name is required";
        } else if (formData.name.length > 25) {
            newErrors.name = "Name must not exceed 25 characters";
        }

        // Email validation
        if (!formData.email.trim()) {
            newErrors.email = "Email is required";
        } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
            newErrors.email = "Email is invalid";
        }

        // Phone validation
        if (!formData.phone.trim()) {
            newErrors.phone = "Phone number is required";
        } else if (!/^\d{10}$/.test(formData.phone)) {
            newErrors.phone = "Phone number must be exactly 10 digits";
        }

        // Password validation
        if (!formData.password) {
            newErrors.password = "Password is required";
        } else if (formData.password.length < 6) {
            newErrors.password = "Password must be at least 6 characters";
        }

        // Confirm password validation
        if (!formData.confirmPassword) {
            newErrors.confirmPassword = "Please confirm your password";
        } else if (formData.password !== formData.confirmPassword) {
            newErrors.confirmPassword = "Passwords do not match";
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        
        // Restrict name to 25 characters
        if (name === "name" && value.length > 25) {
            return;
        }
        
        // Restrict phone to digits only and 10 characters
        if (name === "phone" && (!/^\d*$/.test(value) || value.length > 10)) {
            return;
        }

        setFormData({
            ...formData,
            [name]: value
        });

        // Clear error for this field when user starts typing
        if (errors[name]) {
            setErrors({
                ...errors,
                [name]: ""
            });
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (!validateForm()) {
            return;
        }

        setLoading(true);
        
        try {
            // Remove confirmPassword before sending to backend
            const { confirmPassword, ...dataToSend } = formData;
            const response = await registerUser(dataToSend); // ✅ FIXED: Added the missing API call
            console.log(response.data);
            setShowOTP(true);
        } catch(err) {
            console.error(err.response?.data?.detail || err.message);
            setErrors({
                submit: err.response?.data?.detail || "Registration Failed"
            });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800">

            <div className="w-full max-w-2xl bg-slate-900/80 backdrop-blur-xl p-10 rounded-2xl shadow-xl">

                <Link to="/">
                    <h1 className="text-3xl text-white font-bold text-center mb-8">
                        Cab<span className="text-cyan-400">Zy</span>
                    </h1>
                </Link>

                <h1 className="text-2xl text-white text-center font-bold mb-8">
                    Join<span className="text-cyan-400"> Us</span>
                </h1>

                {/* Error Message */}
                {errors.submit && (
                    <div className="bg-red-500/10 border border-red-500 text-red-400 p-3 rounded-lg mb-4 flex items-center gap-2">
                        <AlertCircle className="w-5 h-5" />
                        <span>{errors.submit}</span>
                    </div>
                )}

                <form className="space-y-4" onSubmit={handleSubmit}>

                    <div className="grid grid-cols-2 gap-4">

                        {/* Name */}
                        <div className="relative">
                            <label className="flex items-center gap-2 mb-2 text-white text-lg font-semibold">
                                <User className="w-4 h-4" />
                                <span>Na<span className="text-cyan-400">me</span></span>
                            </label>
                            <input
                                type="text"
                                name="name"
                                placeholder="Enter your name"
                                value={formData.name}
                                onChange={handleChange}
                                className={`w-full p-3 bg-slate-800 rounded-lg text-white outline-none ${
                                    errors.name ? 'border-2 border-red-500' : ''
                                }`}
                            />
                            <div className="flex justify-between mt-1">
                                {errors.name && (
                                    <p className="text-red-400 text-xs">{errors.name}</p>
                                )}
                                <p className="text-gray-400 text-xs ml-auto">
                                    {formData.name.length}/25
                                </p>
                            </div>
                        </div>

                        {/* Role */}
                        <div className="relative">
                            <label className="flex items-center gap-2 mb-2 text-white text-lg font-semibold">
                                <UserCircle className="w-4 h-4" />
                                <span>Ro<span className="text-cyan-400">le</span></span>
                            </label>
                            <select 
                                className="w-full p-3 bg-slate-800 rounded-lg text-white outline-none"
                                name="role"
                                value={formData.role}
                                onChange={handleChange}
                            >
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
                            <input
                                type="email"
                                name="email"
                                placeholder="Enter your email"
                                value={formData.email}
                                onChange={handleChange}
                                className={`w-full p-3 bg-slate-800 rounded-lg text-white outline-none ${
                                    errors.email ? 'border-2 border-red-500' : ''
                                }`}
                            />
                            {errors.email && (
                                <p className="text-red-400 text-xs mt-1">{errors.email}</p>
                            )}
                        </div>

                        {/* Contact */}
                        <div className="relative">
                            <label className="flex items-center gap-2 mb-2 text-white text-lg font-semibold">
                                <Phone className="w-4 h-4" />
                                <span>Conta<span className="text-cyan-400">ct</span></span>
                            </label>
                            <input
                                type="tel"
                                name="phone"
                                placeholder="Enter your number"
                                value={formData.phone}
                                onChange={handleChange}
                                className={`w-full p-3 bg-slate-800 rounded-lg text-white outline-none ${
                                    errors.phone ? 'border-2 border-red-500' : ''
                                }`}
                            />
                            <div className="flex justify-between mt-1">
                                {errors.phone && (
                                    <p className="text-red-400 text-xs">{errors.phone}</p>
                                )}
                                <p className="text-gray-400 text-xs ml-auto">
                                    {formData.phone.length}/10
                                </p>
                            </div>
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
                                placeholder="Enter your password"
                                value={formData.password}
                                onChange={handleChange}
                                className={`w-full p-3 bg-slate-800 rounded-lg text-white outline-none ${
                                    errors.password ? 'border-2 border-red-500' : ''
                                }`}
                            />
                            {errors.password && (
                                <p className="text-red-400 text-xs mt-1">{errors.password}</p>
                            )}
                        </div>

                        {/* Confirm Password */}
                        <div className="relative">
                            <label className="flex items-center gap-2 mb-2 text-white text-lg font-semibold">
                                <Lock className="w-4 h-4" />
                                <span>Confirm <span className="text-cyan-400">Password</span></span>
                            </label>
                            <input
                                type="password"
                                name="confirmPassword"
                                placeholder="Confirm password"
                                value={formData.confirmPassword}
                                onChange={handleChange}
                                className={`w-full p-3 bg-slate-800 rounded-lg text-white outline-none ${
                                    errors.confirmPassword ? 'border-2 border-red-500' : ''
                                }`}
                            />
                            {errors.confirmPassword && (
                                <p className="text-red-400 text-xs mt-1">{errors.confirmPassword}</p>
                            )}
                        </div>

                    </div>

                    {/* Register Button */}
                    <button 
                        type="submit" 
                        disabled={loading}
                        className="w-full bg-cyan-500 hover:bg-cyan-600 disabled:bg-cyan-700 hover:cursor-pointer transition rounded-lg p-3 text-white font-semibold"
                    >
                        {loading ? "Creating Account..." : "Sign Up"}
                    </button>

                </form>

                <div className="text-center text-gray-400 mt-6 text-sm">
                    Or Sign Up With
                </div>

                <div className="flex gap-4 mt-4">
                    <button className="flex-1 bg-gradient-to-br from-[#EA4335] to-[#C5221F] text-white py-2 rounded-lg hover:opacity-90 transition">
                        Google
                    </button>

                    <button className="flex-1 bg-gradient-to-br from-gray-800 to-[#1C1C1E] text-white py-2 rounded-lg hover:opacity-90 transition">
                        Apple
                    </button>
                </div>

                <p className="text-center text-gray-400 text-sm mt-6">
                    Already have an account?{" "}
                    <Link to="/login" className="text-cyan-400 hover:underline">
                        Sign In
                    </Link>
                </p>

            </div>

            {/* OTP Modal */}
            <OTPVerification
                isOpen={showOTP}
                onClose={() => setShowOTP(false)}
                email={formData.email}
            />

        </div>
    );
}
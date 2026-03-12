import { useState } from "react";
import { AlertCircle } from "lucide-react";
import { verifyOTP, getCurrentUser } from "../../api/auth";

export default function OTPVerification({ isOpen, onClose, email }) {
    const [otp, setOtp] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleVerify = async () => {
        if (!otp || otp.length !== 6) {
            setError("Please enter a valid 6-digit OTP");
            return;
        }

        setLoading(true);
        setError("");

        try {
            console.log("1. Verifying OTP...");
            const response = await verifyOTP({ email, otp });
            const token = response.data.access_token;
            
            console.log("2. Token received:", token);
            // Store token
            localStorage.setItem("token", token);
            
            console.log("3. Fetching user data...");
            // Fetch user data to determine role
            const userResponse = await getCurrentUser();
            const userRole = userResponse.data.role;
            
            console.log("4. User role:", userRole);
            console.log("5. Navigating to dashboard...");
            
            // Close modal
            onClose();
            
            // ✅ Use window.location.href for hard reload
            // This ensures AuthContext picks up the token
            if (userRole === "rider") {
                window.location.href = "/rider-dashboard";
            } else if (userRole === "driver") {
                window.location.href = "/driver-dashboard";
            }
            
        } catch (err) {
            console.error("OTP Verification Error:", err);
            setError(err.response?.data?.detail || "Invalid or Expired OTP");
        } finally {
            setLoading(false);
        }
    };

    const handleOtpChange = (e) => {
        const value = e.target.value.replace(/\D/g, "");
        if (value.length <= 6) {
            setOtp(value);
            setError("");
        }
    };

    const handleResendOTP = async () => {
        // TODO: Implement resend OTP logic
        console.log("Resend OTP to:", email);
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 flex items-center justify-center bg-slate-900/80 backdrop-blur-sm z-50">
            <div className="bg-slate-900 p-8 rounded-xl w-full max-w-md mx-4 shadow-xl border border-slate-800">
                
                <h2 className="text-2xl text-white font-bold text-center mb-2">
                    Verify <span className="text-cyan-400">OTP</span>
                </h2>
                
                <p className="text-gray-400 text-center mb-6 text-sm">
                    Enter the 6-digit code sent to <br />
                    <span className="text-cyan-400">{email}</span>
                </p>

                {error && (
                    <div className="bg-red-500/10 border border-red-500 text-red-400 p-3 rounded-lg mb-4 flex items-center gap-2">
                        <AlertCircle className="w-4 h-4" />
                        <span className="text-sm">{error}</span>
                    </div>
                )}

                <input
                    type="text"
                    inputMode="numeric"
                    value={otp}
                    onChange={handleOtpChange}
                    placeholder="Enter 6-digit OTP"
                    maxLength={6}
                    className={`w-full p-4 bg-slate-800 rounded-lg text-white outline-none text-center text-2xl tracking-widest mb-4 ${
                        error ? 'border-2 border-red-500' : 'border-2 border-transparent focus:border-cyan-500'
                    }`}
                    autoFocus
                />

                <p className="text-gray-400 text-xs text-center mb-4">
                    {otp.length}/6 digits entered
                </p>

                <button
                    onClick={handleVerify}
                    disabled={loading || otp.length !== 6}
                    className="w-full bg-cyan-500 hover:bg-cyan-600 disabled:bg-cyan-700 disabled:cursor-not-allowed mt-2 p-3 rounded-lg text-white font-semibold transition"
                >
                    {loading ? "Verifying..." : "Verify OTP"}
                </button>

                <div className="flex justify-between mt-6 text-sm">
                    <button
                        onClick={handleResendOTP}
                        className="text-gray-400 hover:text-cyan-400 transition"
                    >
                        Resend OTP
                    </button>

                    <button
                        onClick={onClose}
                        className="text-red-400 hover:text-red-300 transition"
                    >
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    );
}
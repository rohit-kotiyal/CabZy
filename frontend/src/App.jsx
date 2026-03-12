import { Route, Routes, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/authContext";
import ProtectedRoutes from "./components/ProtectedRoutes"; 
import LandingPage from "./pages/LandingPage";
import Login from "./pages/Login";
import Register from "./pages/Register";
import RiderDashboard from "./pages/RiderDashboard";
import DriverDashboard from "./pages/DriverDashboard";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      
      {/* PROTECTED ROUTES - Wrapped individually */}
      <Route
        path="/rider-dashboard"
        element={
          <AuthProvider>
            <ProtectedRoutes allowedRoles={["rider"]}>
              <RiderDashboard />
            </ProtectedRoutes>
          </AuthProvider>
        }
      />
      
      <Route
        path="/driver-dashboard"
        element={
          <AuthProvider>
            <ProtectedRoutes allowedRoles={["driver"]}>
              <DriverDashboard />
            </ProtectedRoutes>
          </AuthProvider>
        }
      />
      
      {/* UNAUTHORIZED PAGE */}
      <Route 
        path="/unauthorized" 
        element={
          <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-slate-900 to-slate-800">
            <div className="text-white text-center">
              <h1 className="text-4xl font-bold mb-4">Unauthorized Access</h1>
              <p className="text-gray-400">You don't have permission to access this page.</p>
            </div>
          </div>
        } 
      />
    </Routes>
  );
}
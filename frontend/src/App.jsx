import { Route, Routes, Navigate } from "react-router-dom";
import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";
import useAuthStore from "./store/authStore";


export default function App(){
  const token = useAuthStore((state) => state.token);

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* redirect root to login if not logged in */}
      <Route path="/" element={
        token ? <Navigate to="/dashboard" /> : <Navigate to="/login" />
      } /> 
    </Routes>
  );
}
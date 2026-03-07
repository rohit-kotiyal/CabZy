import Navbar from "../components/landing/Navbar";
import Hero from "../components/landing/Hero";
import Footer from "../components/landing/Footer";
export default function LandingPage(){
    return (
        <div className="relative min-h-screen bg-gray-900">
            <Navbar />
            <Hero />
            <Footer />
        </div>
    );
}
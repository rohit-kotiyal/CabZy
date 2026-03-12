import axios from "axios";

const API = axios.create({
    baseURL: "http://127.0.0.1:8000",
});


// Add Token to every request
API.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("token");
        if (token){
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    }, (error) => {
        return Promise.reject(error);
    }
);

// Handle Token expiration
API.interceptors.response.use(
    (response) => response,
    (error) => {
        if(error.response?.status === 401){
            // Token expired or invalid
            localStorage.removeItem("token");
            window.location.href = "/login";
        }
        return Promise.reject(error);
    }
);


export default API;



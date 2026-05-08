import axios from "axios";


const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1',
})


// attach access token to every request automatically
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token')
    if (token){
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})


// if access token expires, refresh automatically
api.interceptors.response.use((response) => response,
    async(error) => {
        const original = error.config

        if(error.response?.status === 401 && !original._retry){
            original._retry = true
            
            try{
                const refresh = localStorage.getItem('refresh_token')
                const res = await axios.post(
                    'http://127.0.0.1:8000/api/v1/auth/token/refresh',
                    {refresh}
                )
                const newAccess = res.data.access
                localStorage.setItem('access_token', newAccess)
                original.headers.Authorization = `Bearer ${newAccess}`
                return api(original)
                } catch{
                localStorage.clear()
                window.location.href = '/login'
            }
        }
        return Promise.reject(error)
    }
)

export default api;
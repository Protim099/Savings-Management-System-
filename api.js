import axios from 'axios'
const api = axios.create({baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api'})
api.interceptors.request.use(c=>{const t=localStorage.getItem('access'); if(t)c.headers.Authorization=`Bearer ${t}`; return c})
export default api

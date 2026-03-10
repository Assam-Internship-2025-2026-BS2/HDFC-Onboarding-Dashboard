
import axios from "axios";

const API = import.meta.env.VITE_API_URL || "/api";

export const getDashboard = async (filters)=>{
 const res = await axios.get(`${API}/executive/dashboard`,{params:filters})
 return res.data
}

export const getMatrix = async (filters)=>{
 const res = await axios.get(`${API}/dashboard/stage-dropoff`,{params:filters})
 return res.data
}


import axios from "axios";

const API = "http://127.0.0.1:8000/api";

export const getDashboard = async (filters)=>{
 const res = await axios.get(`${API}/executive/dashboard`,{params:filters})
 return res.data
}

export const getMatrix = async (filters)=>{
 const res = await axios.get(`${API}/dashboard/stage-dropoff`,{params:filters})
 return res.data
}

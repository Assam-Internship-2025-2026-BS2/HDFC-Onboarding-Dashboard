import axios from "axios";

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api";

// Auto-retry interceptor for Network Errors (Connection Refused)
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const { config, message } = error;
    if (!config) return Promise.reject(error);
    
    // Set up retry states
    if (!config.retryCount) config.retryCount = 0;
    
    // Only retry on Network Errors up to 3 times
    if (message === 'Network Error' && config.retryCount < 3) {
      config.retryCount += 1;
      
      // Exponential backoff: 1s, 2s, 3s...
      const delay = new Promise((resolve) => setTimeout(resolve, config.retryCount * 1000));
      await delay;
      return axios(config);
    }
    return Promise.reject(error);
  }
);

export const getDashboard = async (filters)=>{
 const res = await axios.get(`${API}/executive/dashboard`,{params:filters})
 return res.data
}

export const getMatrix = async (filters)=>{
 const res = await axios.get(`${API}/v1/dashboard/stage-dropoff`,{params:filters})
 return res.data
}

export const getProducts = async (filters) => {
  const res = await axios.get(`${API}/v1/products/`, {params: filters})
  return res.data
}

export const getInsights = async (filters) => {
  const res = await axios.get(`${API}/v1/insights/`, {params: filters})
  return res.data
}

export const getAnalysis = async (filters) => {
  const res = await axios.get(`${API}/v1/analysis/`, { params: filters })
  return res.data
}

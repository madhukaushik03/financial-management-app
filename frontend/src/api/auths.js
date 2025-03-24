import axios from "axios";
const API_BASE_URL = "http://127.0.0.1:5000"; // Flask Backend URL

export const registerUser = async (username, password) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/register`, { username, password });
    return response.data;
  } catch (error) {
    return { error: error.response?.data?.message || "Registration failed" };
  }
};

export const loginUser = async (username, password) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/login`, { username, password });
    localStorage.setItem("token", response.data.token); // Store token
    return response.data;
  } catch (error) {
    return { error: error.response?.data?.message || "Login failed" };
  }
};

import axios from "axios";
const API_BASE_URL = "http://127.0.0.1:5000"; // Flask Backend URL

export const addExpense = async (amount, category, date) => {
  try {
    const token = localStorage.getItem("token");
    const response = await axios.post(
      `${API_BASE_URL}/expense`,
      { amount, category, date },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    return response.data;
  } catch (error) {
    return { error: error.response?.data?.message || "Failed to add expense" };
  }
};

export const getExpenses = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/expenses`);
    return response.data;
  } catch (error) {
    return { error: error.response?.data?.message || "Failed to fetch expenses" };
  }
};

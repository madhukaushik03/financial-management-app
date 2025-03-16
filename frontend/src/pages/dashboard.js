import React, { useState, useEffect } from "react";
import axios from "axios";

const Dashboard = () => {
  const [predictedExpense, setPredictedExpense] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/predict")
      .then((res) => {
        console.log("API Response:", res.data);  // 🔍 Debugging line

        if (res.data.predicted_spending) {
          setPredictedExpense(res.data.predicted_spending);
        } else {
          setError("Not enough data to predict");
        }
      })
      .catch((err) => {
        console.error("Error fetching prediction:", err);
        setError("Error fetching prediction");
      });
  }, []);

  return (
    <div>
      <h2>AI-Based Expense Prediction</h2>
      {error ? (
        <p style={{ color: "red" }}>{error}</p>
      ) : (
        <p>Predicted Spending Next Month: ₹{predictedExpense}</p>
      )}
    </div>
  );
};

export default Dashboard;

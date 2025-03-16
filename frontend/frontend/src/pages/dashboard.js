import React, { useState, useEffect } from "react";
import axios from "axios";

const Dashboard = () => {
  const [expenses, setExpenses] = useState([]);
  const [predictedSpending, setPredictedSpending] = useState(null);
  const [newExpense, setNewExpense] = useState({ category: "", amount: "", date: "" });

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/expenses").then(res => setExpenses(res.data));
    axios.get("http://127.0.0.1:5000/predict").then(res => setPredictedSpending(res.data.predicted_spending));
  }, []);

  const addExpense = () => {
    axios.post("http://127.0.0.1:5000/expense", newExpense).then(() => {
      setExpenses([...expenses, newExpense]);
      setNewExpense({ category: "", amount: "", date: "" });
    });
  };

  return (
    <div>
      <h2>Dashboard</h2>
      <p>Predicted Spending Next Month: ₹{predictedSpending}</p>
      
      <input type="text" placeholder="Category" onChange={(e) => setNewExpense({ ...newExpense, category: e.target.value })} />
      <input type="number" placeholder="Amount" onChange={(e) => setNewExpense({ ...newExpense, amount: e.target.value })} />
      <input type="date" onChange={(e) => setNewExpense({ ...newExpense, date: e.target.value })} />
      <button onClick={addExpense}>Add Expense</button>
      
      <ul>
        {expenses.map((exp, index) => <li key={index}>{exp.category} - ₹{exp.amount}</li>)}
      </ul>
    </div>
  );
};

export default Dashboard;

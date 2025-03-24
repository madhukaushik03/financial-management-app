import React, { useEffect, useState } from "react";
import { getExpenses } from "../api/expenses"; // ✅ Corrected import
import { Bar } from "react-chartjs-2";
import "../styles/Expenses.css";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const Expenses = () => {
  const [expenses, setExpenses] = useState([]);

  useEffect(() => {
    const fetchExpenses = async () => {
      const data = await getExpenses();
      if (!data.error) setExpenses(data);
    };
    fetchExpenses();
  }, []);

  const chartData = {
    labels: expenses.map((e) => e.category),
    datasets: [
      {
        label: "Expense Amount",
        data: expenses.map((e) => e.amount),
        backgroundColor: "rgba(75,192,192,0.6)",
      },
    ],
  };

  return (
    <div className="expenses-container">
      <h2>Expenses</h2>
      <table>
        <thead>
          <tr><th>Date</th><th>Category</th><th>Amount</th></tr>
        </thead>
        <tbody>
          {expenses.map((e, index) => (
            <tr key={index}>
              <td>{e.date}</td>
              <td>{e.category}</td>
              <td>₹{e.amount}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="chart-container">
        <Bar data={chartData} />
      </div>
    </div>
  );
};

export default Expenses;

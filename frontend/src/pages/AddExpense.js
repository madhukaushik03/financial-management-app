import React, { useState } from "react";
import { addExpense } from "../api/expenses"; // ✅ Corrected import
import "../styles/AddExpense.css";

const AddExpense = () => {
  const [amount, setAmount] = useState("");
  const [category, setCategory] = useState("");
  const [date, setDate] = useState("");
  const [message, setMessage] = useState("");

  const handleAddExpense = async () => {
    const response = await addExpense(amount, category, date);
    setMessage(response.error || "✅ Expense added successfully!");
    if (!response.error) {
      setAmount(""); setCategory(""); setDate("");
    }
  };

  return (
    <div className="expense-container">
      <h2>Add Expense</h2>
      <input type="number" placeholder="Amount" value={amount} onChange={(e) => setAmount(e.target.value)} />
      <input placeholder="Category" value={category} onChange={(e) => setCategory(e.target.value)} />
      <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
      <button onClick={handleAddExpense}>Add Expense</button>
      <p>{message}</p>
    </div>
  );
};

export default AddExpense;

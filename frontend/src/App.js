import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import Navbar from "./Navbar.js";
import Login from "./pages/Login.js";
import Signup from "./pages/Signup.js";
import Dashboard from "./pages/Dashboard.js";
import Auth from "./pages/Auth.js";
import AddExpense from "./pages/AddExpense";
import Expenses from "./pages/Expenses.js";

function App() {
  const [token, setToken] = useState(null);

  return (
    <Router>
      <Navbar />  {/* ✅ Navbar should be inside Router */}
      
      {/* ✅ Navigation Links */}
      <nav>
        <Link to="/">Login</Link>
        <Link to="/signup">Signup</Link>
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/add-expense">Add Expense</Link>
        <Link to="/expenses">View Expenses</Link>
      </nav>

      {/* ✅ Correct Routes Setup */}
      <Routes>
        <Route path="/" element={<Auth />} />
        <Route path="/login" element={<Login setToken={setToken} />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/dashboard" element={<Dashboard token={token} />} />
        <Route path="/add-expense" element={<AddExpense />} />
        <Route path="/expenses" element={<Expenses />} />
      </Routes>
    </Router>
  );
}

export default App;

import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./Navbar.js";
import Login from "./pages/login.js";
import Signup from "./pages/signup.js";
import Dashboard from "./pages/dashboard.js";

function App() {
// eslint-disable-next-line
const [token, setToken] = useState(null);


  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/login" element={<Login setToken={setToken} />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default App;


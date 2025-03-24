import React, { useState } from "react";
import "../styles/Auth.css"; // Add CSS for styling
import { registerUser, loginUser } from "../api/auths"; 


const Auth = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleAuth = async () => {
    const response = isLogin
      ? await loginUser(username, password)
      : await registerUser(username, password);
    if (response.token) {
      localStorage.setItem("token", response.token);
      setMessage("✅ Success!");
      window.location.href = "/add-expense"; // Redirect after login
    } else {
      setMessage(response.error || "Something went wrong");
    }
  };

  return (
    <div className="auth-container">
      <h2>{isLogin ? "Login" : "Register"}</h2>
      <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleAuth}>{isLogin ? "Login" : "Register"}</button>
      <p>{message}</p>
      <button className="switch-btn" onClick={() => setIsLogin(!isLogin)}>
        {isLogin ? "Need an account? Register" : "Already have an account? Login"}
      </button>
    </div>
  );
};

export default Auth;

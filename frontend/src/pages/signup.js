import React, { useState } from "react";
import { Container, TextField, Button, Typography } from "@mui/material";
import axios from "axios";

const Signup = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSignup = async () => {
    try {
      await axios.post("http://127.0.0.1:5000/register", { username, password });
      alert("User registered successfully!");
    } catch (err) {
      alert("Signup failed: " + err.response.data.message);
    }
  };

  return (
    <Container maxWidth="sm" style={{ marginTop: "50px", textAlign: "center" }}>
      <Typography variant="h4">Sign Up</Typography>
      <TextField fullWidth label="Username" margin="normal" onChange={(e) => setUsername(e.target.value)} />
      <TextField fullWidth label="Password" type="password" margin="normal" onChange={(e) => setPassword(e.target.value)} />
      <Button variant="contained" color="primary" onClick={handleSignup}>Sign Up</Button>
    </Container>
  );
};

export default Signup;

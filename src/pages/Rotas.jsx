// src/Rotas.jsx
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
//import Login from "./pages/Login";
//import Dashboard from "./pages/Dashboard";
//import Desafios from "./pages/Desafios";
//import Leaderboard from "./pages/Leaderboard";
//import Analytics from "./pages/Analytics"; // novo
//import { isAuthenticated } from "./api/auth";

export default function Rotas() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={isAuthenticated() ? <Dashboard /> : <Navigate to="/login" />} />
        <Route path="/desafios" element={isAuthenticated() ? <Desafios /> : <Navigate to="/login" />} />
        <Route path="/leaderboard" element={isAuthenticated() ? <Leaderboard /> : <Navigate to="/login" />} />
        <Route path="/analytics" element={isAuthenticated() ? <Analytics /> : <Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

import React, { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';

import Header from "./components/Header";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Desafios from "./pages/Desafios";
import Submissao from "./pages/Submissao";
import Ranking from "./pages/Ranking";
import Analitico from "./pages/Analitico";
import Rotas from "./pages/Rotas";
import ListaDeRotas from "./pages/ListaDeRotas";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    setIsAuthenticated(!!token);
  }, []);

  const handleLogin = () => setIsAuthenticated(true);
  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setIsAuthenticated(false);
  };

  return (
    <BrowserRouter>
      <Header onLogout={handleLogout} />

      <Routes>
        {/* Login route */}
        <Route
          path="/"
          element={
            isAuthenticated ? (
              <Navigate to="/dashboard" />
            ) : (
              <Login onLogin={handleLogin} />
            )
          }
        />

        {/* Protected routes */}
        <Route
          path="/dashboard"
          element={
            isAuthenticated ? (
              <Dashboard onLogout={handleLogout} />
            ) : (
              <Navigate to="/" />
            )
          }
        />
        <Route
          path="/rotas/:endpoint"
          element={isAuthenticated ? <Rotas /> : <Navigate to="/" />}
        />
        <Route
          path="/rotas"
          element={isAuthenticated ? <ListaDeRotas /> : <Navigate to="/" />}
        />
        <Route
          path="/submissao/:id"
          element={isAuthenticated ? <Submissao /> : <Navigate to="/" />}
        />
        <Route
          path="/ranking"
          element={isAuthenticated ? <Ranking /> : <Navigate to="/" />}
        />
        <Route
          path="/analitico"
          element={isAuthenticated ? <Analitico /> : <Navigate to="/" />}
        />
      </Routes>

      <ToastContainer
        position="top-right"
        autoClose={4000}
        hideProgressBar={false}
        closeOnClick
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
      />
    </BrowserRouter>
  );
}

export default App;

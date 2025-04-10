import React from "react";
import { Link, useLocation } from "react-router-dom";
<>
  <Link to="/analitico">📊 Análise</Link>
  <Link to="/rotas">📚 Rotas</Link>
</>


const Header = ({ onLogout }) => {
  const location = useLocation();
  const isLoggedIn = !!localStorage.getItem("access_token");

  return (
    <nav className="bg-slate-800 text-white p-4 flex justify-between items-center">
      <span className="font-bold text-lg">Pulso do Mercado</span>

      {isLoggedIn && (
        <div className="space-x-4 flex items-center">
          <Link
            to="/dashboard"
            className={location.pathname === "/dashboard" ? "underline text-yellow-300" : ""}
          >
            Dashboard
          </Link>
          <Link
            to="/desafios"
            className={location.pathname === "/desafios" ? "underline text-yellow-300" : ""}
          >
            Desafios
          </Link>
          <Link
            to="/ranking"
            className={location.pathname === "/ranking" ? "underline text-yellow-300" : ""}
          >
            Ranking
          </Link>

          <button
            onClick={onLogout}
            className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded"
          >
            Sair
          </button>
        </div>
      )}
    </nav>
  );
};

export default Header;

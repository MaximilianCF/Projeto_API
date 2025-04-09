import React from "react";
import { Link } from "react-router-dom";

const Header = () => (
  <nav className="bg-slate-800 text-white p-4 flex justify-between">
    <span className="font-bold">Pulso do Mercado</span>
    <div className="space-x-4">
      <Link to="/dashboard">Dashboard</Link>
      <Link to="/desafios">Desafios</Link>
      <Link to="/ranking">Ranking</Link>
    </div>
  </nav>
);

export default Header;
import React from "react";
import { Link } from "react-router-dom";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

const Dashboard = ({ onLogout }) => {
  const dadosMock = [
    { titulo: "Inflação", media: 80 },
    { titulo: "Selic", media: 72 },
    { titulo: "PIB", media: 65 },
  ];

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-3xl mx-auto bg-white rounded-lg shadow-md p-8">
        <h1 className="text-3xl font-bold mb-4 text-gray-800">Painel do Usuário</h1>
        <p className="mb-6 text-gray-600">Escolha uma das opções abaixo:</p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <Link
            to="/desafios"
            className="block bg-blue-600 hover:bg-blue-700 text-white text-center py-4 rounded-lg shadow transition"
          >
            📋 Ver Desafios
          </Link>

          <Link
            to="/ranking"
            className="block bg-green-600 hover:bg-green-700 text-white text-center py-4 rounded-lg shadow transition"
          >
            🏆 Ver Ranking
          </Link>

          <Link
            to="/analitico"
            className="block bg-purple-600 hover:bg-purple-700 text-white text-center py-4 rounded-lg shadow transition"
          >
            📊 Análise Visual
          </Link>

          <button
            onClick={onLogout}
            className="block bg-red-600 hover:bg-red-700 text-white text-center py-4 rounded-lg shadow transition col-span-1 sm:col-span-2"
          >
            🚪 Sair da Plataforma
          </button>
        </div>

        {/* Gráfico de barras */}
        <div className="mt-10">
          <h3 className="text-lg font-semibold mb-2 text-gray-700">
            Desafios com maior média de acertos
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={dadosMock}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="titulo" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="media" fill="#6366f1" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

const Analitico = () => {
  const [dados, setDados] = useState([]);
  const [porDesafio, setPorDesafio] = useState([]);

  useEffect(() => {
    // Dados mock — substitua por API futuramente
    setDados([
      { data: "01/04", score: 60 },
      { data: "02/04", score: 72 },
      { data: "03/04", score: 85 },
      { data: "04/04", score: 78 },
      { data: "05/04", score: 90 },
    ]);

    setPorDesafio([
      { titulo: "Inflação", media: 80 },
      { titulo: "Selic", media: 74 },
      { titulo: "PIB", media: 68 },
    ]);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-5xl mx-auto bg-white shadow rounded-lg p-8 space-y-12"
      >
        <h1 className="text-3xl font-bold text-gray-800">📊 Análise de Performance</h1>

        {/* Evolução da pontuação */}
        <div>
          <h2 className="text-xl font-semibold mb-3 text-gray-700">Evolução da Pontuação</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={dados}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="data" />
                <YAxis />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="score"
                  stroke="#10b981"
                  strokeWidth={3}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Média por desafio */}
        <div>
          <h2 className="text-xl font-semibold mb-3 text-gray-700">Média por Desafio</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={porDesafio}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="titulo" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="media" fill="#6366f1" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Analitico;

import React, { useEffect, useState } from "react";
import api from "../api/client";
import { toast } from "react-toastify";
import { motion } from "framer-motion";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

const Ranking = () => {
  const [ranking, setRanking] = useState([]);

  useEffect(() => {
    const fetchRanking = async () => {
      try {
        const response = await api.get("/leaderboard");
        setRanking(response.data);
      } catch (err) {
        console.error("Erro ao carregar ranking:", err);
        toast.error("❌ Não foi possível carregar o ranking.");
      }
    };

    fetchRanking();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-4xl mx-auto bg-white shadow-md rounded-lg p-8"
      >
        <h1 className="text-3xl font-bold mb-6 text-gray-800">🏆 Ranking de Desempenho</h1>

        {ranking.length === 0 ? (
          <p className="text-gray-600">Nenhum dado de ranking disponível.</p>
        ) : (
          <>
            {/* Tabela */}
            <div className="overflow-x-auto mb-10">
              <table className="min-w-full border border-gray-200 rounded-md">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="py-2 px-4 border-b text-left">#</th>
                    <th className="py-2 px-4 border-b text-left">Usuário</th>
                    <th className="py-2 px-4 border-b text-left">Pontuação</th>
                  </tr>
                </thead>
                <tbody>
                  {ranking.map((item, index) => (
                    <tr key={item.usuario_id || index} className="hover:bg-gray-50">
                      <td className="py-2 px-4 border-b">{index + 1}</td>
                      <td className="py-2 px-4 border-b">{item.usuario || "Anônimo"}</td>
                      <td className="py-2 px-4 border-b">{item.pontuacao || 0}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Gráfico de barras */}
            <div className="w-full h-96">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={ranking}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="usuario" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="pontuacao" fill="#3b82f6" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </>
        )}
      </motion.div>
    </div>
  );
};

export default Ranking;

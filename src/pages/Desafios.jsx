import React, { useEffect, useState } from "react";
import api from "../api/client";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";
import { motion } from "framer-motion";

const Desafios = () => {
  const [desafios, setDesafios] = useState([]);

  useEffect(() => {
    const fetchDesafios = async () => {
      try {
        const response = await api.get("/desafios");
        setDesafios(response.data);
      } catch (err) {
        console.error("Erro ao buscar desafios:", err);
        toast.error("❌ Erro ao carregar desafios.");
      }
    };

    fetchDesafios();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-4xl mx-auto"
      >
        <h1 className="text-3xl font-bold text-gray-800 mb-6">📋 Desafios Disponíveis</h1>

        {desafios.length === 0 ? (
          <p className="text-gray-600">Nenhum desafio disponível no momento.</p>
        ) : (
          <div className="space-y-4">
            {desafios.map((desafio) => (
              <div
                key={desafio.id}
                className="bg-white rounded-lg shadow-md p-6 border border-gray-200"
              >
                <h2 className="text-xl font-semibold text-gray-800 mb-2">
                  {desafio.titulo || desafio.nome}
                </h2>
                <p className="text-gray-600">{desafio.descricao}</p>
                <Link
                  to={`/submissao/${desafio.id}`}
                  className="inline-block mt-4 text-blue-600 hover:underline font-medium"
                >
                  Enviar Solução →
                </Link>
              </div>
            ))}
          </div>
        )}
      </motion.div>
    </div>
  );
};

export default Desafios;

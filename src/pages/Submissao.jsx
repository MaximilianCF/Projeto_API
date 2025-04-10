import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api/client";
import { toast } from "react-toastify";
import { motion } from "framer-motion";

const Submissao = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [resposta, setResposta] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post("/submissoes", {
        desafio_id: parseInt(id),
        resposta,
      });
      toast.success("✅ Submissão enviada com sucesso!");
      setTimeout(() => navigate("/dashboard"), 2000);
    } catch (err) {
      console.error(err);
      toast.error("❌ Erro ao enviar a submissão.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6 flex items-center justify-center">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-white shadow-md rounded-lg p-8 w-full max-w-2xl"
      >
        <h1 className="text-2xl font-bold mb-4 text-gray-800">
          Submissão para o Desafio #{id}
        </h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <label htmlFor="resposta" className="block text-sm font-medium text-gray-700">
            Sua resposta, link ou explicação
          </label>
          <textarea
            id="resposta"
            value={resposta}
            onChange={(e) => setResposta(e.target.value)}
            required
            className="w-full h-32 p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />

          <button
            type="submit"
            disabled={loading}
            className={`bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition ${
              loading ? "opacity-50 cursor-not-allowed" : ""
            }`}
          >
            {loading ? "Enviando..." : "Enviar Submissão"}
          </button>
        </form>
      </motion.div>
    </div>
  );
};

export default Submissao;

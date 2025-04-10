import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { rotas } from "../data/rotas";

const ListaDeRotas = () => {
  const chaves = Object.keys(rotas);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-5xl mx-auto bg-white shadow-md rounded-lg p-8"
      >
        <h1 className="text-3xl font-bold text-gray-800 mb-6">📚 Rotas disponíveis</h1>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {chaves.map((chave) => (
            <Link
              to={`/rotas/${chave}`}
              key={chave}
              className="block bg-blue-100 hover:bg-blue-200 border-l-4 border-blue-500 p-4 rounded shadow transition"
            >
              <h2 className="text-lg font-semibold text-blue-800">
                {rotas[chave].nome}
              </h2>
              <p className="text-sm text-gray-600 mt-1">
                {rotas[chave].descricao}
              </p>
              <p className="text-xs text-gray-500 mt-2 font-mono">{rotas[chave].rota}</p>
            </Link>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default ListaDeRotas;

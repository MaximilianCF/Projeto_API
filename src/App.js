import React, { useState } from "react";

/**
 * Pulso do Mercado - Wireframe MVP
 * --------------------------------
 * Este código exibe um layout estático simulando o fluxo de:
 * 1. Pergunta -> 2. Botão Consultar -> 3. Card de Resposta -> 4. Gráfico placeholder
 * + Seção explicando "Por que é melhor do que ChatGPT sozinho?".
 *
 * Para rodar:
 *  - npx create-react-app pulso-wireframe
 *  - Substitua o conteúdo do src/App.js por ESTE código
 *  - npm start
 */

function App() {
  // Estado local apenas para demonstrar a digitação da pergunta e a “resposta”
  const [inputValue, setInputValue] = useState("");
  const [aiResponse, setAiResponse] = useState("");
  const [showResponse, setShowResponse] = useState(false);

  function handleSubmit() {
    if (inputValue.trim() === "") return;
    // Simula uma resposta fixa da “IA”
    const mockAnswer = `A inflação (IPCA) está em aproximadamente 5,6% nos últimos 12 meses. (Exemplo de resposta fictícia)`;
    setAiResponse(mockAnswer);
    setShowResponse(true);
  }

  return (
    <div style={styles.container}>
      {/* Cabeçalho */}
      <header style={styles.header}>
        <h1 style={styles.title}>Pulso do Mercado</h1>
        <p style={styles.subtitle}>API + IA para dados econômicos brasileiros</p>
      </header>

      {/* Campo de Pergunta */}
      <div style={styles.inputContainer}>
        <input
          style={styles.input}
          type="text"
          placeholder="Como está a inflação?"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
        />
        <button style={styles.button} onClick={handleSubmit}>
          Consultar
        </button>
      </div>

      {/* Card de Resposta */}
      {showResponse && (
        <div style={styles.card}>
          <h2>Resposta</h2>
          <p>{aiResponse}</p>
        </div>
      )}

      {/* Espaço para Gráfico */}
      {showResponse && (
        <div style={styles.chartPlaceholder}>
          <p>[Gráfico do IPCA acumulado]</p>
        </div>
      )}

      {/* Botões de Exportação (desabilitados) */}
      {showResponse && (
        <div style={styles.exportButtons}>
          <button style={styles.disabledButton} disabled>
            Exportar p/ Notion
          </button>
          <button style={styles.disabledButton} disabled>
            Exportar p/ Sheets
          </button>
          <button style={styles.disabledButton} disabled>
            Enviar p/ Telegram
          </button>
        </div>
      )}

      {/* Seção "Por que isso é melhor que ChatGPT sozinho?" */}
      <section style={styles.whyBetterSection}>
        <h3 style={styles.whyBetterTitle}>
          Por que isso é melhor do que ChatGPT sozinho?
        </h3>
        <ul style={styles.whyBetterList}>
          <li>Dados reais e atualizados (Bacen, Ipea, IBGE).</li>
          <li>Integrações futuras com Notion, Sheets, Telegram.</li>
          <li>Foco total em economia brasileira.</li>
        </ul>
      </section>

      {/* Rodapé */}
      <footer style={styles.footer}>
        <p>© 2023 Pulso do Mercado</p>
      </footer>
    </div>
  );
}

// Estilos inline para simplificar
const styles = {
  container: {
    fontFamily: "sans-serif",
    color: "#333",
    maxWidth: "600px",
    margin: "0 auto",
    padding: "1rem",
  },
  header: {
    textAlign: "center",
    marginBottom: "1rem",
    backgroundColor: "#0E2A3A",
    color: "#FFF",
    padding: "1.5rem",
    borderRadius: "8px",
  },
  title: {
    fontSize: "2rem",
    margin: 0,
  },
  subtitle: {
    fontSize: "1rem",
    margin: "0.5rem 0 0 0",
  },
  inputContainer: {
    display: "flex",
    gap: "0.5rem",
    marginBottom: "1rem",
    justifyContent: "center",
  },
  input: {
    flex: 1,
    padding: "0.5rem",
    fontSize: "1rem",
    borderRadius: "4px",
    border: "1px solid #ccc",
  },
  button: {
    backgroundColor: "#1E8FBB",
    color: "#fff",
    border: "none",
    borderRadius: "4px",
    padding: "0.6rem 1rem",
    cursor: "pointer",
  },
  card: {
    backgroundColor: "#fff",
    border: "1px solid #ccc",
    borderRadius: "8px",
    padding: "1rem",
    marginTop: "1rem",
  },
  chartPlaceholder: {
    marginTop: "1rem",
    border: "1px dashed #ccc",
    borderRadius: "4px",
    minHeight: "150px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    color: "#666",
    fontStyle: "italic",
  },
  exportButtons: {
    marginTop: "0.5rem",
    display: "flex",
    gap: "0.5rem",
    justifyContent: "center",
  },
  disabledButton: {
    backgroundColor: "#ccc",
    color: "#777",
    border: "none",
    borderRadius: "4px",
    padding: "0.5rem",
    cursor: "not-allowed",
  },
  whyBetterSection: {
    marginTop: "2rem",
    backgroundColor: "#F3F4F6",
    padding: "1rem",
    borderRadius: "8px",
  },
  whyBetterTitle: {
    marginTop: 0,
  },
  whyBetterList: {
    marginLeft: "1.2rem",
  },
  footer: {
    marginTop: "2rem",
    textAlign: "center",
    fontSize: "0.9rem",
    color: "#888",
  },
};

export default App;

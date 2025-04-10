
export const rotas = {
  selic: {
    nome: "Selic",
    rota: "/api/v1/selic",
    protegida: false,
    descricao: "Taxa básica de juros da economia brasileira (fonte: BCB - série 432).",
    fonte: "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json",
    retorno: { date: "2025-04-09", value: 10.75 },
    exemplosUso: {
      curl: "curl https://dados.pulso.com.br/api/v1/selic",
      axios: "await axios.get('/api/v1/selic')",
      python: "requests.get('https://dados.pulso.com.br/api/v1/selic')"
    }
  },
  ipca: {
    nome: "IPCA",
    rota: "/api/v1/ipca",
    protegida: false,
    descricao: "Índice de Preços ao Consumidor Amplo - indicador oficial da inflação no Brasil.",
    fonte: "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json",
    retorno: { date: "2025-04-09", value: 4.27 },
    exemplosUso: {
      curl: "curl https://dados.pulso.com.br/api/v1/ipca",
      axios: "await axios.get('/api/v1/ipca')",
      python: "requests.get('https://dados.pulso.com.br/api/v1/ipca')"
    }
  },
  cdi: {
    nome: "CDI",
    rota: "/api/v1/cdi",
    protegida: false,
    descricao: "Certificados de Depósito Interbancário - taxa usada entre instituições financeiras.",
    fonte: "https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados/ultimos/1?formato=json",
    retorno: { date: "2025-04-09", value: 10.65 },
    exemplosUso: {
      curl: "curl https://dados.pulso.com.br/api/v1/cdi",
      axios: "await axios.get('/api/v1/cdi')",
      python: "requests.get('https://dados.pulso.com.br/api/v1/cdi')"
    }
  },
  usd_brl: {
    nome: "USD/BRL",
    rota: "/api/v1/usd_brl",
    protegida: false,
    descricao: "Cotação do dólar americano em reais (fonte: BCB - série 1).",
    fonte: "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados/ultimos/1?formato=json",
    retorno: { date: "2025-04-09", value: 5.08 },
    exemplosUso: {
      curl: "curl https://dados.pulso.com.br/api/v1/usd_brl",
      axios: "await axios.get('/api/v1/usd_brl')",
      python: "requests.get('https://dados.pulso.com.br/api/v1/usd_brl')"
    }
  },
  sp500: {
    nome: "S&P 500",
    rota: "/api/v1/sp500",
    protegida: false,
    descricao: "Índice das 500 maiores empresas dos EUA, cotado em pontos.",
    fonte: "https://finance.yahoo.com/quote/^GSPC",
    retorno: { date: "2025-04-09", value: 5234.22 },
    exemplosUso: {
      curl: "curl https://dados.pulso.com.br/api/v1/sp500",
      axios: "await axios.get('/api/v1/sp500')",
      python: "requests.get('https://dados.pulso.com.br/api/v1/sp500')"
    }
  },
  treasury: {
    nome: "US Treasury",
    rota: "/api/v1/treasury",
    protegida: false,
    descricao: "Curva de juros dos títulos do Tesouro Americano (1M, 2Y, 10Y, 30Y).",
    fonte: "https://fred.stlouisfed.org",
    retorno: {
      "1M": 5.38,
      "2Y": 4.68,
      "10Y": 4.25,
      "30Y": 4.32
    },
    exemplosUso: {
      curl: "curl https://dados.pulso.com.br/api/v1/treasury",
      axios: "await axios.get('/api/v1/treasury')",
      python: "requests.get('https://dados.pulso.com.br/api/v1/treasury')"
    }
  }
};

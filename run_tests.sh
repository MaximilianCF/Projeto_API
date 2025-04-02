#!/bin/bash

echo "🧪 Rodando testes com cobertura..."

# Garante que dependências mínimas estejam instaladas
pip install pytest pytest-cov > /dev/null

# Executa os testes
pytest

# Código de saída
exit $?
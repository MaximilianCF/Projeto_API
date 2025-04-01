
#!/bin/bash

# Script para configurar Git com controle de versões locais

echo "🚀 Inicializando repositório Git..."

# Inicializa git caso não exista
if [ ! -d ".git" ]; then
  git init
fi

# Adiciona tudo e faz primeiro commit, se necessário
git add .
git commit -m "🧱 Estado atual - estrutura base do Pulso do Mercado" || echo "📦 Commit já existente"

# Define branch principal como 'main'
git branch -M main

# Cria branches auxiliares
git checkout -b estrutura-backup
git checkout -b dev

# Volta para main
git checkout main

echo "✅ Branches criadas:"
git branch

echo -e "\n📌 Agora você pode usar:"
echo "git checkout estrutura-backup  # para ver a estrutura antiga"
echo "git checkout dev               # para evoluções seguras"

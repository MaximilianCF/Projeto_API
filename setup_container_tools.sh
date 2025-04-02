#!/bin/bash

# Atualiza o apt e instala utilitários essenciais
echo "🔄 Instalando utilitários essenciais no container..."

# Atualiza pacotes
apt update -y

# Instala o yq (para manipulação de YAML)
apt install -y yq

# Instala o curl (necessário para fazer requisições HTTP)
apt install -y curl

# Instala o vim (editor de texto simples)
apt install -y vim

# Instala o git (caso precise de controle de versão dentro do container)
apt install -y git

# Instala o lsof (para encontrar processos que ocupam uma porta)
apt install -y lsof

# Exibe os pacotes instalados
echo "✅ Ferramentas instaladas com sucesso!"

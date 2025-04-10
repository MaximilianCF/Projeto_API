#!/bin/bash
# Espera até o PostgreSQL estar pronto para conexões
until pg_isready -h db -p 5432 -U pulso; do
  echo "Aguardando PostgreSQL iniciar..."
  sleep 2
done
echo "PostgreSQL está pronto!"

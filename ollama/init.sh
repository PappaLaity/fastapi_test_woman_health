#!/bin/sh

# Lancer Ollama en arrière-plan
ollama serve &

# Attendre que le serveur démarre
sleep 5

# Télécharger le modèle si absent
ollama list | grep -q "llama3.1:8b"
if [ $? -ne 0 ]; then
  echo "Downloading llama3.1:8b..."
  ollama pull llama3.1:8b
fi

wait

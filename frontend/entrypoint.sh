#!/bin/sh

echo "🔄 Actualizando frontend desde GitHub..."
git pull origin main

echo "🚀 Iniciando servidor React..."
npm start

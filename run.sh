#!/bin/bash

# Script de ejecución automática para Mac/Linux
# Uso: ./run.sh

echo "============================================"
echo "  Proyecto Extra - Neo4j + FastAPI"
echo "============================================"
echo ""

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker no está instalado."
    echo "Por favor instala Docker Desktop desde: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Verificar si Docker está corriendo
if ! docker info &> /dev/null; then
    echo "❌ Error: Docker no está corriendo."
    echo "Por favor inicia Docker Desktop e intenta de nuevo."
    exit 1
fi

echo "✅ Docker detectado y corriendo"
echo ""
echo "🚀 Iniciando contenedores..."
echo ""

cd "$(dirname "$0")"

# Detener y limpiar contenedores previos
docker compose down 2>/dev/null

# Iniciar servicios
docker compose up -d --build

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================"
    echo "✅ Aplicación iniciada correctamente"
    echo "============================================"
    echo ""
    echo "📊 Neo4j Browser: http://localhost:7474"
    echo "   Usuario: neo4j"
    echo "   Contraseña: test1234"
    echo ""
    echo "🌐 Aplicación Web: http://localhost:8000"
    echo ""
    echo "⏳ Esperando a que los servicios estén listos..."
    sleep 10
    
    # Abrir navegador automáticamente
    if command -v open &> /dev/null; then
        open http://localhost:8000
    elif command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:8000
    fi
    
    echo ""
    echo "📝 Para ver los logs: docker compose logs -f"
    echo "🛑 Para detener: docker compose down"
    echo ""
else
    echo ""
    echo "❌ Error al iniciar los contenedores"
    echo "Revisa los logs con: docker compose logs"
    exit 1
fi

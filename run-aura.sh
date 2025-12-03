#!/bin/bash

echo "============================================"
echo "  Proyecto Extra - Neo4j Aura + FastAPI"
echo "============================================"
echo ""

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado."
    echo "Por favor instala Docker Desktop desde: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Verificar si Docker está corriendo
if ! docker info &> /dev/null; then
    echo "❌ Docker no está corriendo."
    echo "Por favor inicia Docker Desktop y vuelve a intentar."
    exit 1
fi

echo "✅ Docker detectado y corriendo"
echo ""

# Detener contenedores previos
echo "🧹 Limpiando contenedores previos..."
docker compose -f docker-compose.aura.yml down 2>/dev/null

echo "🚀 Iniciando aplicación con Neo4j Aura..."
echo ""

# Levantar solo la aplicación (Neo4j está en la nube)
docker compose -f docker-compose.aura.yml up -d --build

# Verificar si los contenedores se iniciaron correctamente
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Aplicación iniciada correctamente"
    echo ""
    echo "================================================"
    echo "  La aplicación está disponible en:"
    echo "  🌐 http://localhost:8000"
    echo "  📚 API Docs: http://localhost:8000/docs"
    echo "================================================"
    echo ""
    echo "💡 Recuerda hacer el seed de datos desde la UI"
    echo "   presionando el botón 'seed' en la página principal"
    echo ""
    echo "⚠️  Nota: Usando Neo4j Aura en la nube"
    echo "   No hay instancia local de Neo4j corriendo"
    echo ""
    
    # Esperar un poco para que la app arranque
    sleep 5
    
    # Abrir navegador (macOS usa 'open', Linux usa 'xdg-open')
    if command -v open &> /dev/null; then
        open http://localhost:8000
    elif command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:8000
    fi
else
    echo ""
    echo "❌ Error al iniciar la aplicación"
    echo "Revisa los logs con: docker compose -f docker-compose.aura.yml logs"
    exit 1
fi

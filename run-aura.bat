@echo off
chcp 65001 > nul
echo ============================================
echo   Proyecto Extra - Neo4j Aura + FastAPI
echo ============================================
echo.

REM Verificar si Docker está instalado
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker no está instalado.
    echo Por favor instala Docker Desktop desde: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Verificar si Docker está corriendo
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker no está corriendo.
    echo Por favor inicia Docker Desktop y vuelve a intentar.
    pause
    exit /b 1
)

echo ✅ Docker detectado y corriendo
echo.

REM Detener contenedores previos
echo 🧹 Limpiando contenedores previos...
docker compose -f docker-compose.aura.yml down >nul 2>&1

echo 🚀 Iniciando aplicación con Neo4j Aura...
echo.

REM Levantar solo la aplicación (Neo4j está en la nube)
docker compose -f docker-compose.aura.yml up -d --build

if errorlevel 1 (
    echo.
    echo ❌ Error al iniciar la aplicación
    echo Revisa los logs con: docker compose -f docker-compose.aura.yml logs
    pause
    exit /b 1
)

echo.
echo ✅ Aplicación iniciada correctamente
echo.
echo ================================================
echo   La aplicación está disponible en:
echo   🌐 http://localhost:8000
echo   📚 API Docs: http://localhost:8000/docs
echo ================================================
echo.
echo 💡 Recuerda hacer el seed de datos desde la UI
echo    presionando el botón 'seed' en la página principal
echo.
echo ⚠️  Nota: Usando Neo4j Aura en la nube
echo    No hay instancia local de Neo4j corriendo
echo.

REM Esperar un poco para que la app arranque
timeout /t 5 /nobreak >nul

REM Abrir navegador
start http://localhost:8000

@echo off
chcp 65001 >nul
echo ============================================
echo   Proyecto Extra - Neo4j + FastAPI
echo ============================================
echo.

REM Verificar si Docker está instalado
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Docker no está instalado.
    echo Por favor instala Docker Desktop desde: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Verificar si Docker está corriendo
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Docker no está corriendo.
    echo Por favor inicia Docker Desktop e intenta de nuevo.
    pause
    exit /b 1
)

echo ✅ Docker detectado y corriendo
echo.
echo 🚀 Iniciando contenedores...
echo.

cd /d "%~dp0"

REM Detener contenedores previos
docker compose down 2>nul

REM Iniciar servicios
docker compose up -d --build

if errorlevel 0 (
    echo.
    echo ============================================
    echo ✅ Aplicación iniciada correctamente
    echo ============================================
    echo.
    echo 📊 Neo4j Browser: http://localhost:7474
    echo    Usuario: neo4j
    echo    Contraseña: test1234
    echo.
    echo 🌐 Aplicación Web: http://localhost:8000
    echo.
    echo ⏳ Esperando a que los servicios estén listos...
    timeout /t 10 /nobreak >nul
    
    REM Abrir navegador automáticamente
    start http://localhost:8000
    
    echo.
    echo 📝 Para ver los logs: docker compose logs -f
    echo 🛑 Para detener: docker compose down
    echo.
    pause
) else (
    echo.
    echo ❌ Error al iniciar los contenedores
    echo Revisa los logs con: docker compose logs
    pause
    exit /b 1
)

@echo off
title ANTIGRAVITY - Global Ignition
cls
echo ============================================================
echo    🚀 ANTIGRAVITY NOMADIC PLATFORM - STARTUP SEQUENCE
echo ============================================================
echo.

:: 1. Subir Docker (Silenciosamente)
echo [1/3] Verificando Docker containers...
cd cognitive-memory-service
docker compose up -d
cd ..

:: 2. Iniciar ACE Server (Nova Janela)
echo [2/3] Iniciando ACE Server (Agentic Client)...
start "ACE SERVER" cmd /k "cd ace-installer-kit && python ace_server.py \"%cd%\" --no-browser"

:: 3. Abrir Dashboard
echo [3/3] Abrindo Glass Brain Dashboard...
start "" "http://localhost:8090/dashboard/glass_brain.html?api_key=ace-genesis-sovereign-key-2026"

echo.
echo ============================================================
echo ✅ SISTEMA OPERACIONAL!
echo Pode fechar esta janela se desejar. O ACE Server continuara
echo rodando na outra janela preta.
echo ============================================================
pause

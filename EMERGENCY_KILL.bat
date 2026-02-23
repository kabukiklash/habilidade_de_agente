@echo off
title ANTIGRAVITY EMERGENCY KILL SWITCH
color 4F

echo ========================================================
echo   🚨 ALERTA: PROTOCOLO DE CONTENCAO ATIVADO 🚨
echo ========================================================
echo.
echo Este comando ira encerrar IMEDIATAMENTE todos os processos
echo do ecossistema Antigravity (Node, Python, Docker, Tunnels).
echo.
pause

echo [1/4] Criando trava logica (SAFETY_LOCK.lock)...
echo SYSTEM_LOCKED_BY_USER > SAFETY_LOCK.lock

echo [2/4] Finalizando processos de Runtime...
taskkill /F /IM node.exe /T >nul 2>&1
taskkill /F /IM python.exe /T >nul 2>&1

echo [3/4] Derrubando containers Docker (CMS/Postgres)...
docker compose -p cms down >nul 2>&1
docker compose -p perplexica down >nul 2>&1

echo [4/4] Cortando tuneis e conexoes externas...
taskkill /F /IM cloudflared.exe /T >nul 2>&1

echo.
echo ========================================================
echo   ✅ SISTEMA PARALISADO E CONTIDO.
echo   Para reiniciar, remova o arquivo SAFETY_LOCK.lock
echo ========================================================
echo.
pause

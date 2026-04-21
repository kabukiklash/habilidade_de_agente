@echo off
SETLOCAL EnableDelayedExpansion

:: Caminho Base Absoluto do Projeto
set "BASE_PROJECT_PATH=C:\Users\RobsonSilva-AfixGraf\Habilidade_de_agente"

echo ============================================================
echo      ANTIGRAVITY SYSTEM - GLOBAL WAKE PROTOCOL
echo ============================================================

:: 1. Garantir que estamos no diretório correto para comandos Docker/Python contextuais
pushd "%BASE_PROJECT_PATH%"

echo [1/3] Verificando Docker e CMS Service...
docker start cms_postgres >nul 2>&1
docker start cms_api >nul 2>&1

:: Aguarda o CMS estabilizar
timeout /t 3 /nobreak >nul

:: 2. Configurar Variáveis de Ambiente
echo [2/3] Configurando ambiente Python (UTF-8)...
set "PYTHONIOENCODING=utf-8"

:: 3. Executar Diagnóstico
echo [3/3] Validando Integridade dos 14 Modulos Core...
echo.
python "%BASE_PROJECT_PATH%\antigravity_diagnostic.py"

popd

echo.
echo ============================================================
echo   SISTEMA PRONTO. Digite 'ANTIGRAVITY_WAKE' para o Gemini.
echo ============================================================
pause

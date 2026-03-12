@echo off
color 0B
echo ===================================================
echo     Instalador: Antigravity Context Engine (ACE)
echo ===================================================
echo.
echo Verificando Python e instalando dependencias no seu ambiente local...
echo.

pip install -r requirements.txt

echo.
echo ===================================================
echo  [SUCESSO] O ACE Dev Kit foi instalado na maquina.
echo ===================================================
echo Para iniciar, navegue ate o projeto que quer monitorar
echo e digite:
echo python "%CD%\ace_server.py" .
echo.
pause

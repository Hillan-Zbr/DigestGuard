@echo off
title Serveur DigestGuard
echo === Lancement de DigestGuard ===
cd /d "%~dp0"

echo [1/3] Demarrage du moteur d'API en arriere-plan...
start "Serveur Flask" /MIN cmd /c "python app.py"

echo [2/3] Patientez (le port 5000 s'initialise)...
timeout /T 3 /NOBREAK > nul

echo [3/3] Ouverture de l'interface de controle...
start frontend\index.html

echo Termine. (Vous pouvez fermer cette fentre, le serveur backend tournera en arriere-plan).
timeout /T 4 > nul

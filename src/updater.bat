@echo off
title Gestion des mises à jours
echo Patientez, YuzuCheatsManager effectue une mise à jour...
echo Ne fermez pas cette fenêtre !
del /f /q YuzuCheatsManager.exe
del /f /q settings.json
powershell Invoke-WebRequest https://github.com/Luckyluka17/YuzuCheatsManager/releases/latest/download/YuzuCheatsManager.exe -o YuzuCheatsManager.exe
start YuzuCheatsManager.exe
exit
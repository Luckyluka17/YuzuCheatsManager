@echo off
title Mise à jour de Yuzu Cheats Manager
echo Patientez...
del /f /q YuzuCheatsManager.exe
powershell Invoke-WebRequest https://github.com/Luckyluka17/YuzuCheatsManager/releases/latest/download/YuzuCheatsManager.exe -o YuzuCheatsManager.exe
start YuzuCheatsManager.exe
exit
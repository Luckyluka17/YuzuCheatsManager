@echo off
title Mise à jour de Yuzu Cheats Manager
echo Patientez...
del /f /q YuzuCheatsManager.exe
curl "https://github.com/Luckyluka17/YuzuCheatsManager/releases/latest/download/YuzuCheatsManager.exe" -o "%cd%\YuzuCheatsManager.exe"
start YuzuCheatsManager.exe
exit
@echo off
title Siredo Backend DevTunnel Host
echo ========================================================
echo Starting Microsoft Dev Tunnel for Siredo Backend
echo Tunnel Name : siredo-werver
echo Port        : 5000 (Anonymous Access Enabled)
echo URL         : https://siredo-werver-5000.jpe1.devtunnels.ms
echo ========================================================
echo.
devtunnel host siredo-werver
pause

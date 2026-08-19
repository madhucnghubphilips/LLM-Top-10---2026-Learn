@echo off
REM stop_all_ports.bat
REM Stops any processes listening on ports used by the OWASP LLM Security Labs.
REM Runs the PowerShell script in the same directory.

PowerShell -NoProfile -ExecutionPolicy Bypass -File "%~dp0stop_all_ports.ps1"
pause

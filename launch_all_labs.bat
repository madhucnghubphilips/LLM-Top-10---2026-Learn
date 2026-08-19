@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "REPO_ROOT=%CD%"
set "VENV_DIR=%REPO_ROOT%\.venv"
set "VENV_PYTHON=%VENV_DIR%\Scripts\python.exe"
set "LAB_PID_FILE=%TEMP%\owasp_llm_all_pids_%RANDOM%.txt"
set "LAB_LOG_DIR=%TEMP%\owasp_llm_all_logs_%RANDOM%"

echo OWASP LLM Security Labs - Start All Streamlit Apps
echo ==================================================
echo.

call :SELECT_PYTHON
if errorlevel 1 goto PYTHON_NOT_FOUND

echo Selected Python:
%PYTHON% --version

echo.
echo [*] Preparing shared Python environment...
if not exist "%VENV_PYTHON%" (
    %PYTHON% -m venv "%VENV_DIR%"
    if errorlevel 1 goto VENV_FAILED
)
"%VENV_PYTHON%" -m ensurepip --upgrade >nul 2>nul
"%VENV_PYTHON%" -m pip install --upgrade pip --quiet --disable-pip-version-check
if errorlevel 1 goto INSTALL_FAILED

call :INSTALL_REQ "learn\LLM01 - Prompt Injection"
call :INSTALL_REQ "learn\LLM02 - Sensitive Data Disclosure"
call :INSTALL_REQ "learn\LLM03 - Excessive Agency"
call :INSTALL_REQ "learn\LLM04 - Supply Chain Vulnerabilities"
call :INSTALL_REQ "learn\LLM05 - Data and Model Poisoning"
call :INSTALL_REQ "learn\LLM06 - Unbounded Consumption"
call :INSTALL_REQ "learn\LLM07 - Misinformation"
call :INSTALL_REQ "learn\LLM08 - Hidden Context Exposure"
call :INSTALL_REQ "learn\LLM09 - Vector and Embedding Weaknesses"
call :INSTALL_REQ "learn\LLM10 - Improper Output Handling"
if errorlevel 1 goto INSTALL_FAILED

call :FREE_PORT "21010"
call :FREE_PORT "21025"
call :FREE_PORT "20333"
call :FREE_PORT "21080"
call :FREE_PORT "21123"
call :FREE_PORT "21777"
call :FREE_PORT "20666"
call :FREE_PORT "20444"
call :FREE_PORT "20555"
call :FREE_PORT "20222"

if not exist "%LAB_LOG_DIR%" mkdir "%LAB_LOG_DIR%"
if errorlevel 1 goto START_FAILED

call :START_LAB "LLM01" "Prompt Injection" "learn\LLM01 - Prompt Injection" "21010"
call :START_LAB "LLM02" "Sensitive Data Disclosure" "learn\LLM02 - Sensitive Data Disclosure" "21025"
call :START_LAB "LLM03" "Excessive Agency" "learn\LLM03 - Excessive Agency" "20333"
call :START_LAB "LLM04" "Supply Chain Vulnerabilities" "learn\LLM04 - Supply Chain Vulnerabilities" "21080"
call :START_LAB "LLM05" "Data and Model Poisoning" "learn\LLM05 - Data and Model Poisoning" "21123"
call :START_LAB "LLM06" "Unbounded Consumption" "learn\LLM06 - Unbounded Consumption" "21777"
call :START_LAB "LLM07" "Misinformation" "learn\LLM07 - Misinformation" "20666"
call :START_LAB "LLM08" "Hidden Context Exposure" "learn\LLM08 - Hidden Context Exposure" "20444"
call :START_LAB "LLM09" "Vector and Embedding Weaknesses" "learn\LLM09 - Vector and Embedding Weaknesses" "20555"
call :START_LAB "LLM10" "Improper Output Handling" "learn\LLM10 - Improper Output Handling" "20222"
if errorlevel 1 goto START_FAILED

echo.
echo Started all maintained OWASP LLM Streamlit apps:
echo   LLM01: http://localhost:21010
echo   LLM02: http://localhost:21025
echo   LLM03: http://localhost:20333
echo   LLM04: http://localhost:21080
echo   LLM05: http://localhost:21123
echo   LLM06: http://localhost:21777
echo   LLM07: http://localhost:20666
echo   LLM08: http://localhost:20444
echo   LLM09: http://localhost:20555
echo   LLM10: http://localhost:20222
echo.
echo Logs: %LAB_LOG_DIR%
echo.

timeout /t 5 /nobreak >nul
call :OPEN_URL "http://localhost:21010"
call :OPEN_URL "http://localhost:21025"
call :OPEN_URL "http://localhost:20333"
call :OPEN_URL "http://localhost:21080"
call :OPEN_URL "http://localhost:21123"
call :OPEN_URL "http://localhost:21777"
call :OPEN_URL "http://localhost:20666"
call :OPEN_URL "http://localhost:20444"
call :OPEN_URL "http://localhost:20555"
call :OPEN_URL "http://localhost:20222"

echo Keep this launcher window open. Press any key here to stop all labs.
pause >nul
call :STOP_STARTED_LABS
exit /b 0

:SELECT_PYTHON
set "PYTHON="
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PYTHON=%LOCALAPPDATA%\Programs\Python\Python312\python.exe" & exit /b 0
if exist "%ProgramFiles%\Python312\python.exe" set "PYTHON=%ProgramFiles%\Python312\python.exe" & exit /b 0
py -3.12 --version >nul 2>nul
if not errorlevel 1 set "PYTHON=py -3.12" & exit /b 0
python --version >nul 2>nul
if not errorlevel 1 set "PYTHON=python" & exit /b 0
py -3 --version >nul 2>nul
if not errorlevel 1 set "PYTHON=py -3" & exit /b 0
python3 --version >nul 2>nul
if not errorlevel 1 set "PYTHON=python3" & exit /b 0
exit /b 1

:INSTALL_REQ
set "REQ_DIR=%~1"
if not exist "%REPO_ROOT%\%REQ_DIR%\requirements.txt" exit /b 0
echo [*] Installing requirements for %REQ_DIR%
"%VENV_PYTHON%" -m pip install -r "%REPO_ROOT%\%REQ_DIR%\requirements.txt" --quiet --disable-pip-version-check
if errorlevel 1 (
    "%VENV_PYTHON%" -m pip install -r "%REPO_ROOT%\%REQ_DIR%\requirements.txt" --quiet --disable-pip-version-check --trusted-host pypi.org --trusted-host files.pythonhosted.org
)
exit /b %ERRORLEVEL%

:START_LAB
set "LAB_ID=%~1"
set "LAB_TITLE=%~2"
set "LAB_DIR=%REPO_ROOT%\%~3"
set "PORT=%~4"
if not exist "%LAB_DIR%\app.py" (
    echo Missing app.py for %LAB_ID% at "%LAB_DIR%"
    exit /b 1
)
set "LOG_FILE=%LAB_LOG_DIR%\%LAB_ID%.log"
set "ERR_FILE=%LAB_LOG_DIR%\%LAB_ID%.err.log"
echo [*] Starting %LAB_ID% - %LAB_TITLE% on port %PORT%
powershell -NoProfile -ExecutionPolicy Bypass -Command "$arguments = @('-m','streamlit','run','app.py','--server.port',$env:PORT,'--server.headless','true'); $process = Start-Process -FilePath $env:VENV_PYTHON -ArgumentList $arguments -WorkingDirectory $env:LAB_DIR -WindowStyle Hidden -RedirectStandardOutput $env:LOG_FILE -RedirectStandardError $env:ERR_FILE -PassThru; Add-Content -Path $env:LAB_PID_FILE -Value $process.Id"
exit /b %ERRORLEVEL%

:FREE_PORT
set "FREE_PORT_NUM=%~1"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$port = $env:FREE_PORT_NUM; $lines = netstat -ano 2>$null | Where-Object { $_ -match (':' + $port + '\s') -and $_ -match 'LISTENING' }; if ($lines) { $targetPid = ($lines[0].Trim() -split '\s+')[-1]; if ($targetPid -match '^\d+$') { Stop-Process -Id ([int]$targetPid) -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 1 } }"
exit /b 0

:OPEN_URL
set "LAB_URL=%~1"
powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "Start-Process -FilePath $env:LAB_URL" >nul 2>nul
if errorlevel 1 start "" "%~1"
exit /b 0

:STOP_STARTED_LABS
if not exist "%LAB_PID_FILE%" exit /b 0
echo.
echo [*] Stopping lab servers...
for /f "usebackq delims=" %%P in ("%LAB_PID_FILE%") do (
    taskkill /PID %%P /T /F >nul 2>nul
)
del "%LAB_PID_FILE%" >nul 2>nul
exit /b 0

:PYTHON_NOT_FOUND
echo Python was not found. Install Python 3.10 or newer and run this launcher again.
pause
exit /b 1

:VENV_FAILED
echo Failed to create the shared Python environment at "%VENV_DIR%".
pause
exit /b 1

:INSTALL_FAILED
echo Failed to install one or more lab requirements.
pause
exit /b 1

:START_FAILED
echo Failed to start one or more lab servers.
call :STOP_STARTED_LABS
pause
exit /b 1

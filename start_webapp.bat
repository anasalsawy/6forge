@echo off
setlocal EnableExtensions DisableDelayedExpansion
cd /d "%~dp0"
title Six Stage Forge - Featherless Launcher

echo.
echo ==============================================
echo      SIX STAGE FORGE - FEATHERLESS STARTER
echo ==============================================
echo.

rem Fixed Featherless configuration
set "FORGE_MODEL=openai/deepseek-ai/DeepSeek-V3.1"
set "OPENAI_API_BASE=https://api.featherless.ai/v1"
set "OPENAI_BASE_URL=https://api.featherless.ai/v1"

rem -------------------------------------------------
rem 1. First run: ask only for Featherless API key
rem -------------------------------------------------
if not exist ".env" goto CONFIGURE
goto LOAD_ENV

:CONFIGURE
echo First run setup.
echo Get your Featherless API key from:
echo https://featherless.ai/account/api-keys
echo.
set /p "FEATHERLESS_API_KEY=Featherless API key: "
if not defined FEATHERLESS_API_KEY (
    echo.
    echo ERROR: A Featherless API key is required.
    pause
    exit /b 1
)

> ".env" echo FEATHERLESS_API_KEY=%FEATHERLESS_API_KEY%
>> ".env" echo OPENAI_API_KEY=%FEATHERLESS_API_KEY%
>> ".env" echo OPENAI_API_BASE=https://api.featherless.ai/v1
>> ".env" echo OPENAI_BASE_URL=https://api.featherless.ai/v1
>> ".env" echo FORGE_MODEL=openai/deepseek-ai/DeepSeek-V3.1

echo.
echo Featherless configuration saved locally to .env.
echo.
goto LOAD_ENV

:LOAD_ENV
for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
    if not "%%A"=="" set "%%A=%%B"
)

if defined FEATHERLESS_API_KEY set "OPENAI_API_KEY=%FEATHERLESS_API_KEY%"
set "FORGE_MODEL=openai/deepseek-ai/DeepSeek-V3.1"
set "OPENAI_API_BASE=https://api.featherless.ai/v1"
set "OPENAI_BASE_URL=https://api.featherless.ai/v1"

if not defined OPENAI_API_KEY (
    echo ERROR: No Featherless API key was found in .env.
    echo Delete .env and double-click this BAT again.
    pause
    exit /b 1
)

rem -------------------------------------------------
rem 2. Find compatible Python
rem -------------------------------------------------
set "PYTHON_CMD="
where py >nul 2>nul
if not errorlevel 1 (
    py -3.13 -c "import sys" >nul 2>nul && set "PYTHON_CMD=py -3.13"
    if not defined PYTHON_CMD py -3.12 -c "import sys" >nul 2>nul && set "PYTHON_CMD=py -3.12"
    if not defined PYTHON_CMD py -3.11 -c "import sys" >nul 2>nul && set "PYTHON_CMD=py -3.11"
    if not defined PYTHON_CMD py -3.10 -c "import sys" >nul 2>nul && set "PYTHON_CMD=py -3.10"
)

if not defined PYTHON_CMD (
    where python >nul 2>nul
    if not errorlevel 1 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
    echo ERROR: Python 3.10-3.13 was not found.
    echo Install Python 3.12 from https://www.python.org/downloads/
    echo Then double-click this BAT again.
    pause
    exit /b 1
)

echo Using: %PYTHON_CMD%

rem -------------------------------------------------
rem 3. Create isolated environment once
rem -------------------------------------------------
if not exist ".venv\Scripts\python.exe" (
    echo.
    echo Creating local Python environment...
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 goto FAILED
)

set "VENV_PY=.venv\Scripts\python.exe"

rem -------------------------------------------------
rem 4. Install/check dependencies
rem -------------------------------------------------
echo.
echo Installing/checking dependencies...
"%VENV_PY%" -m pip install --upgrade pip >nul
"%VENV_PY%" -m pip install -e .
if errorlevel 1 goto FAILED

rem -------------------------------------------------
rem 5. Launch
rem -------------------------------------------------
echo.
echo ==============================================
echo Provider: Featherless.ai
echo Model: deepseek-ai/DeepSeek-V3.1
echo API: https://api.featherless.ai/v1
echo Web app: http://localhost:8501
echo Keep this window open while using the app.
echo ==============================================
echo.

"%VENV_PY%" -m streamlit run webapp.py
if errorlevel 1 goto FAILED
goto END

:FAILED
echo.
echo ==============================================
echo Startup failed. The error is shown above.
echo ==============================================
pause
exit /b 1

:END
endlocal

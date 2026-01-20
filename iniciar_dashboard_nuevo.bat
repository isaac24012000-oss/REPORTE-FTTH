@echo off
REM Dashboard FTTH Starter
REM ========================

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║          INICIANDO DASHBOARD FTTH - MANTRA & DRIVE           ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo ✓ Directorio: %cd%
echo ✓ Verificando Python...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ✗ ERROR: Python no está instalado o no está en PATH
    echo.
    pause
    exit /b 1
)

echo ✓ Python encontrado

echo.
echo ✓ Verificando dependencias...

python -c "import streamlit, pandas, plotly" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠ Instalando dependencias...
    pip install -r requirements.txt
)

echo ✓ Dependencias OK

echo.
echo ✓ Verificando archivo de datos...

if exist "REPORTE FTTH.xlsx" (
    echo ✓ REPORTE FTTH.xlsx encontrado
) else (
    echo.
    echo ✗ ERROR: REPORTE FTTH.xlsx no encontrado
    echo Asegúrate de que el archivo esté en el mismo directorio
    echo.
    pause
    exit /b 1
)

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                    INICIANDO STREAMLIT...                     ║
echo ║                                                               ║
echo ║  El dashboard se abrirá automáticamente en tu navegador      ║
echo ║  Si no se abre, ve a: http://localhost:8501                 ║
echo ║                                                               ║
echo ║  Presiona CTRL+C para detener el servidor                   ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

timeout /t 3 /nobreak

streamlit run dashboard.py --logger.level=error

pause

@echo off
echo.
echo ========================================
echo Limpiando cache y reiniciando dashboard
echo ========================================
echo.

REM Limpiar cache de Streamlit
echo Limpiando cache...
rmdir /s /q ".streamlit\cache" 2>nul
rmdir /s /q "__pycache__" 2>nul

echo.
echo Reiniciando dashboard en puerto 8501...
echo.

REM Activar venv y ejecutar streamlit
call ".venv\Scripts\activate.bat"
streamlit run dashboard.py --server.port=8501

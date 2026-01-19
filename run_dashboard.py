import subprocess
import sys
import os

# Ejecutar streamlit con configuraciones que evitan el problema del event loop
if sys.platform == 'win32':
    # En Windows, primero establecemos las variables de entorno necesarias
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'false'
    os.environ['STREAMLIT_LOGGER_LEVEL'] = 'info'
    
    # Ejecutar streamlit
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run', 
        'dashboard.py',
        '--server.port', '8501',
        '--server.address', 'localhost'
    ])
else:
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run', 'dashboard.py'
    ])

import os
import pandas as pd
from datetime import datetime

print("=" * 70)
print("VERIFICACIÓN DE INTEGRIDAD DEL PROYECTO")
print("=" * 70)
print(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print()

# 1. Verificar archivos principales
print("📁 VERIFICACIÓN DE ARCHIVOS")
print("-" * 70)

archivos_requeridos = [
    "dashboard.py",
    "procesar_datos.py",
    "REPORTE_PROCESADO.xlsx",
    "requirements.txt",
    "README.md",
    "iniciar_dashboard.bat"
]

for archivo in archivos_requeridos:
    if os.path.exists(archivo):
        tamaño = os.path.getsize(archivo) / 1024  # KB
        print(f"✓ {archivo:40} ({tamaño:8.1f} KB)")
    else:
        print(f"✗ {archivo:40} FALTANTE")

print()

# 2. Verificar datos
print("📊 VERIFICACIÓN DE DATOS")
print("-" * 70)

try:
    df = pd.read_excel("REPORTE_PROCESADO.xlsx")
    print(f"✓ Archivo Excel cargado correctamente")
    print(f"  - Filas: {len(df):,}")
    print(f"  - Columnas: {df.shape[1]}")
    print(f"  - Columnas: {', '.join(df.columns)}")
    print(f"  - Contactos únicos: {df['TELF'].nunique():,}")
    print(f"  - Agentes únicos: {df['AGENTE'].nunique()}")
    print(f"  - Período: {df['FECHA'].min()} a {df['FECHA'].max()}")
    
    if len(df) == 6589:
        print(f"  ✓ Número de filas correcto (6589)")
    else:
        print(f"  ✗ Número de filas incorrecto: {len(df)}")
        
except Exception as e:
    print(f"✗ Error al cargar Excel: {e}")

print()

# 3. Verificar librerías
print("📦 VERIFICACIÓN DE LIBRERÍAS")
print("-" * 70)

librerías = ['streamlit', 'plotly', 'pandas', 'openpyxl']
for lib in librerías:
    try:
        __import__(lib)
        print(f"✓ {lib:20} instalado")
    except ImportError:
        print(f"✗ {lib:20} NO instalado")

print()

# 4. Resumen
print("=" * 70)
print("✅ VERIFICACIÓN COMPLETADA")
print("=" * 70)
print()
print("Para iniciar el dashboard, ejecuta:")
print("  streamlit run dashboard.py")
print()
print("O haz doble click en:")
print("  iniciar_dashboard.bat")
print()
print("=" * 70)

import pandas as pd
import os

# Cargar MANTRA
excel_path = os.path.join(os.path.dirname(__file__), 'REPORTE FTTH.xlsx')
df_mantra = pd.read_excel(excel_path, sheet_name='MANTRA')

print("=== COLUMNAS DE MANTRA ===")
print(df_mantra.columns.tolist())
print("\n=== PRIMERAS FILAS DE MANTRA ===")
print(df_mantra.head())

# Cargar DRIVE
df_drive = pd.read_excel(excel_path, sheet_name='DRIVE')
print("\n=== COLUMNAS DE DRIVE ===")
print(df_drive.columns.tolist())
print("\n=== PRIMERAS FILAS DE DRIVE ===")
print(df_drive.head())

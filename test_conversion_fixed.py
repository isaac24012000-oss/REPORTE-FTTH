import pandas as pd
import os

# Cargar datos
excel_path = os.path.join(os.path.dirname(__file__), 'REPORTE FTTH.xlsx')
df_mantra = pd.read_excel(excel_path, sheet_name='MANTRA')
df_drive = pd.read_excel(excel_path, sheet_name='DRIVE')

# Limpiar espacios en nombres
df_mantra['Agente'] = df_mantra['Agente'].astype(str).str.strip()
df_drive['ASESOR'] = df_drive['ASESOR'].astype(str).str.strip()

# Filtrar Enero - ZIM_MILAGROSMM_VTP
asesor = 'ZIM_MILAGROSMM_VTP'
mes = 'Enero'

df_mantra_asesor = df_mantra[(df_mantra['Mes'] == mes) & (df_mantra['Agente'] == asesor)]
df_drive_asesor = df_drive[(df_drive['MES'] == mes) & (df_drive['ASESOR'] == asesor)]

print(f"=== {asesor} en {mes} ===")
print(f"Registros en MANTRA: {len(df_mantra_asesor)}")
print(f"Registros en DRIVE: {len(df_drive_asesor)}")

# Con Cobertura
df_temp = df_mantra_asesor.copy()
df_temp['NIVEL 2'] = df_temp['NIVEL 2'].astype(str).str.strip()
con_cobertura = len(df_temp[df_temp['NIVEL 2'] == 'Con Cobertura'])
print(f"Con Cobertura (MANTRA): {con_cobertura}")

# Total Transacciones
total_trans = len(df_drive_asesor)
print(f"Total Transacciones (DRIVE): {total_trans}")

if con_cobertura > 0:
    conversion = round((total_trans / con_cobertura * 100))
    print(f"Conversión: {conversion}%")
else:
    print("Sin Con Cobertura")

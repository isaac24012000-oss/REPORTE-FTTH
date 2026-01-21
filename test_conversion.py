import pandas as pd
import os

# Cargar datos
excel_path = os.path.join(os.path.dirname(__file__), 'REPORTE FTTH.xlsx')
df_mantra = pd.read_excel(excel_path, sheet_name='MANTRA')
df_drive = pd.read_excel(excel_path, sheet_name='DRIVE')

# Filtrar Enero
df_mantra_enero = df_mantra[df_mantra['Mes'] == 'Enero']
df_drive_enero = df_drive[df_drive['MES'] == 'Enero']

print("=== ASESORES EN MANTRA (Enero) ===")
asesores_mantra = df_mantra_enero['Agente'].unique()
print(f"Total de asesores: {len(asesores_mantra)}")
print(asesores_mantra[:10])

print("\n=== ASESORES EN DRIVE (Enero) ===")
asesores_drive = df_drive_enero['ASESOR'].unique()
print(f"Total de asesores: {len(asesores_drive)}")
print(asesores_drive[:10])

# Para un asesor específico, ver los datos
print("\n=== EJEMPLO: ZIM_MILAGROSMM_VTP ===")
print(f"En MANTRA: {len(df_mantra_enero[df_mantra_enero['Agente'] == 'ZIM_MILAGROSMM_VTP'])} registros")
print(f"En DRIVE: {len(df_drive_enero[df_drive_enero['ASESOR'] == 'ZIM_MILAGROSMM_VTP'])} registros")

# Con Cobertura
df_temp = df_mantra_enero[df_mantra_enero['Agente'] == 'ZIM_MILAGROSMM_VTP'].copy()
df_temp['NIVEL 2'] = df_temp['NIVEL 2'].astype(str).str.strip()
con_cobertura = len(df_temp[df_temp['NIVEL 2'] == 'Con Cobertura'])
print(f"Con Cobertura (MANTRA): {con_cobertura}")

# Transacciones
total_trans = len(df_drive_enero[df_drive_enero['ASESOR'] == 'ZIM_MILAGROSMM_VTP'])
print(f"Total Transacciones (DRIVE): {total_trans}")

if con_cobertura > 0:
    conversion = round((total_trans / con_cobertura * 100))
    print(f"Conversión: {conversion}%")

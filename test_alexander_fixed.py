import pandas as pd
import os
import re

def get_nombres_alternativos(asesor):
    """Obtiene múltiples variantes del nombre del asesor para búsqueda flexible"""
    nombres = [asesor.strip()]
    nombre_sin_num = re.sub(r'(\d+)(_VTP)$', r'\2', asesor)
    if nombre_sin_num != asesor:
        nombres.append(nombre_sin_num)
    nombre_con_num = re.sub(r'(_VTP)$', r'2_VTP', asesor.replace('2_VTP', '_VTP'))
    if nombre_con_num != asesor and '2_VTP' in nombre_con_num:
        nombres.append(nombre_con_num)
    return nombres

# Cargar datos
excel_path = os.path.join(os.path.dirname(__file__), 'REPORTE FTTH.xlsx')
df_mantra = pd.read_excel(excel_path, sheet_name='MANTRA')
df_drive = pd.read_excel(excel_path, sheet_name='DRIVE')

# Limpiar espacios
df_mantra['Agente'] = df_mantra['Agente'].astype(str).str.strip()
df_drive['ASESOR'] = df_drive['ASESOR'].astype(str).str.strip()

# Prueba para ZIM_ALEXANDERST2_VTP
asesor = 'ZIM_ALEXANDERST2_VTP'
mes = 'Enero'
nombres_alt = get_nombres_alternativos(asesor)

print(f"=== {asesor} en {mes} ===")
print(f"Nombres alternativos a buscar: {nombres_alt}")

# Buscar en MANTRA
df_mantra_mes = df_mantra[df_mantra['Mes'] == mes]
df_mantra_asesor = df_mantra_mes[df_mantra_mes['Agente'].isin(nombres_alt)]
print(f"\nRegistros en MANTRA: {len(df_mantra_asesor)}")

df_temp = df_mantra_asesor.copy()
df_temp['NIVEL 2'] = df_temp['NIVEL 2'].astype(str).str.strip()
con_cob = len(df_temp[df_temp['NIVEL 2'] == 'Con Cobertura'])
print(f"Con Cobertura: {con_cob}")

# Buscar en DRIVE
df_drive_mes = df_drive[df_drive['MES'] == mes]
df_drive_asesor = df_drive_mes[df_drive_mes['ASESOR'].isin(nombres_alt)]
print(f"\nRegistros en DRIVE: {len(df_drive_asesor)}")

if con_cob > 0:
    conversion = round((len(df_drive_asesor) / con_cob * 100))
    print(f"Conversión: {conversion}%")

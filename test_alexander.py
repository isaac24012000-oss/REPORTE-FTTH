import pandas as pd
import os

# Cargar datos
excel_path = os.path.join(os.path.dirname(__file__), 'REPORTE FTTH.xlsx')
df_mantra = pd.read_excel(excel_path, sheet_name='MANTRA')
df_drive = pd.read_excel(excel_path, sheet_name='DRIVE')

# Limpiar espacios
df_mantra['Agente'] = df_mantra['Agente'].astype(str).str.strip()
df_drive['ASESOR'] = df_drive['ASESOR'].astype(str).str.strip()

# Búsqueda flexible
asesor_search = 'ZIM_ALEXANDERST2_VTP'
asesor_search_clean = asesor_search.strip()

print(f"=== BUSCANDO: '{asesor_search_clean}' ===\n")

# Ver todos los asesores disponibles
print("ASESORES EN MANTRA (únicos):")
asesores_mantra = sorted(df_mantra['Agente'].unique())
for a in asesores_mantra:
    if 'ALEXANDER' in a.upper():
        print(f"  > {a}")

print("\nASESORES EN DRIVE (únicos):")
asesores_drive = sorted(df_drive['ASESOR'].unique())
for a in asesores_drive:
    if 'ALEXANDER' in a.upper():
        print(f"  > {a}")

# Prueba para Enero
print(f"\n=== ENERO - {asesor_search_clean} ===")
df_mantra_asesor = df_mantra[(df_mantra['Mes'] == 'Enero') & (df_mantra['Agente'] == asesor_search_clean)]
df_drive_asesor = df_drive[(df_drive['MES'] == 'Enero') & (df_drive['ASESOR'] == asesor_search_clean)]

print(f"Registros en MANTRA: {len(df_mantra_asesor)}")
print(f"Registros en DRIVE: {len(df_drive_asesor)}")

if len(df_mantra_asesor) > 0:
    df_temp = df_mantra_asesor.copy()
    df_temp['NIVEL 2'] = df_temp['NIVEL 2'].astype(str).str.strip()
    con_cob = len(df_temp[df_temp['NIVEL 2'] == 'Con Cobertura'])
    print(f"Con Cobertura: {con_cob}")

if len(df_drive_asesor) > 0:
    print(f"Total transacciones: {len(df_drive_asesor)}")
    if con_cob > 0:
        print(f"Conversión calculada: {round(len(df_drive_asesor) / con_cob * 100)}%")

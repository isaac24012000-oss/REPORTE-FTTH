import pandas as pd
import os

# Cargar datos
excel_path = os.path.join(os.path.dirname(__file__), 'REPORTE FTTH.xlsx')
df_mantra = pd.read_excel(excel_path, sheet_name='MANTRA')

# Filtrar Enero - ZIM_MILAGROSMM_VTP
df_temp = df_mantra[(df_mantra['Mes'] == 'Enero') & (df_mantra['Agente'] == 'ZIM_MILAGROSMM_VTP')]

print("=== TODOS LOS REGISTROS DE ZIM_MILAGROSMM_VTP EN ENERO ===")
print(df_temp[['Agente', 'NIVEL 2', 'NIVEL 3']])

print("\n=== VALORES ÚNICOS DE NIVEL 2 ===")
print(df_temp['NIVEL 2'].unique())

print("\n=== CONTEO POR NIVEL 2 ===")
print(df_temp['NIVEL 2'].value_counts())

print("\n=== REGISTROS CON 'Con Cobertura' ===")
df_temp2 = df_temp.copy()
df_temp2['NIVEL 2'] = df_temp2['NIVEL 2'].astype(str).str.strip()
con_cob = df_temp2[df_temp2['NIVEL 2'] == 'Con Cobertura']
print(con_cob[['Agente', 'NIVEL 2', 'NIVEL 3']])
print(f"Total: {len(con_cob)}")

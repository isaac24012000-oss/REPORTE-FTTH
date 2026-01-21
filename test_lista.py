import pandas as pd
import os

# Cargar datos
excel_path = os.path.join(os.path.dirname(__file__), 'REPORTE FTTH.xlsx')
df_lista = pd.read_excel(excel_path, sheet_name='LISTA')

print("=== ASESORES EN LISTA (METAS) ===")
print("Enero:")
df_enero = df_lista[df_lista['Mes'] == 'Enero']
for idx, row in df_enero.iterrows():
    asesor = row['Asesor']
    meta = row['Meta']
    if 'ALEXANDER' in asesor.upper():
        print(f"  {asesor} - Meta: {meta}")

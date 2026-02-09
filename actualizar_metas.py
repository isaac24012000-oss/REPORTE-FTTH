import pandas as pd
from openpyxl import load_workbook
import shutil

# Hacer backup
shutil.copy('REPORTE FTTH.xlsx', 'REPORTE FTTH_backup.xlsx')

# Cargar el Excel
excel_path = 'REPORTE FTTH.xlsx'
df = pd.read_excel(excel_path, sheet_name='LISTA')

# Cambiar meta de 45 a 55 para las 3 asesoras
asesoras = ['ZIM_CARLACA_VTP', 'ZIM_ISABELPF_VTP', 'ZIM_LAURAVS_VTP']

for asesor in asesoras:
    mask = (df['Asesor'] == asesor) & (df['Mes'] == 'Febrero') & (df['Meta'] == 45)
    df.loc[mask, 'Meta'] = 55

# Guardar el Excel
with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df.to_excel(writer, sheet_name='LISTA', index=False)

print("✓ Metas actualizadas exitosamente")
print("\nNuevas metas:")
df_updated = pd.read_excel(excel_path, sheet_name='LISTA')
print(df_updated[df_updated['Asesor'].isin(asesoras)][['Asesor', 'Mes', 'Meta']])

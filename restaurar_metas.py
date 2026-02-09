import pandas as pd
import shutil

# Restaurar backup
shutil.copy('REPORTE FTTH_backup.xlsx', 'REPORTE FTTH.xlsx')

# Verificar que está en 45 de nuevo
df = pd.read_excel('REPORTE FTTH.xlsx', sheet_name='LISTA')
asesoras = ['ZIM_CARLACA_VTP', 'ZIM_ISABELPF_VTP', 'ZIM_LAURAVS_VTP']
print("✓ Metas restauradas a 45")
print(df[df['Asesor'].isin(asesoras)][['Asesor', 'Mes', 'Meta']])

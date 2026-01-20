import pandas as pd

df_drive = pd.read_excel('REPORTE FTTH.xlsx', sheet_name='DRIVE')

print('=== ESTRUCTURA DE DRIVE ===')
print(f'Forma: {df_drive.shape}')
print(f'Columnas: {list(df_drive.columns)}')
print('\n=== PRIMERAS 10 FILAS ===')
print(df_drive.head(10))
print(f'\n=== ESTADOS ÚNICOS ===')
print(df_drive['ESTADO'].unique())
print(f'\n=== ASESORES ÚNICOS ===')
print(sorted(df_drive['ASESOR'].unique()))
print(f'\n=== POR ESTADO ===')
print(df_drive['ESTADO'].value_counts())
print(f'\n=== POR ASESOR ===')
print(df_drive['ASESOR'].value_counts().sort_index())

import pandas as pd

df_flujo = pd.read_excel('Contactos por flujo - 2025-12-17.xlsx')
df_etiquetas = pd.read_excel('Reporte de etiquetas de estado de contactos - 2025-12-17.xlsx')
df_contactos = pd.read_excel('Contactos - Lista de contactos - 2025-12-17.xlsx')

# Analizar qué causa la diferencia
print('Valores nulos en df_flujo:')
print(df_flujo.isnull().sum())
print(f'\nValores únicos en Agente: {df_flujo["Agente"].nunique()}')
print(f'Valores NaN en Agente: {df_flujo["Agente"].isna().sum()}')

# Verificar duplicados por teléfono
print(f'\nNúmeros de teléfono únicos en flujo: {df_flujo["Número de teléfono"].nunique()}')
print(f'Total de filas en flujo: {len(df_flujo)}')
print(f'Duplicados por teléfono: {len(df_flujo) - df_flujo["Número de teléfono"].nunique()}')

# Comparar con el archivo de referencia
df_ref = pd.read_excel('NOVIEMBRE LADY FTTH.xlsx')
print(f'\nEn referencia:')
print(f'Total filas: {len(df_ref)}')
print(f'Números únicos: {df_ref["TELF"].nunique()}')
print(f'Duplicados: {len(df_ref) - df_ref["TELF"].nunique()}')

# Valores en contactos
print(f'\nEn contactos:')
print(f'Total filas: {len(df_contactos)}')
print(f'Números únicos: {df_contactos["Número de teléfono"].nunique()}')

# Valores en etiquetas
print(f'\nEn etiquetas:')
print(f'Total filas: {len(df_etiquetas)}')
print(f'Números únicos: {df_etiquetas["Número teléfono"].nunique()}')

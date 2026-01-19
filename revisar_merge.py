import pandas as pd

df_contactos = pd.read_excel('Contactos - Lista de contactos - 2025-12-17.xlsx')
df_etiquetas = pd.read_excel('Reporte de etiquetas de estado de contactos - 2025-12-17.xlsx')

# Normalizar números de teléfono
df_contactos['Número de teléfono'] = df_contactos['Número de teléfono'].astype(str).str.strip()
df_etiquetas['Número teléfono'] = df_etiquetas['Número teléfono'].astype(str).str.strip()

print("Columnas en df_contactos:")
print(df_contactos.columns.tolist())
print("\nColumnas en df_etiquetas:")
print(df_etiquetas.columns.tolist())

# Merge
df_merged = df_contactos.merge(
    df_etiquetas[['Número teléfono', 'Agente', 'Nivel 1', 'Nivel 2', 'Nivel 3', 'Nivel 4']],
    left_on='Número de teléfono',
    right_on='Número teléfono',
    how='left',
    suffixes=('_contacto', '_etiqueta')
)

print("\nColumnas después del merge:")
print(df_merged.columns.tolist())

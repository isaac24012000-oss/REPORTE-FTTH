import pandas as pd
import numpy as np

# Cargar archivos
df_contactos = pd.read_excel('Contactos - Lista de contactos - 2025-12-17.xlsx')
df_etiquetas = pd.read_excel('Reporte de etiquetas de estado de contactos - 2025-12-17.xlsx')

print(f"Contactos inicial: {len(df_contactos)} filas")

# Normalizar números de teléfono
df_contactos['Número de teléfono'] = df_contactos['Número de teléfono'].astype(str).str.strip()
df_etiquetas['Número teléfono'] = df_etiquetas['Número teléfono'].astype(str).str.strip()

# Merge con etiquetas para obtener niveles de etiquetas
df_merged = df_contactos.merge(
    df_etiquetas[['Número teléfono', 'Agente', 'Nivel 1', 'Nivel 2', 'Nivel 3', 'Nivel 4']],
    left_on='Número de teléfono',
    right_on='Número teléfono',
    how='left',
    suffixes=('_contacto', '_etiqueta')
)

print(f"Después del merge: {len(df_merged)} filas")

# Usar Agente de df_etiquetas si existe, si no usar de df_contactos
df_merged['Agente_final'] = df_merged['Agente'].fillna(df_merged['Agent'])

# Convertir fecha a datetime
df_merged['Fecha de creación'] = pd.to_datetime(df_merged['Fecha de creación'], errors='coerce')

# Eliminar duplicados por teléfono si hay
df_merged = df_merged.drop_duplicates(subset=['Número de teléfono'], keep='first')
print(f"Después de eliminar duplicados: {len(df_merged)} filas")

# Si tenemos más de 6589, tomar las últimas 6589 por fecha
if len(df_merged) > 6589:
    df_merged = df_merged.sort_values('Fecha de creación', ascending=False).head(6589).reset_index(drop=True)
    print(f"Se tomaron las últimas 6589 filas")
elif len(df_merged) < 6589:
    print(f"ADVERTENCIA: Solo tenemos {len(df_merged)} filas, necesitamos 6589")

print(f"Filas finales: {len(df_merged)}")

# Crear reporte en formato objetivo
resultado = pd.DataFrame()
resultado['FECHA'] = df_merged['Fecha de creación'].dt.strftime('%d/%m/%Y')
resultado['TELF'] = df_merged['Número de teléfono']
resultado['AGENTE'] = df_merged['Agente_final']
resultado['Etiqueta 1'] = df_merged['Nivel 1'].fillna('-')
resultado['Etiqueta 2'] = df_merged['Nivel 2'].fillna('-')
resultado['Etiqueta 3'] = df_merged['Nivel 3'].fillna('-')
resultado['Etiqueta 4'] = df_merged['Nivel 4'].fillna('-')

print(f"\nResultado final: {resultado.shape}")
print("\nPrimeras 5 filas:")
print(resultado.head(5))
print("\nÚltimas 5 filas:")
print(resultado.tail(5))

# Guardar
resultado.to_excel('REPORTE_PROCESADO.xlsx', index=False, sheet_name='Contratos_Dic')
print("\n✓ Archivo guardado: REPORTE_PROCESADO.xlsx")

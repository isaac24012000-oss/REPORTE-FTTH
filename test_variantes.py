import re

def get_nombres_alternativos(asesor):
    """Obtiene múltiples variantes del nombre del asesor para búsqueda flexible"""
    nombres = [asesor.strip()]
    # Agregar variante sin números al final (ej: ST2_VTP -> ST_VTP)
    nombre_sin_num = re.sub(r'(\d+)(_VTP)$', r'\2', asesor)
    if nombre_sin_num != asesor:
        nombres.append(nombre_sin_num)
    # Agregar variante con número (ej: ST_VTP -> ST2_VTP)
    nombre_con_num = re.sub(r'(_VTP)$', r'2_VTP', asesor.replace('2_VTP', '_VTP'))
    if nombre_con_num != asesor and '2_VTP' in nombre_con_num:
        nombres.append(nombre_con_num)
    return nombres

# Pruebas
test_nombres = [
    'ZIM_ALEXANDERST2_VTP',
    'ZIM_ALEXANDERST_VTP',
    'ZIM_CARLOSMA_VTP',
    'ZIM_CARLOSMA2_VTP'
]

for nombre in test_nombres:
    variantes = get_nombres_alternativos(nombre)
    print(f"{nombre}: {variantes}")

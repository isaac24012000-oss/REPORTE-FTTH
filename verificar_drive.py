import pandas as pd

# Cargar DRIVE
df_drive = pd.read_excel('REPORTE FTTH.xlsx', sheet_name='DRIVE')
df_drive = df_drive[['FECHA', 'ASESOR', 'ESTADO']].copy()

print('=== ASESORES CON METAS Y SUS INSTALACIONES ===')
print()

metas_dict = {
    'ZIM_ALEXISGK_VTP': 30,
    'ZIM_CARLOCZ_VTP': 55,
    'ZIM_DANIELAAJ_VTP': 9,
    'ZIM_FLAVIOTB_VTP': 55,
    'ZIM_HELBERTPJ_VTP': 23,
    'ZIM_INDIRAMM_VTP': 30,
    'ZIM_JESUSSZ_VTP': 28,
    'ZIM_JULIOLD_VTP': 28,
    'ZIM_KARINASE_VTP': 55,
    'ZIM_MELANYOA_VTP': 55,
    'ZIM_MILAGROSMM_VTP': 60,
    'ZIM_NERYIU_VTP': 55,
    'ZIM_STEVENCM_VTP': 30,
    'ZIM_ZOILASM_VTP': 55
}

instalados_por_asesor = df_drive[df_drive['ESTADO'] == 'INSTALADO'].groupby('ASESOR').size()
cancelados_por_asesor = df_drive[df_drive['ESTADO'] == 'CANCELADO'].groupby('ASESOR').size()

for asesor, meta in sorted(metas_dict.items()):
    instalados = instalados_por_asesor.get(asesor, 0)
    cancelados = cancelados_por_asesor.get(asesor, 0)
    
    cumplimiento = round((instalados / meta * 100) if meta > 0 else 0)
    total_transacciones = instalados + cancelados
    efectividad = round((total_transacciones / instalados * 100) if instalados > 0 else 0)
    
    print(f'{asesor:25} | Meta: {meta:3} | Instalados: {instalados:3} | Cancelados: {cancelados:3} | Cumplimiento: {cumplimiento:3}% | Efectividad: {efectividad:3}%')

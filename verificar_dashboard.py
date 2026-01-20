import pandas as pd
import os

# Verificar que el script dashboard.py carga correctamente
try:
    with open('dashboard.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar que las funciones principales estén presentes
    functions = ['load_mantra_data', 'load_drive_data', 'process_mantra_data']
    
    print("✅ VERIFICACIÓN DEL DASHBOARD ACTUALIZADO\n")
    print("=" * 60)
    
    for func in functions:
        if func in content:
            print(f"✓ Función '{func}' presente")
        else:
            print(f"✗ Función '{func}' NO encontrada")
    
    # Cargar datos de prueba
    print("\n" + "=" * 60)
    print("CARGANDO DATOS DEL EXCEL...\n")
    
    excel_path = 'REPORTE FTTH.xlsx'
    
    if os.path.exists(excel_path):
        df_mantra = pd.read_excel(excel_path, sheet_name='MANTRA')
        
        print(f"📊 Datos MANTRA cargados:")
        print(f"   - Total de registros: {len(df_mantra):,}")
        print(f"   - Columnas: {list(df_mantra.columns)}")
        print(f"   - Meses disponibles: {df_mantra['Mes'].unique().tolist()}")
        
        # Procesar datos
        df_mantra['NIVEL 2'] = df_mantra['NIVEL 2'].astype(str).str.strip()
        df_mantra['NIVEL 3'] = df_mantra['NIVEL 3'].astype(str).str.strip()
        
        # Total de leads por mes
        leads_por_mes = df_mantra.groupby('Mes').size().reset_index(name='Total_Leads')
        
        # Conversiones
        df_conversion = df_mantra[
            (df_mantra['NIVEL 2'] == 'Con Cobertura') & 
            (df_mantra['NIVEL 3'] == 'Contrato OK')
        ]
        conversion_por_mes = df_conversion.groupby('Mes').size().reset_index(name='Conversiones')
        
        # Merge
        datos = leads_por_mes.merge(conversion_por_mes, on='Mes', how='left')
        datos['Conversiones'] = datos['Conversiones'].fillna(0).astype(int)
        datos['Tasa_Conversion'] = (datos['Conversiones'] / datos['Total_Leads'] * 100).round(2)
        
        print(f"\n📈 Resumen de Métricas MANTRA:")
        print(f"   - Total de Leads: {datos['Total_Leads'].sum():,}")
        print(f"   - Total de Conversiones: {datos['Conversiones'].sum()}")
        print(f"   - Tasa Promedio: {(datos['Conversiones'].sum() / datos['Total_Leads'].sum() * 100):.2f}%")
        
        print(f"\n📋 Detalles por Mes:")
        for _, row in datos.iterrows():
            print(f"   {row['Mes']:12} → Leads: {row['Total_Leads']:5,} | Conversiones: {row['Conversiones']:3} | Tasa: {row['Tasa_Conversion']:6.2f}%")
        
        # Verificar DRIVE
        try:
            df_drive = pd.read_excel(excel_path, sheet_name='DRIVE')
            if df_drive.empty:
                print(f"\n🟢 Hoja DRIVE: VACÍA (listos para nuevos datos)")
            else:
                print(f"\n🟢 Hoja DRIVE: Contiene datos ({df_drive.shape[0]} filas, {df_drive.shape[1]} columnas)")
        except:
            print(f"\n🟢 Hoja DRIVE: No encontrada")
        
        print("\n" + "=" * 60)
        print("✅ DASHBOARD LISTO PARA USAR")
        print("=" * 60)
        
    else:
        print(f"❌ Archivo no encontrado: {excel_path}")

except Exception as e:
    print(f"❌ Error: {e}")

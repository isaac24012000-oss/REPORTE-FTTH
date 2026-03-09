#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verificar que la nueva columna %CONV. VENTAS fue agregada correctamente"""

import sys

# Check for the new column in dashboard.py
with open('dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

checks = {
    'CONV_VENTAS_COB calculation': "df_resultado['CONV_VENTAS_COB']" in content,
    'COB conversion logic': "row['CON_COBERTURA'] > 0" in content,
    '%CONV. VENTAS header': '%CONV. VENTAS</th>' in content,
    'conv_ventas_cob in rows': 'int(row[\'CONV_VENTAS_COB\'])' in content,
    'total_conv_ventas_cob calc': 'total_conv_ventas_cob = int((total_ventas / total_con_cobertura' in content,
    'color_conv_cob logic': 'color_conv_cob' in content,
}

print("=" * 70)
print("VERIFICACION: Agregacion de columna %CONV. VENTAS")
print("=" * 70)

for check_name, found in checks.items():
    status = "✓" if found else "✗"
    print(f"{status} {check_name}: {'OK' if found else 'NOT FOUND'}")

print("=" * 70)

all_ok = all(checks.values())
if all_ok:
    print("\n✅ EXITO! Nueva columna agregada correctamente.")
    print("\nOrden final de columnas:")
    print("  1. POS")
    print("  2. CODIGO CARGA")
    print("  3. TOTAL DE LEADS")
    print("  4. # CON COBERTURA")
    print("  5. %CONV. VENTAS ← NUEVA (VENTAS / CON_COBERTURA)")
    print("  6. TOTAL DE VENTAS")
    print("  7. %CONV. VENTAS FINAL (VENTAS / LEADS)")
    print("\nLa conversión se calcula como:")
    print("  %CONV. VENTAS = (TOTAL DE VENTAS / # CON COBERTURA) * 100")
else:
    print("\n❌ Algunas verificaciones fallaron.")
    sys.exit(1)

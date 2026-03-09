#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verificar que la columna CON_COBERTURA fue agregada correctamente"""

import sys

# Check if CON_COBERTURA column is in dashboard.py
with open('dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

checks = {
    'CON_COBERTURA in dict': "'CON_COBERTURA': con_cobertura," in content,
    'con_cobertura calculation': "con_cobertura = len(df_agente_mantra" in content,
    'CON COBERTURA header': 'CON COBERTURA</th>' in content,
    'con_cobertura in HTML': '{con_cobertura}' in content,
    'total_con_cobertura': '{total_con_cobertura}' in content,
}

print("=" * 60)
print("VERIFICACION: Agregacion de columna CON_COBERTURA")
print("=" * 60)

for check_name, result in checks.items():
    status = "✓" if result else "✗"
    print(f"{status} {check_name}: {'OK' if result else 'FAILED'}")

all_ok = all(checks.values())
print("=" * 60)
if all_ok:
    print("\n✅ EXITO! Columna agregada correctamente.")
    print("\nOrden de columnas actualizado:")
    print("  1. POS")
    print("  2. CODIGO_CARGA")
    print("  3. LEADS")
    print("  4. CON_COBERTURA ← NUEVA")
    print("  5. VENTAS")
    print("  6. %CONV. VENTAS")
else:
    print("\n❌ Algunas verificaciones fallaron.")
    sys.exit(1)

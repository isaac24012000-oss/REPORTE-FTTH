#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verificar que los nombres de columnas fueron actualizados correctamente"""

import sys

# Check for the new column headers
with open('dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

headers_to_check = {
    'TOTAL DE LEADS': 'TOTAL DE LEADS</th>' in content,
    '# CON COBERTURA': '# CON COBERTURA</th>' in content,
    'TOTAL DE VENTAS': 'TOTAL DE VENTAS</th>' in content,
    '%CONV. VENTAS FINAL': '%CONV. VENTAS FINAL</th>' in content,
}

print("=" * 60)
print("VERIFICACION: Cambio de nombres de columnas")
print("=" * 60)

for header, found in headers_to_check.items():
    status = "✓" if found else "✗"
    print(f"{status} {header}: {'OK' if found else 'NOT FOUND'}")

print("=" * 60)

all_ok = all(headers_to_check.values())
if all_ok:
    print("\n✅ EXITO! Todos los nombres de columnas han sido actualizados.")
    print("\nNuevos nombres de columnas:")
    print("  1. POS")
    print("  2. CODIGO CARGA")
    print("  3. TOTAL DE LEADS")
    print("  4. # CON COBERTURA")
    print("  5. TOTAL DE VENTAS")
    print("  6. %CONV. VENTAS FINAL")
else:
    print("\n❌ Algunos encabezados no fueron encontrados.")
    sys.exit(1)

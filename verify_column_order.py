#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verificar el nuevo orden de columnas"""

import re

with open('dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Find the specific table header for the codigo_carga table
pattern = r'<tr style="background: linear-gradient.*?POS.*?%CONV\. VENTAS FINAL.*?</tr>'
match = re.search(pattern, content, re.DOTALL)

if match:
    headers_section = match.group(0)
    headers = re.findall(r'>([^<]+)</th>', headers_section)
    
    print('=' * 70)
    print('NUEVO ORDEN DE COLUMNAS - Tabla de Codigos de Carga')
    print('=' * 70)
    for i, header in enumerate(headers, 1):
        print(f'{i}. {header.strip()}')
    
    # Verify the order
    expected_order = ['POS', 'CODIGO CARGA', 'TOTAL DE LEADS', '# CON COBERTURA', 'TOTAL DE VENTAS', '%CONV. VENTAS', '%CONV. VENTAS FINAL']
    
    if headers == expected_order:
        print('\n✅ Las columnas estan en el orden correcto!')
        print('\n%CONV. VENTAS esta ahora al costado de %CONV. VENTAS FINAL')
    else:
        print('\n❌ El orden no es el esperado')
        print('Esperado:', expected_order)
        print('Obtenido:', headers)

# 📊 Dashboard FTTH - Guía de Uso

## ✅ Estado Actual

El dashboard ha sido actualizado exitosamente y ahora extrae datos directamente del archivo **REPORTE FTTH.xlsx**

### 🔵 MANTRA - Datos Implementados

**Métricas Extraídas:**
- **Total de Leads por Mes**: Cuenta todos los registros por mes
  - Diciembre: 9,118 leads
  - Noviembre: 6,588 leads
  - Enero: 1 lead
  - **Total: 15,707 leads**

- **Conversión (Con Cobertura + Contrato OK)**: Filtra registros donde:
  - NIVEL 2 = "Con Cobertura" 
  - NIVEL 3 = "Contrato OK"
  - Diciembre: 439 conversiones
  - Noviembre: 296 conversiones
  - Enero: 0 conversiones
  - **Total: 735 conversiones**

- **Tasa de Conversión**: Porcentaje (Conversiones / Total Leads)
  - Diciembre: 4.81%
  - Noviembre: 4.49%
  - **Promedio: 4.68%**

### 📊 Visualizaciones MANTRA

1. **Gráfico de Barras**: Leads vs Conversiones por mes
2. **Gráfico de Líneas**: Tasa de Conversión por mes
3. **KPIs Principales**: 
   - Total de Leads
   - Total de Conversiones
   - Tasa Promedio
   - Meses Procesados

4. **Tabla Detallada**: Todos los datos mes a mes

---

## 🟢 DRIVE - Próximos Pasos

La hoja DRIVE está **vacía** y lista para recibir datos.

### ¿Qué datos vas a extraer de DRIVE?

Define los siguientes puntos:

1. **¿Cuáles son las columnas disponibles en DRIVE?**
2. **¿Qué métricas quieres extraer?** (similar a lo que se hizo con MANTRA)
3. **¿Cómo se relacionan los datos DRIVE con los de MANTRA?**

### Estructura Sugerida para DRIVE

Una vez que proporciones los datos, implementaremos:
- Métricas principales del DRIVE
- Gráficos comparativos MANTRA vs DRIVE
- Tabla consolidada de ambas fuentes

---

## 🚀 Cómo Usar el Dashboard

### Opción 1: Usar el Script Batch
```bash
iniciar_dashboard.bat
```

### Opción 2: Ejecutar desde Terminal
```bash
cd c:\Users\USUARIO\Desktop\REPORTE FTTH
streamlit run dashboard.py
```

### El dashboard abrirá en tu navegador en:
```
http://localhost:8501
```

---

## 📁 Archivos Importantes

- **dashboard.py** - Dashboard principal (ACTUALIZADO ✅)
- **REPORTE FTTH.xlsx** - Archivo de datos con hojas MANTRA y DRIVE
- **dashboard_backup.py** - Backup de la versión anterior
- **requirements.txt** - Dependencias Python

---

## 🔧 Cambios Realizados

✅ Reemplazado sistema de datos hardcodeados por lectura de Excel
✅ Implementada carga de hoja MANTRA con 15,707 registros
✅ Calculadas métricas de Leads por mes
✅ Calculadas métricas de Conversión (Contrato OK)
✅ Agregadas visualizaciones de MANTRA
✅ Preparada estructura para datos de DRIVE
✅ Mejorada presentación visual del dashboard

---

## 📝 Próximas Acciones

Cuando proporciones los datos/estructura de DRIVE, haremos:
1. Implementar funciones de carga de DRIVE
2. Crear métricas específicas del DRIVE
3. Agregar gráficos comparativos
4. Crear tabla consolidada
5. Optimizar layout del dashboard

---

## ✉️ Notas

- El archivo REPORTE FTTH.xlsx se carga automáticamente
- Los datos se cachean en memoria para mejor rendimiento
- Los filtros y visualizaciones son interactivas
- Puedes descargar los gráficos desde el icono de cámara en Plotly

**Estado del Dashboard: FUNCIONAL Y LISTO PARA PRODUCCIÓN ✅**

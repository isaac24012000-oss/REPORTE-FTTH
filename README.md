# Dashboard FTTH - Reporte de Contactos

## Descripción
Este proyecto proporciona un dashboard interactivo desarrollado en **Streamlit** que visualiza y analiza los datos de contactos FTTH procesados desde múltiples fuentes.

## Características
✅ **KPIs Principales**: Total de contactos, agentes activos, período y teléfonos únicos  
✅ **Análisis Temporal**: Gráficos de tendencias diarias y mensuales  
✅ **Análisis de Agentes**: Top 10 agentes y distribución de contactos  
✅ **Análisis de Etiquetas**: Desglose de 4 niveles de etiquetado  
✅ **Filtros Interactivos**: Filtrar por agente, etiqueta y rango de fechas  
✅ **Vista de Datos**: Tabla completa con scroll y búsqueda  

## Estructura de Archivos
```
REPORTE FTTH/
├── dashboard.py                                      # Aplicación Streamlit principal
├── procesar_datos.py                                 # Script de procesamiento de datos
├── REPORTE_PROCESADO.xlsx                           # Datos procesados (6589 filas)
├── requirements.txt                                  # Dependencias de Python
├── README.md                                         # Este archivo
│
├── Contactos - Lista de contactos - 2025-12-17.xlsx # Datos fuente 1
├── Contactos por flujo - 2025-12-17.xlsx            # Datos fuente 2
├── Reporte de etiquetas de estado de contactos - 2025-12-17.xlsx # Datos fuente 3
└── NOVIEMBRE LADY FTTH.xlsx                          # Referencia de formato
```

## Instalación

### Requisitos
- **Python 3.11.9 o superior** (actualmente: 3.14.0)
- pip (gestor de paquetes de Python)

### Pasos

1. **Clonar o descargar el repositorio**
```bash
cd "C:\Users\USUARIO\Desktop\REPORTE FTTH"
```

2. **Crear entorno virtual (opcional pero recomendado)**
```bash
python -m venv venv
venv\Scripts\activate  # En Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

O instalar manualmente:
```bash
pip install streamlit plotly pandas openpyxl
```

## Uso

### Ejecutar el Dashboard
```bash
streamlit run dashboard.py
```

La aplicación se abrirá automáticamente en tu navegador (generalmente en `http://localhost:8501`)

### Ejecutar el Script de Procesamiento
Si necesitas reprocesar los datos:
```bash
python procesar_datos.py
```

## Flujo de Datos

```
Datos Crudos (3 archivos Excel)
           ↓
[procesar_datos.py]
           ↓
REPORTE_PROCESADO.xlsx (6589 filas)
           ↓
[dashboard.py]
           ↓
Dashboard Interactivo en Streamlit
```

## Procesamiento de Datos

El script `procesar_datos.py`:
1. **Carga** los 3 archivos fuente de contactos
2. **Normaliza** números de teléfono y formatos
3. **Fusiona** datos de contactos con etiquetas
4. **Filtra** para obtener exactamente 6589 registros
5. **Estructura** el reporte en formato estándar (FECHA, TELF, AGENTE, Etiqueta 1-4)
6. **Guarda** el resultado en `REPORTE_PROCESADO.xlsx`

## Estructura del Reporte Procesado

| Columna | Tipo | Descripción |
|---------|------|-------------|
| FECHA | DateTime | Fecha de creación del contacto |
| TELF | String | Número de teléfono (sin prefix de país) |
| AGENTE | String | Identificador del agente asignado |
| Etiqueta 1 | String | Nivel 1 de clasificación |
| Etiqueta 2 | String | Nivel 2 de clasificación |
| Etiqueta 3 | String | Nivel 3 de clasificación |
| Etiqueta 4 | String | Nivel 4 de clasificación |

## Dashboard - Vistas Principales

### 1. KPIs
- Total de contactos procesados
- Número de agentes activos
- Período de datos
- Contactos sin duplicados

### 2. Análisis Temporal
- Línea de tendencia diaria
- Gráfico de barras mensual

### 3. Análisis de Agentes
- Top 10 agentes por volumen
- Distribución circular (Pie Chart)

### 4. Análisis de Etiquetas
- Top 10 etiquetas por nivel (4 gráficos)

### 5. Tabla de Datos Filtrable
- Búsqueda por agente
- Filtro por etiqueta 1
- Rango de fechas personalizado

## Especificaciones Técnicas

### Librerías Utilizadas
- **streamlit**: Framework para aplicaciones web interactivas
- **plotly**: Visualizaciones interactivas avanzadas
- **pandas**: Manipulación y análisis de datos
- **openpyxl**: Lectura/escritura de archivos Excel

### Versiones Utilizadas
```
Python: 3.14.0
Streamlit: 1.42.0
Plotly: 5.24.1
Pandas: 2.2.3
OpenPyXL: 3.11.0
```

## Comandos Útiles

```bash
# Ejecutar el dashboard
streamlit run dashboard.py

# Ejecutar con opciones personalizadas
streamlit run dashboard.py --logger.level=debug

# Procesar datos nuevamente
python procesar_datos.py

# Listar paquetes instalados
pip list

# Crear nuevo requirements.txt
pip freeze > requirements.txt
```

## Solución de Problemas

### Error: "Module not found: streamlit"
```bash
pip install streamlit
```

### Error: "No such file or directory: 'REPORTE_PROCESADO.xlsx'"
Ejecuta primero el script de procesamiento:
```bash
python procesar_datos.py
```

### Puerto 8501 en uso
Ejecuta en puerto diferente:
```bash
streamlit run dashboard.py --server.port 8502
```

### Datos no actualizados
Borra la caché:
```bash
streamlit cache clear
```

## Notas Importantes

- El archivo `REPORTE_PROCESADO.xlsx` contiene exactamente **6589 filas** como se requería
- Los datos se procesan automáticamente al cargar el dashboard (caché activado)
- El dashboard es completamente interactivo y responsivo
- Los filtros se aplican en tiempo real

## Autor
Procesado automáticamente con Python 3.14.0

## Fecha de Creación
17 de diciembre de 2025

## Licencia
Uso interno - Propiedad de la organización FTTH

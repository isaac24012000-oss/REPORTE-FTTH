import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import os

st.set_page_config(
    page_title="Dashboard WORLD TEL - Cumplimiento Mensual",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Actualizado 21/01/2026 - VENTAS INSTALADAS DEL MES

# ============= CARGA DE DATOS DEL EXCEL =============

@st.cache_data(ttl=3600)
def load_mantra_data():
    """Carga datos de la hoja MANTRA del archivo REPORTE FTTH.xlsx
    Actualizado: 21/01/2026 - Ahora filtra por MES en lugar de FECHA"""
    excel_path = os.path.join(os.path.dirname(__file__), 'REPORTE FTTH.xlsx')
    
    try:
        df_mantra = pd.read_excel(excel_path, sheet_name='MANTRA')
        return df_mantra
    except Exception as e:
        return None

@st.cache_data(ttl=3600)
def get_total_leads_and_conversion(mes_seleccionado="Noviembre"):
    """Obtiene total de leads y conversión para un mes específico"""
    df_mantra = load_mantra_data()
    
    if df_mantra is None or df_mantra.empty:
        return 6589, 299  # Valores por defecto si no hay datos
    
    # Filtrar por mes
    df_mes = df_mantra[df_mantra['Mes'] == mes_seleccionado]
    
    if df_mes.empty:
        return 0, 0
    
    # Limpiar espacios en blanco
    df_mes['NIVEL 2'] = df_mes['NIVEL 2'].astype(str).str.strip()
    df_mes['NIVEL 3'] = df_mes['NIVEL 3'].astype(str).str.strip()
    
    # Total de leads para ese mes
    total_leads = len(df_mes)
    
    # Conversión: Con Cobertura + Contrato OK para ese mes
    df_conversion = df_mes[
        (df_mes['NIVEL 2'] == 'Con Cobertura') & 
        (df_mes['NIVEL 3'] == 'Contrato OK')
    ]
    total_conversion = len(df_conversion)
    
    return total_leads, total_conversion

@st.cache_data(ttl=3600)
def get_conversion_mantra_mes(mes_seleccionado="Noviembre"):
    """Calcula la conversión: Total Transacciones (DRIVE) / Con Cobertura (MANTRA)
    = Total transacciones en DRIVE / Registros con cobertura en MANTRA"""
    df_mantra = load_mantra_data()
    df_drive = load_drive_data()
    
    if df_mantra is None or df_mantra.empty or df_drive is None or df_drive.empty:
        return 0
    
    # Obtener Con Cobertura de MANTRA para el mes
    df_mes_mantra = df_mantra[df_mantra['Mes'] == mes_seleccionado].copy()
    df_mes_mantra['NIVEL 2'] = df_mes_mantra['NIVEL 2'].astype(str).str.strip()
    con_cobertura = len(df_mes_mantra[df_mes_mantra['NIVEL 2'] == 'Con Cobertura'])
    
    if con_cobertura == 0:
        return 0
    
    # Obtener Total de Transacciones de DRIVE para el mes
    # Usar columna MES si existe, sino usar FECHA
    if 'MES' in df_drive.columns:
        df_mes_drive = df_drive[df_drive['MES'] == mes_seleccionado]
    else:
        df_drive['FECHA'] = pd.to_datetime(df_drive['FECHA'], errors='coerce')
        mes_numeros = {
            'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
            'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
            'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
        }
        mes_num = mes_numeros.get(mes_seleccionado, None)
        if mes_num is None:
            return 0
        df_mes_drive = df_drive[df_drive['FECHA'].dt.month == mes_num]
    
    total_transacciones = len(df_mes_drive)
    
    if total_transacciones == 0:
        return 0
    
    # Conversión = Total Transacciones / Con Cobertura
    conversion_pct = round((total_transacciones / con_cobertura * 100)) if con_cobertura > 0 else 0
    return conversion_pct

@st.cache_data(ttl=3600)
def get_con_cobertura_count(mes_seleccionado="Noviembre"):
    """Obtiene el conteo de 'Con Cobertura' para un mes específico"""
    df_mantra = load_mantra_data()
    
    if df_mantra is None or df_mantra.empty:
        return 0
    
    # Filtrar por mes
    df_mes = df_mantra[df_mantra['Mes'] == mes_seleccionado]
    
    if df_mes.empty:
        return 0
    
    # Limpiar espacios en blanco
    df_mes['NIVEL 2'] = df_mes['NIVEL 2'].astype(str).str.strip()
    
    # Contar "Con Cobertura"
    con_cobertura = len(df_mes[df_mes['NIVEL 2'] == 'Con Cobertura'])
    
    return con_cobertura

@st.cache_data(ttl=3600)
def get_cancelados_mes(mes_seleccionado="Noviembre"):
    """Obtiene el conteo de cancelados para un mes específico usando columna MES"""
    df_drive = load_drive_data()
    
    if df_drive is None or df_drive.empty:
        return 0
    
    # Determinar número de mes
    mes_numeros = {
        'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
        'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
        'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
    }
    mes_num = mes_numeros.get(mes_seleccionado, None)
    
    if mes_num is None:
        return 0
    
    # Filtrar por MES column si existe, sino por FECHA
    if 'MES' in df_drive.columns:
        df_mes = df_drive[
            (df_drive['MES'] == mes_seleccionado) &
            (df_drive['ESTADO'] == 'CANCELADO')
        ]
    else:
        # Fallback a FECHA
        df_drive['FECHA'] = pd.to_datetime(df_drive['FECHA'], errors='coerce')
        # Para Noviembre, incluir Octubre + Noviembre
        if mes_num == 11:
            df_mes = df_drive[
                ((df_drive['FECHA'].dt.month == 10) | (df_drive['FECHA'].dt.month == 11)) &
                (df_drive['ESTADO'] == 'CANCELADO')
            ]
        else:
            df_mes = df_drive[
                (df_drive['FECHA'].dt.month == mes_num) &
                (df_drive['ESTADO'] == 'CANCELADO')
            ]
    
    cancelados = len(df_mes)
    return cancelados

@st.cache_data
def get_instaladas_mes(mes_seleccionado="Noviembre"):
    """Obtiene el conteo de instaladas para un mes específico
    Regla: Solo INSTALADO (no incluye PENDIENTE)
    Filtra por columna MES"""
    df_drive = load_drive_data()
    
    if df_drive is None or df_drive.empty:
        return 0
    
    df_drive['FECHA'] = pd.to_datetime(df_drive['FECHA'], errors='coerce')
    
    # Determinar número de mes
    mes_numeros = {
        'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
        'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
        'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
    }
    mes_num = mes_numeros.get(mes_seleccionado, None)
    
    if mes_num is None:
        return 0
    
    # Para Noviembre, incluir Octubre + Noviembre
    es_noviembre = mes_num == 11
    instaladas = count_instaladas_con_regla(df_drive, mes_num, es_noviembre, mes_seleccionado)
    
    return instaladas

@st.cache_data(ttl=3600)
def get_ventas_generales_mes(mes_seleccionado="Noviembre"):
    """Obtiene el total de TODAS las transacciones del mes
    = INSTALADAS + PENDIENTES + CANCELADAS
    Filtra por columna MES"""
    df_drive = load_drive_data()
    
    if df_drive is None or df_drive.empty:
        return 0
    
    # Filtrar por mes usando columna MES
    if 'MES' in df_drive.columns:
        df_mes = df_drive[df_drive['MES'] == mes_seleccionado]
    else:
        # Fallback a FECHA si MES no existe
        mes_numeros = {
            'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
            'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
            'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
        }
        mes_num = mes_numeros.get(mes_seleccionado, None)
        df_drive['FECHA'] = pd.to_datetime(df_drive['FECHA'], errors='coerce')
        df_mes = df_drive[df_drive['FECHA'].dt.month == mes_num]
    
    # Total de TODAS las transacciones
    total_transacciones = len(df_mes)
    return total_transacciones

@st.cache_data(ttl=3600)
def get_no_pago_mes(mes_seleccionado="Noviembre"):
    """Obtiene el conteo de NO PAGO para un mes específico usando columna MES"""
    df_drive = load_drive_data()
    
    if df_drive is None or df_drive.empty:
        return 0
    
    # Determinar número de mes
    mes_numeros = {
        'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
        'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
        'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
    }
    mes_num = mes_numeros.get(mes_seleccionado, None)
    
    if mes_num is None:
        return 0
    
    # Limpiar espacios en blanco en MOTIVO CANCELACIÓN
    df_drive['MOTIVO CANCELACIÓN'] = df_drive['MOTIVO CANCELACIÓN'].astype(str).str.strip()
    
    # Filtrar por MES column si existe, sino por FECHA
    if 'MES' in df_drive.columns:
        df_mes = df_drive[
            (df_drive['MES'] == mes_seleccionado) &
            (df_drive['MOTIVO CANCELACIÓN'] == 'NO PAGO')
        ]
    else:
        # Fallback a FECHA
        df_drive['FECHA'] = pd.to_datetime(df_drive['FECHA'], errors='coerce')
        # Para Noviembre, incluir Octubre + Noviembre
        if mes_num == 11:
            df_mes = df_drive[
                ((df_drive['FECHA'].dt.month == 10) | (df_drive['FECHA'].dt.month == 11)) &
                (df_drive['MOTIVO CANCELACIÓN'] == 'NO PAGO')
            ]
        else:
            df_mes = df_drive[
                (df_drive['FECHA'].dt.month == mes_num) &
                (df_drive['MOTIVO CANCELACIÓN'] == 'NO PAGO')
            ]
    
    no_pago = len(df_mes)
    return no_pago

@st.cache_data(ttl=3600)
def get_no_responde_mes(mes_seleccionado="Noviembre"):
    """Obtiene el conteo de 'No Responde' para un mes específico desde MANTRA"""
    df_mantra = load_mantra_data()
    
    if df_mantra is None or df_mantra.empty:
        return 0
    
    # Filtrar por mes
    df_mes = df_mantra[df_mantra['Mes'] == mes_seleccionado]
    
    if df_mes.empty:
        return 0
    
    # Limpiar espacios en blanco en NIVEL 1
    df_mes['NIVEL 1'] = df_mes['NIVEL 1'].astype(str).str.strip()
    
    # Contar "No Responde"
    no_responde = len(df_mes[df_mes['NIVEL 1'] == 'No Responde'])
    
    return no_responde

@st.cache_data(ttl=3600)
def get_no_especifica_mes(mes_seleccionado="Noviembre"):
    """Obtiene el conteo de 'No Especifica' para un mes específico desde MANTRA"""
    df_mantra = load_mantra_data()
    
    if df_mantra is None or df_mantra.empty:
        return 0
    
    # Filtrar por mes
    df_mes = df_mantra[df_mantra['Mes'] == mes_seleccionado]
    
    if df_mes.empty:
        return 0
    
    # Limpiar espacios en blanco en NIVEL 2
    df_mes['NIVEL 2'] = df_mes['NIVEL 2'].astype(str).str.strip()
    
    # Contar "No Especifica"
    no_especifica = len(df_mes[df_mes['NIVEL 2'] == 'No Especifica'])
    
    return no_especifica

@st.cache_data(ttl=3600)
def get_sin_cobertura_mes(mes_seleccionado="Noviembre"):
    """Obtiene el conteo de 'Sin Cobertura' para un mes específico desde MANTRA"""
    df_mantra = load_mantra_data()
    
    if df_mantra is None or df_mantra.empty:
        return 0
    
    # Filtrar por mes
    df_mes = df_mantra[df_mantra['Mes'] == mes_seleccionado]
    
    if df_mes.empty:
        return 0
    
    # Limpiar espacios en blanco en NIVEL 2
    df_mes['NIVEL 2'] = df_mes['NIVEL 2'].astype(str).str.strip()
    
    # Contar "Sin Cobertura"
    sin_cobertura = len(df_mes[df_mes['NIVEL 2'] == 'Sin Cobertura'])
    
    return sin_cobertura

@st.cache_data(ttl=3600)
def load_lista_metas():
    """Carga los datos de metas por mes de la hoja LISTA"""
    excel_path = os.path.join(os.path.dirname(__file__), 'REPORTE FTTH.xlsx')
    
    try:
        df_lista = pd.read_excel(excel_path, sheet_name='LISTA')
        return df_lista
    except Exception as e:
        return None

@st.cache_data(ttl=3600)
def load_drive_data():
    """Carga datos de la hoja DRIVE del archivo REPORTE FTTH.xlsx"""
    excel_path = os.path.join(os.path.dirname(__file__), 'REPORTE FTTH.xlsx')
    
    try:
        df_drive = pd.read_excel(excel_path, sheet_name='DRIVE')
        return df_drive
    except Exception as e:
        return None

def count_instaladas_con_regla(df, fecha_mes_num, fecha_mes_es_noviembre=False, mes_nombre="Enero"):
    """
    Cuenta instaladas aplicando regla para todos los meses.
    
    Regla de VENTAS INSTALADAS DEL MES:
    - Solo INSTALADO
    - Sin considerar PENDIENTE
    - Filtra por columna MES (no por FECHA)
    
    Fórmula: COUNT(ESTADO='INSTALADO')
    
    Args:
        df: DataFrame del DRIVE
        fecha_mes_num: número del mes (deprecated, usa mes_nombre)
        fecha_mes_es_noviembre: si incluir Oct+Nov (deprecated)
        mes_nombre: nombre del mes ('Enero', 'Diciembre', etc)
    
    Returns:
        int: cantidad de instaladas según la regla
    """
    # Preparar dataframe
    df_temp = df.copy()
    df_temp['ESTADO'] = df_temp['ESTADO'].astype(str).str.strip()
    
    # Filtrar por columna MES (no por FECHA)
    if 'MES' in df_temp.columns:
        df_mes = df_temp[df_temp['MES'] == mes_nombre]
    else:
        # Fallback a filtro por FECHA si MES no existe
        df_temp['FECHA'] = pd.to_datetime(df_temp['FECHA'], errors='coerce')
        if fecha_mes_es_noviembre:
            df_mes = df_temp[
                ((df_temp['FECHA'].dt.month == 10) | (df_temp['FECHA'].dt.month == 11))
            ]
        else:
            df_mes = df_temp[df_temp['FECHA'].dt.month == fecha_mes_num]
    
    # Aplicar regla: Solo INSTALADO
    df_instaladas = df_mes[df_mes['ESTADO'] == 'INSTALADO']
    
    return len(df_instaladas)

@st.cache_data(ttl=3600)
def get_nombres_alternativos(asesor):
    """Obtiene múltiples variantes del nombre del asesor para búsqueda flexible"""
    nombres = [asesor.strip()]
    # Agregar variante sin números al final (ej: ST2_VTP -> ST_VTP)
    import re
    nombre_sin_num = re.sub(r'(\d+)(_VTP)$', r'\2', asesor)
    if nombre_sin_num != asesor:
        nombres.append(nombre_sin_num)
    # Agregar variante con número (ej: ST_VTP -> ST2_VTP)
    nombre_con_num = re.sub(r'(_VTP)$', r'2_VTP', asesor.replace('2_VTP', '_VTP'))
    if nombre_con_num != asesor and '2_VTP' in nombre_con_num:
        nombres.append(nombre_con_num)
    return nombres

def get_pendientes_asesor_mes(asesor, mes_seleccionado="Enero"):
    """Obtiene cantidad de transacciones PENDIENTE por asesor para un mes"""
    df_drive = load_drive_data()
    
    if df_drive is None or df_drive.empty:
        return 0
    
    # Limpiar espacios en los nombres de asesor
    df_drive['ASESOR'] = df_drive['ASESOR'].astype(str).str.strip()
    asesor = asesor.strip()
    
    # Obtener nombres alternativos
    nombres_alternativos = get_nombres_alternativos(asesor)
    
    # Filtrar por mes y asesor (probando múltiples nombres)
    if 'MES' in df_drive.columns:
        df_mes_asesor = df_drive[(df_drive['MES'] == mes_seleccionado) & (df_drive['ASESOR'].isin(nombres_alternativos))]
    else:
        mes_numeros = {
            'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
            'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
            'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
        }
        mes_num = mes_numeros.get(mes_seleccionado, None)
        if mes_num is None:
            return 0
        df_drive['FECHA'] = pd.to_datetime(df_drive['FECHA'], errors='coerce')
        df_mes_asesor = df_drive[(df_drive['FECHA'].dt.month == mes_num) & (df_drive['ASESOR'].isin(nombres_alternativos))]
    
    # Contar PENDIENTE
    df_mes_asesor['ESTADO'] = df_mes_asesor['ESTADO'].astype(str).str.strip()
    pendientes = len(df_mes_asesor[df_mes_asesor['ESTADO'] == 'PENDIENTE'])
    return pendientes

def get_conversion_asesor_mes(asesor, mes_seleccionado="Noviembre"):
    """Calcula la conversión por asesor: Total Transacciones (DRIVE) / Con Cobertura (MANTRA)
    Usando datos de DRIVE y MANTRA"""
    df_mantra = load_mantra_data()
    df_drive = load_drive_data()
    
    if df_mantra is None or df_mantra.empty or df_drive is None or df_drive.empty:
        return 0
    
    # Limpiar espacios en los nombres de asesor
    df_mantra['Agente'] = df_mantra['Agente'].astype(str).str.strip()
    df_drive['ASESOR'] = df_drive['ASESOR'].astype(str).str.strip()
    asesor = asesor.strip()
    
    # Obtener nombres alternativos
    nombres_alternativos = get_nombres_alternativos(asesor)
    
    # Obtener Con Cobertura del asesor en MANTRA para el mes
    # Probar múltiples nombres
    df_mes_mantra = None
    for nombre in nombres_alternativos:
        df_temp = df_mantra[(df_mantra['Mes'] == mes_seleccionado) & (df_mantra['Agente'] == nombre)].copy()
        if not df_temp.empty:
            df_mes_mantra = df_temp
            break
    
    if df_mes_mantra is None or df_mes_mantra.empty:
        return 0
    
    df_mes_mantra['NIVEL 2'] = df_mes_mantra['NIVEL 2'].astype(str).str.strip()
    con_cobertura_asesor = len(df_mes_mantra[df_mes_mantra['NIVEL 2'] == 'Con Cobertura'])
    
    if con_cobertura_asesor == 0:
        return 0
    
    # Obtener Total de Transacciones del asesor en DRIVE
    # Usar columna MES si existe, sino usar FECHA
    if 'MES' in df_drive.columns:
        df_mes_drive = df_drive[(df_drive['MES'] == mes_seleccionado) & (df_drive['ASESOR'].isin(nombres_alternativos))]
    else:
        df_drive['FECHA'] = pd.to_datetime(df_drive['FECHA'], errors='coerce')
        mes_numeros = {
            'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
            'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
            'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
        }
        mes_num = mes_numeros.get(mes_seleccionado, None)
        if mes_num is None:
            return 0
        df_mes_drive = df_drive[(df_drive['FECHA'].dt.month == mes_num) & (df_drive['ASESOR'].isin(nombres_alternativos))]
    
    total_transacciones_asesor = len(df_mes_drive)
    
    if total_transacciones_asesor == 0:
        return 0
    
    # Conversión = Total Transacciones del Asesor / Con Cobertura del Asesor
    conversion_pct = round((total_transacciones_asesor / con_cobertura_asesor * 100)) if con_cobertura_asesor > 0 else 0
    return conversion_pct

def calculate_drive_metrics(metas_dict, mes_filtro=None, mes_nombre=None):

    """
    Calcula Cumplimiento y Efectividad por asesor usando datos de DRIVE
    
    Cumplimiento = INSTALADAS / META
    Efectividad = INSTALADAS / (INSTALADAS + CANCELADAS)
    """
    df_drive = load_drive_data()
    
    if df_drive is None or df_drive.empty:
        return {}
    
    # Extraer columnas necesarias
    df_drive = df_drive[['FECHA', 'MES', 'ASESOR', 'ESTADO', 'PAGO']].copy()
    
    # Filtrar por mes usando columna MES si está disponible
    if mes_nombre and 'MES' in df_drive.columns:
        df_drive = df_drive[df_drive['MES'] == mes_nombre]
    elif mes_filtro:
        # Fallback a FECHA si MES no existe
        df_drive['FECHA'] = pd.to_datetime(df_drive['FECHA'], errors='coerce')
        df_drive = df_drive[df_drive['FECHA'].dt.month == mes_filtro]
    
    # Contar INSTALADOS por asesor (solo INSTALADO, sin PENDIENTE)
    df_drive_temp = df_drive.copy()
    df_drive_temp['ESTADO'] = df_drive_temp['ESTADO'].astype(str).str.strip()
    
    # Solo INSTALADO
    df_instalados = df_drive_temp[df_drive_temp['ESTADO'] == 'INSTALADO']
    instalados_por_asesor = df_instalados.groupby('ASESOR').size()
    
    # Contar CANCELADOS por asesor
    cancelados_por_asesor = df_drive[df_drive['ESTADO'] == 'CANCELADO'].groupby('ASESOR').size()
    
    # Calcular métricas
    metricas = {}
    for asesor, meta in metas_dict.items():
        instalados = instalados_por_asesor.get(asesor, 0)
        cancelados = cancelados_por_asesor.get(asesor, 0)
        
        # Cumplimiento = INSTALADAS / META
        cumplimiento = round((instalados / meta * 100) if meta > 0 else 0)
        
        # Efectividad = Nueva fórmula: Contrato OK / Con Cobertura (de MANTRA)
        efectividad = get_conversion_asesor_mes(asesor, mes_nombre)
        
        metricas[asesor] = {
            'instalados': instalados,
            'cancelados': cancelados,
            'cumplimiento': cumplimiento,
            'efectividad': efectividad
        }
    
    return metricas

# Cargar datos
def load_data(mes_seleccionado=None):
    # Cargar la hoja LISTA para obtener metas por mes
    df_lista = load_lista_metas()
    
    # Crear diccionario de metas para el mes seleccionado
    metas_dict = {}
    
    if df_lista is not None and not df_lista.empty:
        # Filtrar por el mes seleccionado
        df_mes_metas = df_lista[df_lista['Mes'] == mes_seleccionado]
        
        # Crear diccionario {Asesor: Meta} SOLO con los asesores activos en este mes
        for idx, row in df_mes_metas.iterrows():
            metas_dict[row['Asesor']] = int(row['Meta'])
    
    # Si no hay datos para el mes en LISTA, retornar vacío
    if not metas_dict:
        metas_dict = {}
    
    # Determinar número de mes
    mes_numeros = {
        'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
        'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
        'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
    }
    mes_num = mes_numeros.get(mes_seleccionado, None)
    
    # Obtener métricas de DRIVE filtrando por mes (ahora con mes_nombre)
    metricas = calculate_drive_metrics(metas_dict, mes_filtro=mes_num, mes_nombre=mes_seleccionado)
    
    # Construir DataFrame
    empleados = []
    metas = []
    cumplimientos = []
    efectividades = []
    instaladas = []
    canceladas = []
    
    for empleado, meta in metas_dict.items():
        empleados.append(empleado)
        metas.append(meta)
        
        if empleado in metricas:
            cumplimientos.append(metricas[empleado]['cumplimiento'])
            efectividades.append(metricas[empleado]['efectividad'])
            instaladas.append(metricas[empleado]['instalados'])
            canceladas.append(metricas[empleado]['cancelados'])
        else:
            cumplimientos.append(0)
            efectividades.append(0)
            instaladas.append(0)
            canceladas.append(0)
    
    data = {
        'Empleado': empleados,
        'Meta': metas,
        'Instaladas': instaladas,
        'Canceladas': canceladas,
        'Cumplimiento': cumplimientos,
        'Efectividad': efectividades
    }
    
    df = pd.DataFrame(data)
    df['% Meta Alcanzado'] = (df['Cumplimiento'] / 100 * 100).astype(int)
    df['Diferencia'] = df['Cumplimiento'] - 100
    return df

# Estilos mejorados con tema moderno y premium
st.markdown("""
<style>
    :root {
        --primary-color: #0066cc;
        --secondary-color: #00d4ff;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --dark-bg: #0f172a;
        --light-bg: #f8fafc;
        --card-bg: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --border-color: #e2e8f0;
    }

    * {
        font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
        margin: 0;
        padding: 0;
    }

    body {
        background-color: #f0f4f8;
    }

    /* HEADER PRINCIPAL */
    .header-container {
        background: linear-gradient(135deg, #0066cc 0%, #00d4ff 100%);
        padding: 40px 30px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 10px 40px rgba(0, 102, 204, 0.2);
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }

    .header-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        z-index: 0;
    }

    .header-content {
        position: relative;
        z-index: 1;
    }

    .header-title {
        font-size: 2.8em;
        font-weight: 800;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .header-subtitle {
        font-size: 1.3em;
        font-weight: 400;
        opacity: 0.95;
        margin-top: 5px;
    }

    /* KPI CARDS */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 12px;
        margin-bottom: 30px;
    }

    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 160px;
    }

    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 102, 204, 0.15);
        border-color: #0066cc;
    }

    .kpi-icon {
        font-size: 1.6em;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 2.2em;
        font-weight: 800;
        color: #0066cc;
        margin: 8px 0;
        font-family: 'Courier New', monospace;
        line-height: 1.2;
    }

    .kpi-label {
        font-size: 0.75em;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        line-height: 1.3;
        word-wrap: break-word;
    }

    /* SECCIÓN TÍTULOS */
    .section-title {
        font-size: 1.6em;
        font-weight: 700;
        color: #1e293b;
        margin: 30px 0 20px 0;
        padding-bottom: 12px;
        border-bottom: 3px solid #0066cc;
        display: inline-block;
    }

    /* TABLA META */
    .meta-tabla {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid #e2e8f0;
    }

    .meta-tabla table {
        width: 100%;
        border-collapse: collapse;
    }

    .meta-tabla thead {
        background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
        color: white;
        font-weight: 700;
    }

    .meta-tabla th {
        padding: 4px 2px;
        text-align: left;
        font-size: 0.8em;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .meta-tabla td {
        padding: 2px 2px;
        border-bottom: 1px solid #f1f5f9;
        font-size: 0.8em;
    }

    .meta-tabla tbody tr {
        transition: background-color 0.2s ease;
    }

    .meta-tabla tbody tr:hover {
        background-color: #f8fafc;
    }

    .meta-tabla tbody tr:nth-child(odd) {
        background-color: #f9fafc;
    }

    .meta-valor {
        font-weight: 700;
        text-align: center;
        border-radius: 8px;
        padding: 3px 8px;
        display: inline-block;
        min-width: 40px;
        font-size: 0.85em;
        background: linear-gradient(135deg, #f59e0b 0%, #f97316 100%);
        color: white;
    }

    .meta-total {
        background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
        color: white;
        font-weight: 800 !important;
    }

    .meta-total-row {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        font-weight: 700;
    }

    /* CARDS DE GRÁFICOS */
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid #e2e8f0;
    }

    .chart-title {
        font-size: 1.2em;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* TABLA RESUMEN */
    .resumen-tabla {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid #e2e8f0;
    }

    .resumen-tabla table {
        width: 100%;
        border-collapse: collapse;
    }

    .resumen-tabla thead {
        background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
        color: white;
    }

    .resumen-tabla th {
        padding: 10px 6px;
        text-align: center;
        font-size: 0.7em;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .resumen-tabla td {
        padding: 8px 6px;
        border-bottom: 1px solid #f1f5f9;
        text-align: center;
        font-weight: 600;
        font-size: 0.85em;
    }

    .resumen-tabla tbody tr:hover {
        background-color: #f8fafc;
    }

    /* INDICADORES DE ESTADO */
    .status-excellent {
        color: #10b981;
        background: #dcfce7;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 700;
    }

    .status-good {
        color: #f59e0b;
        background: #fef3c7;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 700;
    }

    .status-poor {
        color: #ef4444;
        background: #fee2e2;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 700;
    }

    /* BOTONES */
    .filter-button {
        padding: 10px 16px;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        background: white;
        color: #1e293b;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .filter-button:hover {
        border-color: #0066cc;
        color: #0066cc;
    }

    /* DIVIDER */
    .section-divider {
        margin: 40px 0;
        border: none;
        border-top: 2px solid #e2e8f0;
    }

    /* FOOTER */
    .footer-container {
        text-align: center;
        color: #94a3b8;
        margin-top: 50px;
        padding: 30px;
        font-size: 0.9em;
    }

    .footer-container p {
        margin: 5px 0;
    }

    /* STREAMLIT CUSTOMIZATION */
    [data-testid="stDataFrame"] {
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    /* SELECTBOX STYLING */
    .stSelectbox {
        border-radius: 8px !important;
    }

    /* TABS */
    [data-testid="stTabs"] {
        margin-top: 20px;
    }

    /* SCROLLBAR */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }

    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }

    @media (max-width: 1400px) {
        .kpi-container {
            grid-template-columns: repeat(3, 1fr);
        }
    }

    @media (max-width: 768px) {
        .kpi-container {
            grid-template-columns: repeat(2, 1fr);
        }

        .header-title {
            font-size: 2em;
        }
    }
</style>
""", unsafe_allow_html=True)

# Filtros mejorados con layout dinámico
st.markdown("### 🎛️ Filtros y Opciones")
col_filtros = st.columns(3, gap="medium")

with col_filtros[0]:
    mes = st.selectbox("📅 Selecciona Mes", ["Noviembre", "Diciembre", "Enero"], index=2)

# Mapeo de meses a años
mes_año_map = {
    "Noviembre": "Noviembre 2025",
    "Diciembre": "Diciembre 2025",
    "Enero": "Enero 2026"
}

# Header mejorado - Dinámico
st.markdown(f"""
<div class="header-container">
    <div class="header-content">
        <div class="header-title">🌐 WORLD TEL</div>
        <div class="header-subtitle">Dashboard de Cumplimiento Mensual - {mes_año_map[mes]}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Cargar datos con el mes seleccionado
df = load_data(mes)

with col_filtros[1]:
    opciones_empleados = ["Todos"] + sorted(df['Empleado'].unique())
    empleado_seleccionado = st.selectbox("👤 Filtrar por Empleado", opciones_empleados)

vista = "Completa"

# Obtener valores del Excel basado en el mes seleccionado
total_leads_excel, total_conversion_excel = get_total_leads_and_conversion(mes)

# KPI Cards mejorados - Datos del asesor seleccionado o totales
def get_cumplimiento_total_mes(mes_nombre):
    """Calcula el cumplimiento total del mes: (Total Instaladas / Total de Metas) * 100"""
    df_lista = load_lista_metas()
    df_drive = load_drive_data()
    
    if df_lista is None or df_lista.empty or df_drive is None or df_drive.empty:
        return 0
    
    try:
        # Mapear nombre del mes a número
        mes_numeros = {
            'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
            'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
            'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
        }
        mes_num = mes_numeros.get(mes_nombre)
        
        if mes_num is None:
            return 0
        
        # Obtener total de metas para el mes
        df_mes_metas = df_lista[df_lista['Mes'] == mes_nombre]
        total_metas = df_mes_metas['Meta'].sum()
        
        if total_metas == 0:
            return 0
        
        # Aplicar regla: INSTALADO - pasando mes_nombre para filtrar por MES column
        es_noviembre = mes_num == 11
        total_instaladas = count_instaladas_con_regla(df_drive, mes_num, es_noviembre, mes_nombre)
        
        # Calcular cumplimiento
        cumplimiento_total = round((total_instaladas / total_metas * 100))
        
        return cumplimiento_total
    except Exception as e:
        return 0

def get_efectividad_mes(mes_nombre):
    """Calcula la efectividad para un mes: INSTALADAS/(INSTALADAS+CANCELADAS)
    Donde INSTALADAS = INSTALADO (sin PENDIENTE)"""
    df_drive = load_drive_data()
    
    if df_drive is None or df_drive.empty:
        return 0
    
    try:
        # Mapear nombre del mes a número
        mes_numeros = {
            'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
            'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
            'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
        }
        mes_num = mes_numeros.get(mes_nombre)
        
        if mes_num is None:
            return 0
        
        # Filtrar por MES en lugar de FECHA
        if 'MES' in df_drive.columns:
            df_filtrado = df_drive[df_drive['MES'] == mes_nombre]
        else:
            # Fallback a FECHA si MES no existe
            df_drive['FECHA'] = pd.to_datetime(df_drive['FECHA'], errors='coerce')
            # Para Noviembre, incluir Octubre + Noviembre
            if mes_num == 11:
                df_filtrado = df_drive[
                    ((df_drive['FECHA'].dt.month == 10) | (df_drive['FECHA'].dt.month == 11))
                ]
            else:
                # Para otros meses, solo ese mes
                df_filtrado = df_drive[
                    (df_drive['FECHA'].dt.month == mes_num)
                ]
        
        # Contar instaladas con regla (solo INSTALADO)
        instaladas = count_instaladas_con_regla(df_filtrado, mes_num, mes_num == 11, mes_nombre)
        canceladas = len(df_filtrado[df_filtrado['ESTADO'] == 'CANCELADO'])
        
        # Calcular efectividad
        total_transacciones = instaladas + canceladas
        if total_transacciones > 0:
            efectividad = round((instaladas / total_transacciones * 100))
        else:
            efectividad = 0
        
        return efectividad
    except Exception as e:
        return 0
        
        # Calcular efectividad
        total_transacciones = instaladas + canceladas
        if total_transacciones > 0:
            efectividad = round((instaladas / total_transacciones * 100))
        else:
            efectividad = 0
        
        return efectividad
    except Exception as e:
        return 0

def get_ventas_mes(mes_nombre):
    """Obtiene el total de instaladas para un mes específico del DRIVE
    Donde INSTALADAS = Solo INSTALADO (no incluye PENDIENTE)
    Filtra por columna MES"""
    df_drive = load_drive_data()
    
    if df_drive is None or df_drive.empty:
        return 0
    
    try:
        # Mapear nombre del mes a número
        mes_numeros = {
            'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
            'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
            'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
        }
        mes_num = mes_numeros.get(mes_nombre)
        
        if mes_num is None:
            return 0
        
        # Convertir FECHA a datetime
        df_drive['FECHA'] = pd.to_datetime(df_drive['FECHA'], errors='coerce')
        
        # Para Noviembre, sumar Octubre + Noviembre
        es_noviembre = mes_num == 11
        total = count_instaladas_con_regla(df_drive, mes_num, es_noviembre, mes_nombre)
        return total
    except Exception as e:
        return 0

st.markdown("")  # Espaciador

col1, col2, col3, col4, col5, col6 = st.columns(6, gap="small")

if empleado_seleccionado == "Todos":
    # Preparar datos según vista
    df_vista = df[['Empleado', 'Cumplimiento']].copy()
    
    if vista == "Top 5":
        df_vista = df_vista.nlargest(5, 'Cumplimiento')
    elif vista == "Últimos 5":
        df_vista = df_vista.nsmallest(5, 'Cumplimiento')
    
    # Obtener asesores en la vista
    asesores_vista = df_vista['Empleado'].tolist()
    
    # Obtener ventas totales, efectividad y cumplimiento total del mes actual desde DRIVE
    # SIN filtrar por asesores - mostrar TOTALES de TODOS
    df_drive_filtrado = load_drive_data()
    
    if df_drive_filtrado is not None and not df_drive_filtrado.empty:
        # NO filtrar por asesores - calcular para TODOS
        # df_drive_filtrado = df_drive_filtrado[df_drive_filtrado['ASESOR'].isin(asesores_vista)]
        
        # Calcular métricas para esta vista
        df_drive_filtrado['FECHA'] = pd.to_datetime(df_drive_filtrado['FECHA'], errors='coerce')
        
        # Determinar número de mes
        mes_numeros = {
            'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
            'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
            'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
        }
        mes_num = mes_numeros.get(mes, None)
        
        # Filtrar por columna MES (en lugar de por FECHA)
        if 'MES' in df_drive_filtrado.columns:
            df_mes_filtrado = df_drive_filtrado[df_drive_filtrado['MES'] == mes]
        else:
            # Fallback a FECHA si MES no existe
            df_drive_filtrado['FECHA'] = pd.to_datetime(df_drive_filtrado['FECHA'], errors='coerce')
            if mes_num == 11:
                df_mes_filtrado = df_drive_filtrado[
                    ((df_drive_filtrado['FECHA'].dt.month == 10) | (df_drive_filtrado['FECHA'].dt.month == 11))
                ]
            else:
                df_mes_filtrado = df_drive_filtrado[df_drive_filtrado['FECHA'].dt.month == mes_num]
        
        # Ventas (instaladas) - aplicando regla: Solo INSTALADO
        ventas_total = count_instaladas_con_regla(df_mes_filtrado, mes_num, mes_num == 11, mes)
        
        # Efectividad - Nueva fórmula: Contrato OK / Con Cobertura (de MANTRA)
        efectividad_mes = get_conversion_mantra_mes(mes)
        
        # Cumplimiento - calcular contra TODAS las metas del mes
        df_lista = load_lista_metas()
        df_mes_metas = df_lista[df_lista['Mes'] == mes]
        total_metas = df_mes_metas['Meta'].sum()
        cumplimiento_total = round((ventas_total / total_metas * 100)) if total_metas > 0 else 0
        
        # Ventas generales (total de todas las transacciones)
        ventas_generales = get_ventas_generales_mes(mes)
    else:
        ventas_total = 0
        efectividad_mes = 0
        cumplimiento_total = 0
        ventas_generales = 0
    
    kpis = [
        (f"{total_leads_excel:,}", "📊 Leads", col1),
        (f"{total_conversion_excel}", "✅ Ventas Del Mes", col2),
        (str(ventas_total), "💰 Ventas Instaladas Del Mes", col3),
        (str(ventas_generales), "📈 Ventas Generales Del Mes", col4),
        (f"{efectividad_mes}%", "⭐ Conversión de Ventas", col5),
        (f"{cumplimiento_total}%", "🎯 Cumplimiento", col6),
    ]
else:
    empleado_data = df[df['Empleado'] == empleado_seleccionado].iloc[0]
    cumpl_val = int(empleado_data['Cumplimiento'])
    efect_val = int(empleado_data['Efectividad'])
    
    kpis = [
        (str(int(empleado_data['Meta'])), "📊 Meta", col1),
        (f"{cumpl_val}%", "✅ Cumplimiento", col2),
        (f"{efect_val}%", "⭐ Conversión de Ventas", col3),
        ("70%", "🎯 Cumplimiento", col4),
        ("🟢 Excelente" if cumpl_val >= 70 else "🟡 Bueno" if cumpl_val >= 40 else "🔴 Bajo", "📈 Estado", col5),
    ]

for valor, label, col in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label.split(' ', 1)[1]}</div>
            <div class="kpi-value">{valor}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Sección principal con 3 columnas mejorada - RESPONSIVO
st.markdown("### 📊 Análisis de Desempeño por Agente")
col1, col2, col3 = st.columns([1.2, 1.4, 1.4], gap="medium")

# Columna 1: Meta Mensual
with col1:
    st.markdown('<div class="chart-title">📈 Meta Mensual</div>', unsafe_allow_html=True)
    tabla_meta = df[['Empleado', 'Meta']].copy()
    tabla_meta = tabla_meta.sort_values('Meta', ascending=False).reset_index(drop=True)
    tabla_meta.index = tabla_meta.index + 1
    
    # Crear HTML para la tabla personalizada
    html_tabla = '<div class="meta-tabla" style="width: auto; max-width: none;"><table style="table-layout: fixed;"><thead><tr><th style="width: 25px;">Pos</th><th style="width: 120px;">Empleado</th><th style="width: 60px; text-align: center;">Meta</th></tr></thead><tbody>'
    
    for idx, row in tabla_meta.iterrows():
        empleado = row['Empleado']
        meta = int(row['Meta'])
        html_tabla += f'<tr><td style="font-weight: 700; text-align: center; color: #0066cc;">#{idx}</td><td style="font-weight: 600; overflow: hidden; text-overflow: ellipsis;">{empleado}</td><td style="text-align: center;"><div class="meta-valor">{meta}</div></td></tr>'
    
    # Agregar fila de totales
    total_meta = int(tabla_meta['Meta'].sum())
    html_tabla += f'<tr style="background-color: #e0e7ff; font-weight: 700; border-top: 2px solid #0066cc;"><td style="text-align: center; color: #0066cc;">∑</td><td style="font-weight: 700; color: #0066cc;">TOTAL</td><td style="text-align: center; font-weight: 700; color: #0066cc;"><div class="meta-valor" style="background-color: #0066cc; color: white;">{total_meta}</div></td></tr>'
    
    html_tabla += '</tbody></table></div>'
    
    st.markdown(html_tabla, unsafe_allow_html=True)

# Columna 2: Cumplimiento por Agente
with col2:
    st.markdown('<div class="chart-title">📊 Cumplimiento por Agente (%)</div>', unsafe_allow_html=True)
    df_sorted = df.sort_values('Cumplimiento', ascending=True)
    
    # Crear colores degradados basados en cumplimiento
    def get_color(val):
        if val >= 100:
            return '#10b981'  # Verde
        elif val >= 75:
            return '#f59e0b'  # Naranja
        elif val >= 50:
            return '#f97316'  # Naranja oscuro
        else:
            return '#ef4444'  # Rojo
    
    colors = [get_color(x) for x in df_sorted['Cumplimiento']]
    
    fig_cumpl = go.Figure()
    fig_cumpl.add_trace(go.Bar(
        y=df_sorted['Empleado'],
        x=df_sorted['Cumplimiento'],
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='white', width=2),
            opacity=0.85
        ),
        text=df_sorted['Cumplimiento'].apply(lambda x: f'{x}%'),
        textposition='outside',
        textfont=dict(size=13, color='#1e293b', family='Arial', weight='bold'),
        hovertemplate='<b>%{y}</b><br><b>Cumplimiento:</b> <b>%{x}%</b><extra></extra>',
        name=''
    ))
    fig_cumpl.update_layout(
        height=580,
        margin=dict(l=160, r=50, t=20, b=20),
        showlegend=False,
        xaxis_title="",
        xaxis=dict(
            gridcolor='rgba(0,0,0,0.05)',
            showgrid=True,
            zeroline=False,
            tickfont=dict(size=11, color='#64748b'),
            range=[0, 130],
            ticksuffix='%'
        ),
        yaxis=dict(
            tickfont=dict(size=9, color='#1e293b'),
            automargin=True
        ),
        plot_bgcolor='rgba(248, 250, 252, 0.5)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=11, family='Arial', color='#1e293b'),
        hovermode='closest'
    )
    st.plotly_chart(fig_cumpl, use_container_width=True, config={'displayModeBar': False})

# Columna 3: Conversión de Ventas por Agente
with col3:
    st.markdown('<div class="chart-title">⭐ Conversión de Ventas por Agente (%)</div>', unsafe_allow_html=True)
    df_sorted_eff = df.sort_values('Efectividad', ascending=True)
    
    colors_eff = [get_color(x) for x in df_sorted_eff['Efectividad']]
    
    fig_eff = go.Figure()
    fig_eff.add_trace(go.Bar(
        y=df_sorted_eff['Empleado'],
        x=df_sorted_eff['Efectividad'],
        orientation='h',
        marker=dict(
            color=colors_eff,
            line=dict(color='white', width=2),
            opacity=0.85
        ),
        text=df_sorted_eff['Efectividad'].apply(lambda x: f'{x}%'),
        textposition='outside',
        textfont=dict(size=13, color='#1e293b', family='Arial', weight='bold'),
        hovertemplate='<b>%{y}</b><br><b>Efectividad:</b> <b>%{x}%</b><extra></extra>',
        name=''
    ))
    fig_eff.update_layout(
        height=580,
        margin=dict(l=160, r=50, t=20, b=20),
        showlegend=False,
        xaxis_title="",
        xaxis=dict(
            gridcolor='rgba(0,0,0,0.05)',
            showgrid=True,
            zeroline=False,
            tickfont=dict(size=11, color='#64748b'),
            range=[0, 110],
            ticksuffix='%'
        ),
        yaxis=dict(
            tickfont=dict(size=9, color='#1e293b'),
            automargin=True
        ),
        plot_bgcolor='rgba(248, 250, 252, 0.5)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=11, family='Arial', color='#1e293b'),
        hovermode='closest'
    )
    st.plotly_chart(fig_eff, use_container_width=True, config={'displayModeBar': False})

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Tabla de detalle de empleados
st.markdown("### 👥 Detalle Completo de Empleados")

# Filtro para ordenamiento
criterio_orden = st.selectbox(
    "Ordenar por:",
    ["Cumplimiento (Mayor a Menor)", "Conversión (Mayor a Menor)"],
    key="criterio_orden"
)

df_detail = df[['Empleado', 'Meta', 'Instaladas', 'Canceladas', 'Cumplimiento', 'Efectividad']].copy()
df_detail['Cumpl%'] = df_detail['Cumplimiento'].astype(str) + '%'
df_detail['Efect%'] = df_detail['Efectividad'].astype(str) + '%'

# Agregar columna de Pendientes solo para el mes actual (Enero)
if mes == "Enero":
    pendientes_list = []
    for empleado in df_detail['Empleado']:
        pendientes = get_pendientes_asesor_mes(empleado, mes)
        pendientes_list.append(pendientes)
    df_detail['Pendientes'] = pendientes_list
else:
    df_detail['Pendientes'] = 0

# Separar en Full Time (meta >= 55) y Part Time (meta < 55)
df_fulltime = df_detail[df_detail['Meta'] >= 55].copy()
df_parttime = df_detail[df_detail['Meta'] < 55].copy()

# Ordenar por el criterio seleccionado
if criterio_orden == "Conversión (Mayor a Menor)":
    df_fulltime = df_fulltime.sort_values('Efectividad', ascending=False).reset_index(drop=True)
    df_parttime = df_parttime.sort_values('Efectividad', ascending=False).reset_index(drop=True)
else:
    df_fulltime = df_fulltime.sort_values('Cumplimiento', ascending=False).reset_index(drop=True)
    df_parttime = df_parttime.sort_values('Cumplimiento', ascending=False).reset_index(drop=True)

# Función para generar tabla HTML
def generar_tabla_detalle(df_tabla, tipo_empleado):
    if mes == "Enero":
        html_tabla = '<div class="meta-tabla"><table><thead><tr><th style="width: 5%;">Pos</th><th style="width: 20%;">Empleado</th><th style="width: 7%;">Meta</th><th style="width: 9%;">Inst</th><th style="width: 9%;">Canc</th><th style="width: 9%;">Pend</th><th style="width: 10%;">Cumpl%</th><th style="width: 11%;">Conv%</th><th style="width: 15%;">Estado</th></tr></thead><tbody>'
    else:
        html_tabla = '<div class="meta-tabla"><table><thead><tr><th style="width: 6%;">Pos</th><th style="width: 25%;">Empleado</th><th style="width: 8%;">Meta</th><th style="width: 10%;">Instaladas</th><th style="width: 10%;">Canceladas</th><th style="width: 12%;">Cumpl%</th><th style="width: 12%;">Conv.Vent%</th><th style="width: 17%;">Estado</th></tr></thead><tbody>'

    for idx, (_, row) in enumerate(df_tabla.iterrows(), 1):
        empleado = row['Empleado']
        meta = int(row['Meta'])
        instaladas = int(row['Instaladas'])
        canceladas = int(row['Canceladas'])
        pendientes = int(row['Pendientes']) if mes == "Enero" else 0
        cumpl = int(row['Cumplimiento'])
        efect = int(row['Efectividad'])
        
        # Determinar estado
        if cumpl >= 70:
            estado = '<span class="status-excellent">✓ Excelente</span>'
            fila_bg = 'background-color: #f0fdf4;'
        elif cumpl >= 40:
            estado = '<span class="status-good">~ Bueno</span>'
            fila_bg = 'background-color: #fffbeb;'
        else:
            estado = '<span class="status-poor">✗ Bajo</span>'
            fila_bg = 'background-color: #fef2f2;'
        
        if mes == "Enero":
            html_tabla += f'''<tr style="{fila_bg}">
                <td style="font-weight: 700; text-align: center; color: #0066cc;">#{idx}</td>
                <td style="font-weight: 600;">{empleado}</td>
                <td style="text-align: center; font-weight: 600;">{meta}</td>
                <td style="text-align: center; font-weight: 600; color: #10b981;">{instaladas}</td>
                <td style="text-align: center; font-weight: 600; color: #ef4444;">{canceladas}</td>
                <td style="text-align: center; font-weight: 600; color: #f59e0b;">{pendientes}</td>
                <td style="text-align: center;"><div class="meta-valor">{cumpl}%</div></td>
                <td style="text-align: center;"><div class="meta-valor" style="background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);">{efect}%</div></td>
                <td style="text-align: center;">{estado}</td>
            </tr>'''
        else:
            html_tabla += f'''<tr style="{fila_bg}">
                <td style="font-weight: 700; text-align: center; color: #0066cc;">#{idx}</td>
                <td style="font-weight: 600;">{empleado}</td>
                <td style="text-align: center; font-weight: 600;">{meta}</td>
                <td style="text-align: center; font-weight: 600; color: #10b981;">{instaladas}</td>
                <td style="text-align: center; font-weight: 600; color: #ef4444;">{canceladas}</td>
                <td style="text-align: center;"><div class="meta-valor">{cumpl}%</div></td>
                <td style="text-align: center;"><div class="meta-valor" style="background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);">{efect}%</div></td>
                <td style="text-align: center;">{estado}</td>
            </tr>'''

    html_tabla += '</tbody></table></div>'
    return html_tabla

# Mostrar tabla Full Time
if not df_fulltime.empty:
    st.markdown("#### 💼 Empleados Full Time (8 horas - Meta ≥ 55)")
    html_fulltime = generar_tabla_detalle(df_fulltime, "Full Time")
    st.markdown(html_fulltime, unsafe_allow_html=True)
    st.markdown('<div style="margin: 15px 0;"></div>', unsafe_allow_html=True)

# Mostrar tabla Part Time
if not df_parttime.empty:
    st.markdown("#### ⏢ Empleados Part Time (4 horas - Meta < 55)")
    html_parttime = generar_tabla_detalle(df_parttime, "Part Time")
    st.markdown(html_parttime, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Tabla de resumen mensual
st.markdown("### 📊 Resumen Mensual Completo")

st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)

# Obtener datos para cada mes
meses_disponibles = ['Noviembre', 'Diciembre', 'Enero']
datos_meses = []
totales = {'Leads': 0, 'Contr': 0, 'Cober': 0}

for mes_nombre in meses_disponibles:
    leads, conversion = get_total_leads_and_conversion(mes_nombre)
    con_cobertura = get_con_cobertura_count(mes_nombre)
    cancelados = get_cancelados_mes(mes_nombre)
    instaladas = get_instaladas_mes(mes_nombre)
    no_pago = get_no_pago_mes(mes_nombre)
    no_responde = get_no_responde_mes(mes_nombre)
    no_especifica = get_no_especifica_mes(mes_nombre)
    sin_cobertura = get_sin_cobertura_mes(mes_nombre)
    datos_meses.append({
        'Mes': mes_nombre,
        'Leads': leads,
        'Cober': con_cobertura,
        'Contr': conversion,
        'Cancel': cancelados,
        'Pago': instaladas,
        'NoPago': no_pago,
        'NoResp': no_responde,
        'NoEsp': no_especifica,
        'SinCob': sin_cobertura
    })
    totales['Leads'] += leads
    totales['Cober'] += con_cobertura
    totales['Contr'] += conversion

# Construir resumen_data con datos dinámicos
resumen_data = {
    'Mes': [],
    'Leads': [],
    'Cober': [],
    '%Cob': [],
    'Contr': [],
    '%Conv': [],
    'Real': [],
    'Cancel': [],
    'Pagó': [],
    'NoPag': [],
    'Efect': [],
    'NoResp': [],
    '%NR': [],
    'NoEsp': [],
    '%NE': [],
    '%SC': []
}

# Agregar filas por mes
for dato in datos_meses:
    resumen_data['Mes'].append(dato['Mes'])
    resumen_data['Leads'].append(dato['Leads'])
    resumen_data['Cober'].append(dato['Cober'])
    cob_pct = f'{int(dato["Cober"]/dato["Leads"]*100) if dato["Leads"] > 0 else 0}%'
    resumen_data['%Cob'].append(cob_pct)
    resumen_data['Contr'].append(dato['Contr'])
    conv_pct = f'{int(dato["Contr"]/dato["Leads"]*100) if dato["Leads"] > 0 else 0}%'
    resumen_data['%Conv'].append(conv_pct)
    resumen_data['Real'].append('51%')
    resumen_data['Cancel'].append(dato['Cancel'])
    resumen_data['Pagó'].append(dato['Pago'])
    resumen_data['NoPag'].append(dato['NoPago'])
    # Calcular EFECT = PAGÓ / (CANCEL + PAGÓ + NOPAG)
    total_transacciones = dato['Cancel'] + dato['Pago'] + dato['NoPago']
    efect_pct = f'{int(dato["Pago"]/total_transacciones*100) if total_transacciones > 0 else 0}%'
    resumen_data['Efect'].append(efect_pct)
    resumen_data['NoResp'].append(dato['NoResp'])
    # Calcular %NR = NORESP / LEADS
    nr_pct = f'{int(dato["NoResp"]/dato["Leads"]*100) if dato["Leads"] > 0 else 0}%'
    resumen_data['%NR'].append(nr_pct)
    resumen_data['NoEsp'].append(dato['NoEsp'])
    # Calcular %NE = NOESP / LEADS
    ne_pct = f'{int(dato["NoEsp"]/dato["Leads"]*100) if dato["Leads"] > 0 else 0}%'
    resumen_data['%NE'].append(ne_pct)
    # Calcular %SC = SinCobertura / LEADS
    sc_pct = f'{int(dato["SinCob"]/dato["Leads"]*100) if dato["Leads"] > 0 else 0}%'
    resumen_data['%SC'].append(sc_pct)

df_resumen = pd.DataFrame(resumen_data)

# Crear tabla HTML personalizada para resumen
html_resumen = '<div class="resumen-tabla"><table><thead><tr>'
for col in df_resumen.columns:
    html_resumen += f'<th>{col}</th>'
html_resumen += '</tr></thead><tbody>'

for idx, row in df_resumen.iterrows():
    html_resumen += '<tr>'
    for col in df_resumen.columns:
        valor = row[col]
        html_resumen += f'<td>{valor}</td>'
    html_resumen += '</tr>'

html_resumen += '</tbody></table></div>'
st.markdown(html_resumen, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Footer elegante
st.markdown("""
<div class="footer-container">
    <p><strong>Dashboard WORLD TEL</strong> - Sistema de Control de Cumplimiento Mensual</p>
    <p>📅 Periodo: Noviembre 2025 | 🕐 Actualizado: {}  | 👥 Total Empleados: 14</p>
    <p style="margin-top: 15px; opacity: 0.7;">© 2025 WORLD TEL | Todos los derechos reservados</p>
</div>
""".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")), unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

st.set_page_config(
    page_title="Dashboard WORLD TEL - Cumplimiento Mensual",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar datos
@st.cache_data
def load_data():
    # Datos basados en la imagen proporcionada
    data = {
        'Empleado': ['ZIM_ALEXISGK_VTP', 'ZIM_CARLOCZ_VTP', 'ZIM_DANIELAAJ_VTP', 
                     'ZIM_FLAVIOTB_VTP', 'ZIM_HELBERTPJ_VTP', 'ZIM_INDIRAMM_VTP',
                     'ZIM_JESUSSZ_VTP', 'ZIM_JULIOLD_VTP', 'ZIM_KARINASE_VTP',
                     'ZIM_MELANYOA_VTP', 'ZIM_MILAGROSMM_VTP', 'ZIM_NERYIU_VTP',
                     'ZIM_STEVENCM_VTP', 'ZIM_ZOILASM_VTP'],
        'Meta': [30, 55, 9, 55, 23, 30, 28, 28, 55, 55, 60, 55, 30, 55],
        'Cumplimiento': [120, 5, 22, 40, 104, 67, 82, 7, 102, 36, 23, 102, 73, 47],
        'Efectividad': [73, 33, 38, 74, 63, 69, 70, 100, 84, 70, 94, 82, 60, 52]
    }
    df = pd.DataFrame(data)
    df['% Meta Alcanzado'] = (df['Cumplimiento'] / 100 * 100).astype(int)
    df['Diferencia'] = df['Cumplimiento'] - 100
    return df

df = load_data()

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
        grid-template-columns: repeat(5, 1fr);
        gap: 15px;
        margin-bottom: 30px;
    }

    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 22px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        position: relative;
    }

    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 102, 204, 0.15);
        border-color: #0066cc;
    }

    .kpi-icon {
        font-size: 1.8em;
        margin-bottom: 10px;
    }

    .kpi-value {
        font-size: 2.4em;
        font-weight: 800;
        color: #0066cc;
        margin: 10px 0;
        font-family: 'Courier New', monospace;
    }

    .kpi-label {
        font-size: 0.85em;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
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
        padding: 8px 6px;
        text-align: left;
        font-size: 0.8em;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .meta-tabla td {
        padding: 5px 6px;
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

# Header mejorado
st.markdown("""
<div class="header-container">
    <div class="header-content">
        <div class="header-title">🌐 WORLD TEL</div>
        <div class="header-subtitle">Dashboard de Cumplimiento Mensual - Noviembre 2025</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Filtros mejorados con layout dinámico
st.markdown("### 🎛️ Filtros y Opciones")
col_filtros = st.columns(3, gap="medium")

with col_filtros[0]:
    mes = st.selectbox("📅 Selecciona Mes", ["Noviembre", "Octubre", "Septiembre"])

with col_filtros[1]:
    opciones_empleados = ["Todos"] + sorted(df['Empleado'].unique())
    empleado_seleccionado = st.selectbox("👤 Filtrar por Empleado", opciones_empleados)

with col_filtros[2]:
    vista = st.selectbox("👁️ Vista de Datos", ["Completa", "Top 5", "Últimos 5"])

# KPI Cards mejorados - Datos del asesor seleccionado o totales
st.markdown("")  # Espaciador

col1, col2, col3, col4, col5 = st.columns(5, gap="small")

if empleado_seleccionado == "Todos":
    # Mostrar valores fijos del mes completo
    cumpl_val = 70
    
    kpis = [
        ("6,589", "📊 Leads", col1),
        ("299", "✅ Con Contrato", col2),
        ("397", "💰 Ventas Mes", col3),
        ("70%", "⭐ Efectividad", col4),
        ("39%", "🎯 Conversión", col5),
    ]
else:
    empleado_data = df[df['Empleado'] == empleado_seleccionado].iloc[0]
    cumpl_val = int(empleado_data['Cumplimiento'])
    efect_val = int(empleado_data['Efectividad'])
    
    kpis = [
        (str(int(empleado_data['Meta'])), "📊 Meta", col1),
        (f"{cumpl_val}%", "✅ Cumplimiento", col2),
        (f"{efect_val}%", "⭐ Efectividad", col3),
        ("70%", "🎯 Conversión", col4),
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

# Sección principal con 3 columnas mejorada
st.markdown("### 📊 Análisis de Desempeño por Agente")
col1, col2, col3 = st.columns([0.8, 1.6, 1.6], gap="small")

# Columna 1: Meta Mensual
with col1:
    st.markdown('<div class="chart-title">📈 Meta Mensual</div>', unsafe_allow_html=True)
    tabla_meta = df[['Empleado', 'Meta']].copy()
    tabla_meta = tabla_meta.sort_values('Meta', ascending=False).reset_index(drop=True)
    tabla_meta.index = tabla_meta.index + 1
    
    # Crear HTML para la tabla personalizada
    html_tabla = '<div class="meta-tabla"><table><thead><tr><th style="width: 10%;">Pos</th><th style="width: 50%;">Empleado</th><th style="width: 40%; text-align: center;">Meta</th></tr></thead><tbody>'
    
    for idx, row in tabla_meta.iterrows():
        empleado = row['Empleado']
        meta = int(row['Meta'])
        html_tabla += f'<tr><td style="font-weight: 700; text-align: center; color: #0066cc;">#{idx}</td><td style="font-weight: 600;">{empleado}</td><td style="text-align: center;"><div class="meta-valor">{meta}</div></td></tr>'
    
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

# Columna 3: Efectividad por Agente
with col3:
    st.markdown('<div class="chart-title">⭐ Efectividad por Agente (%)</div>', unsafe_allow_html=True)
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

# Tabla de resumen mensual
st.markdown("### 📊 Resumen Mensual Completo")

st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)

resumen_data = {
    'Mes': ['Noviembre', 'Total'],
    'Leads': [6589, 6589],
    'Cober': [774, 774],
    '%Cob': ['12%', '12%'],
    'Contr': [299, 299],
    '%Conv': ['39%', '39%'],
    'Real': ['51%', '51%'],
    'Cancel': [89, 89],
    'Pagó': [352, 352],
    'NoPag': [63, 63],
    'Efect': ['70%', '70%'],
    'NoResp': [2271, 2271],
    '%NR': ['34%', '34%'],
    'NoEsp': [1021, 1021],
    '%NE': ['15%', '15%'],
    '%SC': ['38%', '38%']
}

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
        if idx == 1:  # Fila de totales
            html_resumen += f'<td style="font-weight: 800; color: #0066cc;">{valor}</td>'
        else:
            html_resumen += f'<td>{valor}</td>'
    html_resumen += '</tr>'

html_resumen += '</tbody></table></div>'
st.markdown(html_resumen, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Tabla de detalle de empleados
st.markdown("### 👥 Detalle Completo de Empleados")

df_detail = df[['Empleado', 'Meta', 'Cumplimiento', 'Efectividad']].copy()
df_detail['Cumpl%'] = df_detail['Cumplimiento'].astype(str) + '%'
df_detail['Efect%'] = df_detail['Efectividad'].astype(str) + '%'

# Aplicar filtro de vista
if vista == "Top 5":
    df_detail = df_detail.nlargest(5, 'Cumplimiento')
elif vista == "Últimos 5":
    df_detail = df_detail.nsmallest(5, 'Cumplimiento')
else:
    df_detail = df_detail.sort_values('Cumplimiento', ascending=False)

# Crear tabla HTML personalizada con TODOS los datos
html_detail = '<div class="meta-tabla"><table><thead><tr><th style="width: 8%;">Pos</th><th style="width: 35%;">Empleado</th><th style="width: 12%;">Meta</th><th style="width: 12%;">Cumpl%</th><th style="width: 12%;">Efectiv%</th><th style="width: 21%;">Estado</th></tr></thead><tbody>'

for idx, (_, row) in enumerate(df_detail.iterrows(), 1):
    empleado = row['Empleado']
    meta = int(row['Meta'])
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
    
    html_detail += f'''<tr style="{fila_bg}">
        <td style="font-weight: 700; text-align: center; color: #0066cc;">#{idx}</td>
        <td style="font-weight: 600;">{empleado}</td>
        <td style="text-align: center; font-weight: 600;">{meta}</td>
        <td style="text-align: center;"><div class="meta-valor">{cumpl}%</div></td>
        <td style="text-align: center;"><div class="meta-valor" style="background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);">{efect}%</div></td>
        <td style="text-align: center;">{estado}</td>
    </tr>'''

html_detail += '</tbody></table></div>'
st.markdown(html_detail, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Footer elegante
st.markdown("""
<div class="footer-container">
    <p><strong>Dashboard WORLD TEL</strong> - Sistema de Control de Cumplimiento Mensual</p>
    <p>📅 Periodo: Noviembre 2025 | 🕐 Actualizado: {}  | 👥 Total Empleados: 14</p>
    <p style="margin-top: 15px; opacity: 0.7;">© 2025 WORLD TEL | Todos los derechos reservados</p>
</div>
""".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")), unsafe_allow_html=True)

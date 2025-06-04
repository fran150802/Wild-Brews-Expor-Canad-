import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la página
st.set_page_config(page_title="Wild Brews Dashboard", layout="wide")
st.title("🍹 Dashboard Interactivo - Wild Brews")

# Resumen Ejecutivo
with st.expander("📝 Resumen Ejecutivo", expanded=True):
    st.markdown("""
    **Wild Brews** es una empresa costarricense fundada por tres hermanas de Pérez Zeledón, que presentan una propuesta innovadora al ofrecer té de kombucha artesanal gasificado.  
    Su propuesta se distingue por la innovación en sabores, el uso de ingredientes naturales y una presentación atractiva que invita al consumidor a probar sus interesantes sabores y participar de los beneficios que los tés de la marca brindan.

    Ante las posibilidades de internacionalizarse a un nuevo mercado donde existe un nicho bien definido, como lo es el canadiense, se observa un entorno competitivo y dinámico.
    """)

# Paleta de colores
colores = px.colors.sequential.Tealgrn

# Cargar los datos desde el archivo Excel
file_path = "Excel de Wild Brews.xlsx"
sheets = {
    "Importaciones": "IM",
    "Valoración del Mercado": "Valoración del Mercado",
    "Volumen por Segmento": "Volumen por Segmento",
    "Competencia": "Competencia",
    "Fidelización": "Estrategias de Fidelización"
}
data = {name: pd.read_excel(file_path, sheet_name=sheet) for name, sheet in sheets.items()}

# Función para limpiar los datos
def limpiar_datos(df):
    df = df.copy()
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.dropna(how='all')
    for col in df.columns[1:]:
        df[col] = df[col].astype(str) \
                         .str.replace("$", "", regex=False) \
                         .str.replace(",", "", regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=[df.columns[0]])
    return df

# Función para aplicar estilo a los gráficos
def aplicar_estilo(fig, is_money=False):
    fig.update_layout(
        title_font=dict(size=20, family="Arial", color="darkslategray"),
        font=dict(size=14),
        plot_bgcolor="white",
        paper_bgcolor="white",
        colorway=colores
    )
    fig.update_xaxes(showgrid=True, gridcolor='lightgrey', zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor='lightgrey', zeroline=False)
    if is_money:
        fig.update_traces(hovertemplate='%{x}<br>%{y:$,.2f}')
    else:
        fig.update_traces(hovertemplate='%{x}<br>%{y}')
    return fig

# Función para generar gráficos
def generar_grafico(nombre, df):
    if df.empty or len(df.columns) < 2:
        return None

    x_col = df.columns[0]
    y_cols = df.select_dtypes(include='number').columns

    if nombre == "Importaciones":
        df = limpiar_datos(df)
        if len(y_cols) == 0:
            return None
        fig = px.line(df, x=x_col, y=y_cols[0],
                      title="📈 Importaciones por conceptos de bebidas (USD)",
                      markers=True)
        fig.update_yaxes(tickprefix="$", separatethousands=True)
        return aplicar_estilo(fig, is_money=True)

    elif nombre == "Valoración del Mercado":
        df = limpiar_datos(df)
        if len(y_cols) == 0:
            return None
        fig = px.line(df, x=x_col, y=y_cols[0],
                      title="📈 Valoración del mercado de kombucha (USD)",
                      markers=True)
        fig.update_yaxes(tickprefix="$", separatethousands=True)
        return aplicar_estilo(fig, is_money=True)

    elif nombre == "Volumen por Segmento":
        df_burb = df.copy()
        df_burb.columns = df_burb.columns.str.strip()
        df_burb = df_burb.dropna()

        def escala_a_tamano(valor):
            valor = str(valor).strip().lower()
            if "bajo" in valor:
                return 20
            elif "medio" in valor:
                return 60
            elif "alto" in valor:
                return 120
            return 40

        df_burb["Tamaño"] = df_burb.iloc[:, 1].apply(escala_a_tamano)

        fig = px.scatter(df_burb, x=df_burb.columns[0], y=["" for _ in range(len(df_burb))],
                         size="Tamaño", color=df_burb.columns[1],
                         title="Volumen proyectado de consumo por segmento",
                         labels={df_burb.columns[0]: "Segmento", df_burb.columns[1]: "Consumo"},
                         size_max=120)
        return aplicar_estilo(fig)

    elif nombre == "Competencia":
        df_filtrado = df[[col for col in df.columns if col.lower() in ['competidor', 'origen', 'precio'] or any(x in col.lower() for x in ['competidor', 'origen', 'precio'])]].dropna()
        df_filtrado.iloc[:, 2] = df_filtrado.iloc[:, 2].replace({"GT's Kombucha": "Medio"})

        def precio_a_valor(p):
            p = str(p).strip().lower()
            if "bajo" in p:
                return 20
            elif "medio" in p:
                return 60
            elif "alto" in p:
                return 120
            return 40

        df_filtrado["Tamaño"] = df_filtrado.iloc[:, 2].apply(precio_a_valor)
        fig = px.scatter(df_filtrado, x=df_filtrado.columns[0], y=df_filtrado.columns[1],
                         size="Tamaño", color=df_filtrado.iloc[:, 2],
                         title="Competencia: Relación Competidor - Origen - Precio",
                         size_max=120)
        return aplicar_estilo(fig)

    elif nombre == "Fidelización":
        df = limpiar_datos(df)
        if len(y_cols) == 0:
            return None
        fig = px.pie(df, names=x_col, values=y_cols[0],
                     title="🎯 Estrategias de fidelización")
        fig.update_traces(textposition='inside', textinfo='percent')
        fig.update_layout(title_x=0.5)
        return fig

    return None

# Crear pestañas para cada hoja
tabs = st.tabs(list(data.keys()))

# Mostrar gráficos y tablas en cada pestaña
for i, nombre in enumerate(data.keys()):
    with tabs[i]:
        st.subheader(f"📑 Datos: {nombre}")
        st.dataframe(data[nombre].head(20))
        figura = generar_grafico(nombre, data[nombre])
        if figura:
            st.plotly_chart(figura, use_container_width=True)

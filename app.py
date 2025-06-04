import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar los datos
file_path = "Excel de Wild Brews.xlsx"
sheets = {
    "Importaciones": "IM",
    "Valoración del Mercado": "Valoración del Mercado",
    "Volumen por Segmento": "Volumen por Segmento",
    "Competencia": "Competencia",
    "Fidelización": "Estrategias de Fidelización"
}
data = {name: pd.read_excel(file_path, sheet_name=sheet) for name, sheet in sheets.items()}

# Título del dashboard
st.set_page_config(page_title="Wild Brews Dashboard", layout="wide")
st.title("🍹 Dashboard Interactivo - Wild Brews")

# Función para limpiar y detectar columnas numéricas
def limpiar_datos(df):
    df = df.copy()
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.dropna(how='all')
    for col in df.columns[1:]:
        df[col] = (df[col].astype(str)
                         .str.replace("$", "", regex=False)
                         .str.replace(",", "", regex=False))
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=[df.columns[0]])
    return df

# Función para generar los gráficos
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
        fig.update_traces(mode="lines+markers", hovertemplate='%{y:$,.2f}')
        fig.update_yaxes(tickprefix="$", separatethousands=True)
        return fig

    elif nombre == "Valoración del Mercado":
        df = limpiar_datos(df)
        if len(y_cols) == 0:
            return None
        fig = px.line(df, x=x_col, y=y_cols[0],
                      title="📈 Valoración del mercado de kombucha (USD)",
                      markers=True)
        fig.update_traces(mode="lines+markers", hovertemplate='%{y:$,.2f}')
        fig.update_yaxes(tickprefix="$", separatethousands=True)
        return fig

    elif nombre == "Volumen por Segmento":
        st.markdown("### 📊 Volumen por Segmento (Gráfico de Burbujas)")
        df_burb = df.copy()
        df_burb.columns = df_burb.columns.str.strip()
        df_burb = df_burb.dropna()

        def escala_a_tamano(valor):
            valor = str(valor).strip().lower()
            if "bajo" in valor:
                return 10
            elif "medio" in valor:
                return 30
            elif "alto" in valor:
                return 60
            return 20

        df_burb["Tamaño"] = df_burb.iloc[:, 1].apply(escala_a_tamano)

        fig = px.scatter(df_burb, x=df_burb.columns[0], y=["" for _ in range(len(df_burb))],
                         size="Tamaño", color=df_burb.columns[1],
                         title="Volumen proyectado de consumo por segmento",
                         labels={df_burb.columns[0]: "Segmento", df_burb.columns[1]: "Consumo"},
                         size_max=60)
        return fig

    elif nombre == "Competencia":
        st.markdown("### 🧩 Visualización de Competencia (Gráfico de Burbujas)")
        df_filtrado = df[[col for col in df.columns if col.lower() in ['competidor', 'origen', 'precio'] or any(x in col.lower() for x in ['competidor', 'origen', 'precio'])]].dropna()

        # Asegurar que GT's Kombucha esté clasificado como Medio
        df_filtrado.iloc[:, 2] = df_filtrado.iloc[:, 2].replace({"GT's Kombucha": "Medio"})

        def precio_a_valor(p):
            p = str(p).strip().lower()
            if "bajo" in p:
                return 10
            elif "medio" in p:
                return 30
            elif "alto" in p:
                return 60
            return 20

        df_filtrado["Tamaño"] = df_filtrado.iloc[:, 2].apply(precio_a_valor)
        fig = px.scatter(df_filtrado, x=df_filtrado.columns[0], y=df_filtrado.columns[1],
                         size="Tamaño", color=df_filtrado.iloc[:, 2],
                         title="Competencia: Relación Competidor - Origen - Precio",
                         size_max=60)
        return fig

    elif nombre == "Fidelización":
        df = limpiar_datos(df)
        if len(y_cols) == 0:
            return None
        fig = px.pie(df, names=x_col, values=y_cols[0],
                     title="🎯 Estrategias de fidelización")
        return fig

    return None

# Mostrar todo el contenido en una sola página con interactividad
with st.expander("Mostrar todos los análisis", expanded=True):
    for nombre, df in data.items():
        st.subheader(f"📑 Datos: {nombre}")
        st.dataframe(df.head(20))
        figura = generar_grafico(nombre, df)
        if figura:
            st.plotly_chart(figura, use_container_width=True)
        st.markdown("---")

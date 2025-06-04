import streamlit as st
import pandas as pd
import plotly.express as px

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
st.title("Dashboard Interactivo - Wild Brews")

# Función para limpiar y detectar columnas numéricas

def limpiar_datos(df):
    df = df.copy()
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.dropna(how='all')
    for col in df.columns[1:]:
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
        fig = px.scatter(df, x=x_col, y=y_cols[0],
                         title="Importaciones por conceptos de bebidas (USD)")
    elif nombre == "Valoración del Mercado":
        df = limpiar_datos(df)
        if len(y_cols) == 0:
            return None
        fig = px.scatter(df, x=x_col, y=y_cols[0],
                         title="Valoración del mercado de kombucha (USD)")
    elif nombre == "Volumen por Segmento":
        # Usar un gráfico de barras con conteo por categoría
        fig = px.bar(df, x=x_col, color=df.columns[1],
                     title="Volumen proyectado de consumo por segmento (conteo de categorías)")
    elif nombre == "Competencia":
        # Usar gráfico de barras para mostrar recuento por competidor
        fig = px.bar(df, x=x_col, color=x_col,
                     title="Participación de competidores (frecuencia de mención)")
    elif nombre == "Fidelización":
        df = limpiar_datos(df)
        if len(y_cols) == 0:
            return None
        fig = px.pie(df, names=x_col, values=y_cols[0],
                     title="Estrategias de fidelización")
    else:
        return None

    return fig

# Mostrar todo el contenido en una sola página
for nombre, df in data.items():
    st.subheader(f"Datos: {nombre}")
    st.dataframe(df.head(20))
    figura = generar_grafico(nombre, df)
    if figura:
        st.plotly_chart(figura, use_container_width=True)
    else:
        st.info("No hay datos suficientes o válidos para graficar.")
    st.markdown("---")


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

# Función para generar los gráficos

def generar_grafico(nombre, df):
    df = df.copy()
    if df.empty or len(df.columns) < 2:
        return None

    x_col = df.columns[0]
    y_cols = df.columns[1:]

    # Convertir columnas numéricas y filtrar valores válidos
    for col in y_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=[x_col] + list(y_cols))

    if df.empty:
        return None

    if nombre == "Importaciones":
        fig = px.scatter_matrix(df, dimensions=y_cols, color=x_col,
                                title="Importaciones por conceptos de bebidas")
    elif nombre == "Valoración del Mercado":
        fig = px.scatter(df, x=x_col, y=y_cols[0],
                         title="Valoración del mercado de kombucha")
    elif nombre == "Volumen por Segmento":
        fig = px.bar(df, x=x_col, y=y_cols,
                     barmode="group", title="Volumen proyectado de consumo por segmento")
    elif nombre == "Competencia":
        fig = px.treemap(df, path=[x_col], values=y_cols[0],
                         title="Participación de competidores")
    elif nombre == "Fidelización":
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

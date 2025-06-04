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
    if nombre == "Importaciones" and len(df.columns) > 1:
        return px.bar(df, x=df.columns[0], y=df.columns[1:], barmode="group",
                      title="Importaciones por conceptos de bebidas")
    elif nombre == "Valoración del Mercado" and len(df.columns) > 1:
        return px.line(df, x=df.columns[0], y=df.columns[1:],
                       title="Valoración del mercado de kombucha")
    elif nombre == "Volumen por Segmento" and len(df.columns) > 1:
        return px.area(df, x=df.columns[0], y=df.columns[1:],
                       title="Volumen proyectado de consumo por segmento")
    elif nombre == "Competencia" and len(df.columns) >= 2:
        return px.bar(df, x=df.columns[0], y=df.columns[1],
                      title="Análisis de competidores")
    elif nombre == "Fidelización" and len(df.columns) >= 2:
        return px.pie(df, names=df.columns[0], values=df.columns[1],
                      title="Estrategias de fidelización")
    else:
        return None

# Mostrar todo el contenido en una sola página
for nombre, df in data.items():
    st.subheader(f"Datos: {nombre}")
    st.dataframe(df.head(20))
    figura = generar_grafico(nombre, df)
    if figura:
        st.plotly_chart(figura)
    else:
        st.info("No hay datos suficientes para graficar.")
    st.markdown("---")

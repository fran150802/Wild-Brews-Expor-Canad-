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
    df = df.dropna()  # eliminar filas con valores nulos
    if df.empty or len(df.columns) < 2:
        return None

    x_col = df.columns[0]
    y_cols = df.columns[1:]

    # Intentar convertir todas las columnas Y a numérico (ignorando errores)
    for col in y_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna()  # eliminar filas con datos no convertibles

    if nombre == "Importaciones":
        return px.scatter(df, x=x_col, y=df.select_dtypes(include='number').columns,
                          title="Importaciones por conceptos de bebidas")
    elif nombre == "Valoración del Mercado":
        return px.scatter(df, x=x_col, y=df.select_dtypes(include='number').columns,
                          title="Valoración del mercado de kombucha")
    elif nombre == "Volumen por Segmento":
        return px.bar(df, x=x_col, y=df.select_dtypes(include='number').columns,
                      barmode="group", title="Volumen proyectado de consumo por segmento")
    elif nombre == "Competencia" and df.dtypes[1] in ['int64', 'float64']:
        return px.funnel(df, x=df.columns[1], y=x_col,
                         title="Embudo de participación de competidores")
    elif nombre == "Fidelización" and df.dtypes[1] in ['int64', 'float64']:
        return px.pie(df, names=x_col, values=df.columns[1],
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

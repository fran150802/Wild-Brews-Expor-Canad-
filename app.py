import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración inicial
st.set_page_config(page_title="Wild Brews Dashboard", layout="wide")
st.title("🍹 Dashboard Interactivo - Wild Brews")

# Colores personalizados
colores = px.colors.sequential.Tealgrn

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

# Limpieza de datos
def limpiar_datos(df):
    df = df.copy()
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.dropna(how='all')
    for col in df.columns[1:]:
        df[col] = (df[col].astype(str)

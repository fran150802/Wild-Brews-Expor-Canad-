import dash
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd

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

# Inicializar la app
app = dash.Dash(__name__)
app.title = "Dashboard de Wild Brews"

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

app.layout = html.Div([
    html.H1("Dashboard Interactivo - Wild Brews", style={"textAlign": "center"}),
    
    dcc.Tabs([
        dcc.Tab(label=nombre, children=[
            html.Div([
                html.H2(nombre),
                dash_table.DataTable(
                    data=df.head(20).to_dict("records"),
                    columns=[{"name": i, "id": i} for i in df.columns],
                    page_size=10,
                    style_table={'overflowX': 'auto'},
                    style_cell={"textAlign": "left", "padding": "5px"},
                    style_header={"fontWeight": "bold"}
                ),
                html.Br(),
                dcc.Graph(figure=generar_grafico(nombre, df))
                if generar_grafico(nombre, df) else html.P("No hay datos suficientes para graficar")
            ])
        ]) for nombre, df in data.items()
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)

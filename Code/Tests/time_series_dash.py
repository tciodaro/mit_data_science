# Plot imports
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd



# FILE CONFIGURATION
WORKDIR = 'C:/Users/BZ241WX/Documents/InfNet/CursoPosDataScience/mit_data_science/'
forecast_file = WORKDIR + '/Data/Modeling/forecast_results.parquet'

# LOAD FILE
data = pd.read_parquet(forecast_file)


app = dash.Dash(__name__)


df_history = data.groupby('Date').Weekly_Sales.sum()
df_forecast = data.groupby('Date').forecast.sum()

app.layout = html.Div(children=[
    html.H1(children='Dashboard de Previsão de Vendas'),

    html.Div(children='''
        Desenvolvimento de modelos de previsão de vendas de uma grande rede de lojas de departamentos.
    '''),
    
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [{'x': df_history.index, 'y': df_history.values, 'name': 'Histórico'},
                     {'x': df_forecast.index, 'y': df_forecast.values, 'name': 'Previsão'}],
            
            'layout':{
                'title': 'Série Temporal de Vendas Semanais',
            }
        }
    )
    
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)

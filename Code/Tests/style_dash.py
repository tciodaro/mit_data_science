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
df_history = data.groupby('Date').Weekly_Sales.sum()
df_forecast = data.groupby('Date').forecast.sum()

# STYLE
default_colors = {
    'text': '#000000',
    'bg_plot': '#1122ff',
    'bg_paper': '#9999ff',
    'font_size': '20',
    'font_family': 'arial'
}

# CREATE APP
app = dash.Dash(__name__)

# CREATE LAYOUT
app.layout = html.Div(children=[
    # Main Header
    html.H1(children='Dashboard de Previsão de Vendas',
            style = {
                'textAlign': 'center',
                'color': default_colors['text'],
            }
    ),
    # Subtitle
    html.H2(children='''Desenvolvimento de modelos de previsão de vendas de uma
                         grande rede de lojas de departamentos.
                      ''',
            style = {
                'textAlign': 'center',
                'color': default_colors['text'],
#                 'background': default_colors['bg_paper']
            }
    ),
    
    # GRAPH
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [{'x': df_history.index, 'y': df_history.values, 'name': 'Histórico'},
                     {'x': df_forecast.index, 'y': df_forecast.values, 'name': 'Previsão'}],
            
            'layout':{
                'title': 'Série Temporal de Vendas Semanais',
                'plot_bgcolor': default_colors['bg_plot'],
                'paper_bgcolor': default_colors['bg_paper'],
                'font': {
                    'color': default_colors['text'],
                    'family': default_colors['font_family'],
                    'size': default_colors['font_size'],
                }
            }
        }
    )
    
])


# RUN SERVER
if __name__ == '__main__':
    app.run_server(debug=True, port=8000)

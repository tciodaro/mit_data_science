# Plot imports
import plotly.graph_objs as go

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd



# FILE CONFIGURATION
WORKDIR = 'C:/Users/BZ241WX/Documents/InfNet/CursoPosDataScience/mit_data_science/'
forecast_file = WORKDIR + '/Data/Modeling/forecast_results.parquet'

# LOAD FILE
data = pd.read_parquet(forecast_file)


app = dash.Dash(__name__)


app.layout = html.Div(children=[
    html.H1(children='Dashboard de Previsão de Vendas'),

    html.P(children='''
        Desenvolvimento de modelos de previsão de vendas de uma grande rede de lojas de departamentos.
    '''),
    
    html.Div([
        html.Label('Filtros'),
        html.Br(),
        dcc.Dropdown(
            id='store_selection',
            options = [{'label': val, 'value': val} for val in data.Store.sort_values().unique()],
            value=data.Store.sort_values().unique()[0],
            multi=True,
            placeholder='Escolha uma loja',
#             disabled=True,
        ),
        html.Br(),
        
        dcc.DatePickerRange(
            id='date_range',
            min_date_allowed = data.Date.min(),
            max_date_allowed = data.Date.max(),
        ),
    ]),
    
    html.Div(id='selected_store')
    
])

@app.callback(
    Output(component_id='selected_store', component_property='children'),
    [Input(component_id='store_selection', component_property='value')]
)
def update_selected_store(input_value):
    return 'Selected Store: {}'.format(input_value)



if __name__ == '__main__':
    app.run_server(debug=True, port=8000)

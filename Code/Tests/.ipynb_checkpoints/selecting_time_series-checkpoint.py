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
        html.Label('Lojas'),
        dcc.Dropdown(
            id='store_selection',
            options = [{'label': val, 'value': val} for val in data.Store.sort_values().unique()],
            value=data.Store.sort_values().unique()[0],
            multi=True,
            placeholder='Escolha uma loja',
#             disabled=True,
        ),
        dcc.Dropdown(
            id='dept_selection',
            options = [{'label': val, 'value': val} for val in data.Dept.sort_values().unique()],
            value=data.Dept.sort_values().unique()[0],
            multi=True,
            placeholder='Escolha um departamento',
#             disabled=True,
        ),
        html.Br(),
        dcc.Graph(id='time_series')
    ]),
    
    html.Div(id='selected_store'),
    html.Div(id='selected_dept'),
    
])

@app.callback(
    Output(component_id='time_series', component_property='figure'),
    [Input(component_id='store_selection', component_property='value'),
     Input(component_id='dept_selection', component_property='value')]
)
def update_time_series(selected_stores, selected_depts):
    if isinstance(selected_stores, str):
        selected_stores = [selected_stores]
    if isinstance(selected_depts, str):
        selected_depts = [selected_depts]
    
    filtered_df = (data[data.Store.isin(selected_stores) & data.Dept.isin(selected_depts)]
                   .groupby('Date')[['Weekly_Sales','forecast']]
                   .sum())

    
    return {
                'data': [{'x': filtered_df.index, 'y': filtered_df.Weekly_Sales.values, 'name': 'Histórico'},
                         {'x': filtered_df.index, 'y': filtered_df.forecast.values, 'name': 'Previsão'}],

                'layout':{
                    'title': 'Série Temporal de Vendas Semanais',
                }
            }
    
    
#     fig = px.line(filtered_df, x='Date', y='AAPL.High')
    
#     fig = px.scatter(filtered_df, x="Date", y="lifeExp", 
#                      size="pop", color="continent", hover_name="country", 
#                      log_x=True, size_max=55)

#     fig.update_layout(transition_duration=500)

    
#     return 



if __name__ == '__main__':
    app.run_server(debug=True, port=8000)

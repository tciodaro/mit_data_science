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


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def make_scatter(x, y, xtitle, ytitle):
    # GRAPH
    return  {
        'data': [
            go.Scatter(
                x = x,
                y = y,
                mode='markers'
            )
        ],
        'layout': go.Layout(
            xaxis = {'title': xtitle},
            yaxis = {'title': ytitle},
            hovermode='closest'
        )
    }




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
        html.Br(),
        # New Div for both plots
        html.Div([
            html.Div([
                html.H3('Gráfico de Resíduos'),
                dcc.Graph(id='plot_residuos')
            ], className="six columns"),

            html.Div([
                html.H3('Dispersão dos Resultados'),
                dcc.Graph(id='plot_dispersao')
            ], className="six columns"),
        ], className="row")    
    ]),
    
    html.Div(id='selected_store')
    
])

@app.callback(
    [Output(component_id='plot_residuos', component_property='figure'),
     Output(component_id='plot_dispersao', component_property='figure'),],
    
    [Input(component_id='store_selection', component_property='value')]
)
def update_plots(selected_stores):
    if isinstance(selected_stores, str):
        selected_stores = [selected_stores]
    
    df = (data[data.Store.isin(selected_stores)]
          .dropna()
          .groupby('Date')[['Weekly_Sales','forecast']]
          .sum())
    
    
    return [make_scatter(df.Weekly_Sales,
                         df.Weekly_Sales - df.forecast,
                         'Vendas',
                         'Erro: Venda - Estimativa'),
            make_scatter(df.Weekly_Sales,
                         df.forecast,
                         'Vendas',
                         'Previsão')] 


if __name__ == '__main__':
    app.run_server(debug=True, port=8000)

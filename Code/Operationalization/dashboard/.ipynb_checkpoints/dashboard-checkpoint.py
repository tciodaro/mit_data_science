import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output


import pandas as pd
import pathlib


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table


# FILE CONFIGURATION
WORKDIR = 'C:/Users/BZ241WX/Documents/InfNet/CursoPosDataScience/mit_data_science/'
forecast_file = WORKDIR + '/Data/Modeling/forecast_results.parquet'

# LOAD FILE
data = pd.read_parquet(forecast_file)
data['Year'] = data.Date.dt.year
data['Month'] = data.Date.dt.month
year_data = data.groupby('Year', as_index=False)[['Weekly_Sales','forecast']].sum()
month_data = data.groupby('Month', as_index=False)[['Weekly_Sales','forecast']].sum()



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=external_stylesheets
)

# LAYOUT
app.layout=html.Div([
               html.Div([html.H1('Relatório de Previsão de Demanda')]),
                   html.Div([
                        # Row 3
                        html.Div([
                            html.Div([
                                    html.H5("Sumário do Produto"),
                                    html.Br([]),
                                    html.P('''
                                           Conforme o mercado de varejo retrai, a competitividade no setor aumenta, levando empresas
                                           do setor a investir na otimização de seus processos. A disponibilidade e confiabilidade dos
                                           dados coletados pela empresa permite o desenvolvimento de modelos estatísticos capazes de
                                           prever a demanda futura pelos produtos, através da modelagem do comportamento da série
                                           histórica.
                                           ''',
                                        style={"color": "#ffffff"},
                                        className="row",
                                    ),
                            ], className="product",)
                        ], className="row",),
                    # Row 4
                    html.Div([
                            html.Div([
                                    html.H6(
                                        ["Volume Anual"], className="subtitle padded"
                                    ),
                                    html.Table(make_dash_table(year_data)),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Volume Mensal de Vendas e Previsão",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="monthly_data",
                                        figure={
                                            "data": [
                                                go.Bar(
                                                    x = month_data.index,
                                                    y = month_data.Weekly_Sales,
                                                    marker={
                                                        "color": "#97151c",
                                                        "line": {
                                                            "color": "rgb(255, 255, 255)",
                                                            "width": 2,
                                                        },
                                                    },
                                                    name="Historico Mensal de Vendas",
                                                ),
                                                go.Bar(
                                                    x=month_data.index,
                                                    y=month_data.forecast,
                                                    marker={
                                                        "color": "#dddddd",
                                                        "line": {
                                                            "color": "rgb(255, 255, 255)",
                                                            "width": 2,
                                                        },
                                                    },
                                                    name="Previsão Mensal de Vendas",
                                                ),
                                            ],
                                            "layout": go.Layout(
                                                autosize=False,
                                                bargap=0.35,
                                                font={"family": "Raleway", "size": 10},
                                                height=200,
                                                hovermode="closest",
                                                legend={
                                                    "x": -0.0228945952895,
                                                    "y": -0.189563896463,
                                                    "orientation": "h",
                                                    "yanchor": "top",
                                                },
                                                margin={
                                                    "r": 0,
                                                    "t": 20,
                                                    "b": 10,
                                                    "l": 10,
                                                },
                                                showlegend=True,
                                                title="",
                                                width=330,
                                                xaxis={
                                                    "autorange": True,
                                                    "range": [-0.5, 4.5],
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "category",
                                                },
                                                yaxis={
                                                    "autorange": True,
                                                    "range": [0, 22.9789473684],
                                                    "showgrid": True,
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "linear",
                                                    "zeroline": False,
                                                },
                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),
                    # Row 5
                    html.Div([
                            html.Div([
                                    html.H6(
                                        ["Filtros"], className="subtitle padded"
                                    ),
                                    dcc.Dropdown(
                                        id='store_selection',
                                        options = [{'label': val, 'value': val} for val in data.Store.sort_values().unique()],
                                        value=data.Store.sort_values().unique()[0],
                                        multi=True,
                                        placeholder='Escolha uma loja',
                                    )
                                
                                ],
                                className="six columns",
                            ),
                            html.Div([
                                    html.H6(
                                        ["Série Temporal de Vendas"], className="subtitle padded"
                                    ),
                                    dcc.Graph(id='plot_time_series')
                                ],
                                className="six columns",
                            ),
                    
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
])
    
    


@app.callback(
    Output(component_id='plot_time_series', component_property='figure'),
    [Input(component_id='store_selection', component_property='value')]
)
def update_time_series(selected_stores):
    if isinstance(selected_stores, str):
        selected_stores = [selected_stores]
    
    filtered_df = (data[data.Store.isin(selected_stores)]
                   .groupby('Date')[['Weekly_Sales','forecast']]
                   .sum())

    
    return {
                'data': [{'x': filtered_df.index, 'y': filtered_df.Weekly_Sales.values, 'name': 'Histórico'},
                         {'x': filtered_df.index, 'y': filtered_df.forecast.values, 'name': 'Previsão'}],
            }
    
    

if __name__ == "__main__":
    app.run_server(debug=True, port=8000)    
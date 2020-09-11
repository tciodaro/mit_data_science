import json
import logging
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly.express as px
import pandas.io.json as pd_json

from django_plotly_dash import DjangoDash
from django.core.serializers import serialize

import plotly.figure_factory as ff
from forecast.models import *
from forecast.serializers import *
from rest_framework.response import Response




import numpy as np

import pandas as pd
import pathlib


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    html_row = []
    html_row.append(html.Td(["Ano"]))
    html_row.append(html.Td(["Dados Históricos"]))
    html_row.append(html.Td(["Previsão"]))
    html_row.append(html.Td(["Erro(MW)"]))
    html_row.append(html.Td(["Erro(%)"]))
    table.append((html.Tr(html_row)))


    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table


# FILE CONFIGURATION
WORKDIR = 'C:/Users/thewr/git/mit_data_science.git/'
forecast_file = WORKDIR + '/Data/Modeling/forecasting_versus_actuals.parquet'

from django.core import serializers

forecast_model_active = ForecastModels.objects.get(status=True)

serializedData = serializers.serialize("json", Forecasts.objects.filter(forecast_model = forecast_model_active),use_natural_foreign_keys=True, use_natural_primary_keys=True)
serializedData_forecasts_all = serializers.serialize("json",Forecasts.objects.all())


json_loads = json.loads(serializedData)
forecast_data= pd.json_normalize(json_loads)
print(forecast_data.head()) 
print(forecast_data.tail())


json_loads_forecasts_all = json.loads(serializedData_forecasts_all)
forecast_data_all= pd.json_normalize(json_loads_forecasts_all)


forecast_data['fields.date'] = forecast_data['fields.date'].astype('datetime64[ns]')
forecast_data_all['fields.date'] = forecast_data_all['fields.date'].astype('datetime64[ns]')

pd_teste = forecast_data['fields.measurement'].apply(pd.Series)
#pd_teste_forecast_data_all = forecast_data_all['fields.measurement'].apply(pd.Series)

logging.info("imprimindo info e head de pd_teste ")
pd_teste.columns =['data_medicao','medicao_mw']
#pd_teste_forecast_data_all.columns =['data_medicao','medicao_mw']

pd_teste['data_medicao'] = pd_teste['data_medicao'].astype('datetime64[ns]')
#pd_teste_forecast_data_all['data_medicao'] = pd_teste_forecast_data_all ['data_medicao'].astype('datetime64[ns]')

print(pd_teste.info())
print(pd_teste.head)


logging.info("imprimindo info e head de pd_teste ")




forecast_data = pd.merge(forecast_data, pd_teste, how='inner', \
        left_on='fields.date', right_on='data_medicao')

#forecast_data_all = pd.merge(forecast_data_all, pd_teste_forecast_data_all, how='inner', \
#        left_on='fields.date', right_on='data_medicao')

print(forecast_data.info())
print(forecast_data.head())
print(forecast_data.tail())

forecast_data['Year'] = forecast_data['fields.date'].dt.year
forecast_data['Month'] = forecast_data['fields.date'].dt.month
forecast_data['Day'] = forecast_data['fields.date'].dt.day

forecast_data_all['Day'] = forecast_data_all['fields.date'].dt.day
forecast_data_all['Month'] = forecast_data_all['fields.date'].dt.month
forecast_data_all['data_sem_hora'] = pd.to_datetime(forecast_data_all['fields.date']).dt.normalize()


function_dict = {"medicao_mw": "sum", "fields.PJME_MW": "sum", "fields.error": "sum", "fields.percentage_error": "mean"}

function_dict_forecast_data_all = {"fields.PJME_MW": "sum", "fields.error": "sum", "fields.percentage_error": "mean"}

year_data = forecast_data.groupby('Year', as_index=False)
month_data = forecast_data.groupby('Month', as_index=False)
day_data = forecast_data.groupby('Day', as_index=False)

year_data = year_data.aggregate(function_dict).round(decimals=2)
month_data = month_data.aggregate(function_dict).round(decimals=2)
day_data = day_data.aggregate(function_dict).round(decimals=2)


day_data_all = forecast_data_all.groupby('data_sem_hora', as_index=False)
day_data_all = day_data_all.aggregate(function_dict_forecast_data_all).round(decimals=2)
day_data_all = day_data_all.drop(['fields.PJME_MW','fields.error'],axis=1)
day_data_all.sort_values(by='data_sem_hora',inplace=True)
print(day_data_all.info())
print(day_data_all)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash(
    "ForecastDashboard",
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=external_stylesheets
)

def update_dash():

    n=1000
    plot = go.Figure(data=[go.Scatter(
        x=pd.Series(forecast_data_all["fields.date"]), y=pd.Series(forecast_data_all["fields.percentage_error"]), 
        mode = 'markers', 
        marker=dict( 
        color=np.random.randn(n), 
        colorscale='Viridis',  
        showscale=True
        ) 
        ) 
        ]) 
# LAYOUT
    app.layout = html.Div([
        html.Div([html.H1('Relatório de Previsão de Demanda de Energia')]),
        html.Div([
            # Row 3
            html.Div([
                html.Div([
                    html.H5("Sumário do consumo"),
                    html.Br([]),
                    html.P('''
                                               A disponibilidade e confiabilidade dos dados coletados pela empresa permite o 
                                               desenvolvimento de modelos estatísticos capazes de prever a demanda futura de energia, 
                                               através da modelagem do comportamento da série histórica.
                                               ''',                           
                           className="row",
                           ),
                ], className="product", )
            ], className="row", ),
            # Row 4
            html.Div([
                html.Div([
                    html.H6(
                        ["Volume Anual"], className="subtitle padded"
                    ),
                    html.Table(make_dash_table(day_data)),
                ],
                    className="six columns",
                ),

            ],
                className="row",
                style={"margin-bottom": "35px"},
            )
            
        ],
            className="page",
        ),

        html.Div([
            dcc.Graph(id='historico_previsao'),

            dcc.Slider(
                id='ndays-plot',
                min=1,
                max=240,
                value=240,
                marks={
                    1: {'label': '1 H', 'style': {'color': '#17BECF'}},
                    24: {'label': '1D ', 'style': {'color': '#17BECF'}},
                    120: {'label': '5 D', 'style': {'color': '#17BECF'}},
                    240: {'label': '10 D ', 'style': {'color': '#17BECF'}}                   
                }
            ),
            html.Br(),
            html.Div([
                html.Div([
                    dcc.Graph(id='grafico_erros')
                ], style={'height': 200}),                
            ], className="row"),
            html.Br(),
            """ html.Div([
                html.Div([
                    dcc.Graph(id='grafico_erros_por_dia')
                ], style={'height': 200}),                
            ], className="row"),     """       

        ]),
    ])


@app.callback(
    Output('historico_previsao', 'figure'),    [ 
        Input('ndays-plot', 'value')]
)
def update_graph_raw(ndays_plot):    
    ydata = forecast_data['medicao_mw']
    xdata = forecast_data['data_medicao']
    xdata_forecast = forecast_data['fields.date']
    ydata_forecast = forecast_data['fields.PJME_MW']

    measure_forecast = []
    measure_forecast.append(go.Scatter(
        x=xdata[0:ndays_plot],
        y=ydata[0:ndays_plot],
        text=' ',
        mode='lines+markers',
        legendgroup='Histórico de consumo',
        showlegend=True,
        name='Histórico de consumo',
        marker={
            "size": 15,
            "opacity": 0.5,
            'color': '#17BECF',
            "line": {"width": 0.5, "color": "white"}
        }
        ,

    )),
    measure_forecast.append(go.Scatter(
        x=xdata_forecast[0:ndays_plot],
        y=ydata_forecast[0:ndays_plot],
        text=' ',
        mode='lines+markers',
        legendgroup='Previsão',
        showlegend=True,
        name='Previsão',
        marker={
            "size": 15,
            "opacity": 0.5,
            'color': '#ad1005',
            "line": {"width": 0.5, "color": "white"}
        }),

    )

    my_layout = go.Layout(
            xaxis={'title': ' '},
            yaxis={'title': 'Consumo (MW)'},
            margin={'l': 60, 'r': 40, 't': 40, 'b': 50},
            hovermode='closest',            
            title='Dados Históricos X Previsão'
        )

    fig = {'data':  measure_forecast, 'layout':my_layout}

    return fig


@app.callback(
    Output('grafico_erros', 'figure'),
    [  Input('ndays-plot', 'value')]
)

def update_graph_forecast(ndays_plot): 
    xdata_forecast_all = forecast_data_all['fields.date']
    ydata_forecast_all = forecast_data_all['fields.percentage_error']
    xdata_forecast_all_grouped_by_day = day_data_all['data_sem_hora']
    ydata_forecast_all_grouped_by_day = day_data_all['fields.percentage_error'] 

    measure_forecast_all = []
    measure_forecast_all.append(go.Scatter(
        x=xdata_forecast_all,
        y=ydata_forecast_all,
        text=' ',
        mode='lines+markers',
        legendgroup='Erro por hora',
        showlegend=True,
        name='Erro por hora',
        marker={
            "size": 15,
            "opacity": 0.5,
            'color': '#17BECF',
            "line": {"width": 0.5, "color": "white"}
        }
        ,

    )),

    measure_forecast_all.append(go.Scatter(
        x=xdata_forecast_all_grouped_by_day ,
        y=ydata_forecast_all_grouped_by_day,
        text=' ',
        mode='lines+markers',
        legendgroup='Erro por dia',
        showlegend=True,
        name='Erro por dia',
        marker={
            "size": 15,
            "opacity": 0.5,
            'color': '#ad1005',
            "line": {"width": 0.5, "color": "white"}
        }
        ,

    )),    

    my_layout = go.Layout(
            xaxis={'title': ' '},
            yaxis={'title': 'Erro (%)'},
            margin={'l': 60, 'r': 40, 't': 40, 'b': 50},
            hovermode='closest',            
            title='Histórico de erro percentual'
        )

    fig = {'data':  measure_forecast_all, 'layout':my_layout}

    return fig
""" 
@app.callback(
    Output('grafico_erros_por_dia', 'figure'),
    [  Input('ndays-plot', 'value')]
)

def update_graph_forecast(ndays_plot): 
    xdata_forecast_all = forecast_data_all['fields.date']
    ydata_forecast_all = forecast_data_all['fields.percentage_error']
    xdata_forecast_all_grouped_by_day = day_data_all['data_sem_hora']
    ydata_forecast_all_grouped_by_day = day_data_all['fields.percentage_error']   

    measure_forecast_all = []
    
    measure_forecast_all.append(go.Scatter(
        x=xdata_forecast_all_grouped_by_day,
        y=ydata_forecast_all_grouped_by_day,
        text=' ',
        mode='lines+markers',
        legendgroup='Erro por dia',
        showlegend=True,
        name='Erro por dia',
        marker={
            "size": 15,
            "opacity": 0.5,
            'color': '#17BECF',
            "line": {"width": 0.5, "color": "white"}
        }
        ,

    )),    

    my_layout = go.Layout(
            xaxis={'title': ' '},
            yaxis={'title': 'Erro (%)'},
            margin={'l': 60, 'r': 40, 't': 40, 'b': 50},
            hovermode='closest',            
            title='Histórico de erro percentual'
        )

    fig = {'data':  measure_forecast_all, 'layout':my_layout}

    return fig """


    

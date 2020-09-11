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
from   forecast.models import *
from forecast.serializers import *
from rest_framework.response import Response

import numpy as np
import pandas as pd
import pathlib


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    html_row = []
    html_row.append(html.Td(["Dia"],style = {"border": "1px solid black"}))
    html_row.append(html.Td(["Dados Históricos"],style = {"border": "1px solid black"}))
    html_row.append(html.Td(["Previsão"],style = {"border": "1px solid black"}))
    html_row.append(html.Td(["Erro(MW)"],style = {"border": "1px solid black"}))
    html_row.append(html.Td(["Erro(%)"],style = {"border": "1px solid black"}))
    table.append((html.Tr(html_row, style = {"border": "1px solid black"})))


    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]],style = {"border": "1px solid black"}))
        table.append(html.Tr(html_row))
    return table


# FILE CONFIGURATION
WORKDIR = 'C:/Users/thewr/git/mit_data_science.git/'
forecast_file = WORKDIR + '/Data/Modeling/forecasting_versus_actuals.parquet'

from django.core import serializers

forecast_model_active = ForecastModels.objects.get(status=True)
train_initial_date = forecast_model_active.train_initial_date
train_last_date =forecast_model_active.train_last_date

measurements = Measurements.objects.filter(date__range=[train_initial_date,train_last_date]).values_list('date','PJME_MW')


medicao_historica_periodo_treinamento = pd.DataFrame.from_records(measurements)

medicao_historica_periodo_treinamento.columns = ['data_medicao','PJME_MW']
 
serializedData = serializers.serialize("json", Forecasts.objects.filter(forecast_model = forecast_model_active),use_natural_foreign_keys=True, use_natural_primary_keys=True)
serializedData_forecasts_all = serializers.serialize("json",Forecasts.objects.all())

json_loads = json.loads(serializedData)
measurements_forecast_data= pd.json_normalize(json_loads)


json_loads_forecasts_all = json.loads(serializedData_forecasts_all)
measurements_forecast_data_all= pd.json_normalize(json_loads_forecasts_all)


measurements_forecast_data['fields.date'] = measurements_forecast_data['fields.date'].astype('datetime64[ns]')
measurements_forecast_data_all['fields.date'] = measurements_forecast_data_all['fields.date'].astype('datetime64[ns]')

data_split = measurements_forecast_data['fields.measurement'].apply(pd.Series)

data_split.columns =['historic_measurement_date','historic_measurement']


data_split['historic_measurement_date'] = data_split['historic_measurement_date'].astype('datetime64[ns]')

measurements_forecast_data = pd.merge(measurements_forecast_data, data_split, how='inner', \
        left_on='fields.date', right_on='historic_measurement_date')

measurements_forecast_data.drop('fields.measurement',axis=1,inplace=True)
measurements_forecast_data.columns = ['model','pk','measurement_prediction','prediction_date', \
    'prediction_error','prediction_percentage_error','forecast_model','historic_measurement_date', \
        'historic_measurement']

measurements_forecast_data_all.drop('fields.measurement',axis=1,inplace=True)
measurements_forecast_data_all.columns = ['model','pk','measurement_prediction','prediction_date', \
    'prediction_error','prediction_percentage_error','forecast_model']

measurements_forecast_data['Year'] = measurements_forecast_data['prediction_date'].dt.year
measurements_forecast_data['Month'] = measurements_forecast_data['prediction_date'].dt.month
measurements_forecast_data['Day'] = measurements_forecast_data['prediction_date'].dt.day

measurements_forecast_data_all['Day'] = measurements_forecast_data_all['prediction_date'].dt.day
measurements_forecast_data_all['Month'] = measurements_forecast_data_all['prediction_date'].dt.month
measurements_forecast_data_all['no_hour_date'] = pd.to_datetime(measurements_forecast_data_all['prediction_date']).dt.normalize()


function_dict = {"historic_measurement": "sum", "measurement_prediction": "sum", "prediction_error": "sum", "prediction_percentage_error": "mean"}

function_dict_measurements_forecast_data_all = {"measurement_prediction": "sum", "prediction_error": "sum", "prediction_percentage_error": "mean"}

year_data = measurements_forecast_data.groupby('Year', as_index=False)
month_data = measurements_forecast_data.groupby('Month', as_index=False)
day_data = measurements_forecast_data.groupby('Day', as_index=False)

year_data = year_data.aggregate(function_dict).round(decimals=2)
month_data = month_data.aggregate(function_dict).round(decimals=2)
day_data = day_data.aggregate(function_dict).round(decimals=2)


day_data_all = measurements_forecast_data_all.groupby('no_hour_date', as_index=False)
day_data_all = day_data_all.aggregate(function_dict_measurements_forecast_data_all).round(decimals=2)
day_data_all = day_data_all.drop(['measurement_prediction','prediction_error'],axis=1)
day_data_all.sort_values(by='no_hour_date',inplace=True)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash(
    "ForecastDashboard",
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=external_stylesheets
)

def update_dash():

    n=1000
    plot = go.Figure(data=[go.Scatter(
        x=pd.Series(measurements_forecast_data_all["prediction_date"]), y=pd.Series(measurements_forecast_data_all["prediction_percentage_error"]), 
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
                    html.Table(make_dash_table(day_data), style = {"border": "1px solid black", "border-collapse": "collapse"}),
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
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            
        html.Div([
                    dcc.Graph(id='grafico_correlacao')
                ], style={'height': 200}),                
            ], className="row"),
    ])


@app.callback(
    Output('historico_previsao', 'figure'),    [ 
        Input('ndays-plot', 'value')]
)
def update_graph_raw(ndays_plot):    
    ydata = measurements_forecast_data['historic_measurement']
    xdata = measurements_forecast_data['historic_measurement_date']
    xdata_forecast = measurements_forecast_data['prediction_date']
    ydata_forecast = measurements_forecast_data['measurement_prediction']

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
    xdata_forecast_all = measurements_forecast_data_all['prediction_date']
    ydata_forecast_all = measurements_forecast_data_all['prediction_percentage_error']
    xdata_forecast_all_grouped_by_day = day_data_all['no_hour_date']
    ydata_forecast_all_grouped_by_day = day_data_all['prediction_percentage_error'] 

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




@app.callback(
Output('grafico_correlacao', 'figure'),
[  Input('ndays-plot', 'value')]
)

def update_graph_forecast(ndays_plot): 
    
    columns = ['PJME_MW']
    intervals = [1, 2, 3, 5, 10, 15, 20, 24, 48, 72, 96, 120, 240, 360, 720]
    forecast_shift_data = medicao_historica_periodo_treinamento[['data_medicao','PJME_MW']]
    for x in intervals:
        moved = forecast_shift_data  [columns].shift(x)
        moved.ffill(axis ='rows', inplace=True)        

        if x/24 < 2:
            moved.columns = [str(x) + ' hours']
        else: 
            moved.columns = [str(int(x/24)) + ' days']        

        forecast_shift_data  = pd.concat([moved,forecast_shift_data ], axis=1)
    corr =forecast_shift_data.corr()['PJME_MW'].drop('PJME_MW')     
    

    correlation_data = []
    correlation_data.append(go.Bar(        
        x=corr.index,
        y=corr.values,       
        legendgroup='Correlação entre as mediÃ§Ãµes históricas',
        showlegend=True,
        name='Correlação',
        type='bar'      

    ))   

    my_layout = go.Layout(
            xaxis={'title': ' '},
            yaxis={'title': 'Consumo(MW)'},
            margin={'l': 60, 'r': 40, 't': 40, 'b': 50},
            hovermode='closest',            
            title='Correlação entre as medições históricas'
        )

    fig = {'data':  correlation_data, 'layout':my_layout}

    return fig


    

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from django_plotly_dash import DjangoDash

from taxi import models
from taxi import serializers
import plotly.figure_factory as ff

import numpy as np
import math

from nyctaxi.settings import TAXI_MODEL_WORKDIR
from taxi import globalTrainResults



dev_data = TAXI_MODEL_WORKDIR + '/Data/Modeling/dev_results.jbl'
prev_data = TAXI_MODEL_WORKDIR + '/Data/Processed/nyctaxi_data_analysis_green.parquet'

# Training data
data = pd.read_parquet(dev_data)

#PRediction New Data
data_prev = pd.read_parquet(prev_data)
data_prev['idTaxi'] = data_prev.index.values
data_prev['estimated_fare'] = 0


# Read operation data
# ALERTA: COMENTAR ANTES DE FAZER python manage.py migrate.
# DESCOMENTAR DEPOIS PARA FUNCIONAR CORRETAMENTE
taxi_list = models.Taxi.objects.order_by('-estimated_fare')
taxi_data = serializers.TaxiSerializer(taxi_list, many=True)
taxi_table = pd.DataFrame(taxi_data.data)
model = globalTrainResults['model']


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            val = row[i] if isinstance(row[i],str) else '%.2f'%(row[i])
            html_row.append(html.Td([val]))
        table.append(html.Tr(html_row))
    return table



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] #['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash(
    "TaxiDashboard",
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    # external_stylesheets=external_stylesheets
)

def update_dash():
    # Create dist plots
    hist_data = [taxi_table['fare_amount'].values, taxi_table['estimated_fare'].values]
    fig_dist = ff.create_distplot(hist_data, ['Preço Real', 'Preço Estimado'],show_hist=False)
    ntop = 10

    model = globalTrainResults['model']
    variables = globalTrainResults['variables']

    df_feature_importances = pd.DataFrame(model.feature_importances_*100,columns=["Importance"],index=variables)
    df_feature_importances = df_feature_importances.sort_values("Importance", ascending=False)

    # We create a Features Importance Bar Chart
    fig_features_importance = go.Figure()
    fig_features_importance.add_trace(go.Bar(x=df_feature_importances.index,
                                            y=df_feature_importances["Importance"],
                                            marker_color='rgb(171, 226, 251)')
                                    )
    fig_features_importance.update_layout(title_text='<b>Features Importance<b>', title_x=0.5)

    app.layout = html.Div(children=[
        html.H1(children='Dashboard das Tarifas de Taxis na cidade de Nova York'),

        html.P(children='''
            Desenvolvimento de modelos de previsão de tarifas das corridas de táxi na cidade de Nova York
        '''),
        dcc.Graph(figure=fig_features_importance),

        html.Div([
            # New Div for both plots
            html.Div([
            

                html.Div([
                    html.H3('Maiores ' + str(ntop) + ' Tarifas'),
                    html.Table(make_dash_table(taxi_table[['idTaxi','estimated_fare']].head(ntop)))
                ], className="six columns"),

                html.Div([
                    html.H3('Distribuição das Tarifas'),
                    dcc.Graph(
                        id='score-dist',
                        figure=fig_dist
                    )
                ], className="six columns"),

                html.Div([
                    html.H3('Variáveis do Taxi'),
                    dcc.Dropdown(
                        id='taxi_selection',
                        options = [{'label': val, 'value': val} for val in taxi_table.idTaxi.sort_values().unique()],
                        value=taxi_table.idTaxi.sort_values().unique()[0],
                        multi=False,
                        placeholder='Escolha um Id da Corrida',
                    ),
                    dcc.Graph(
                        id='taxi-variables'
                    )
                ], className="six columns"),

                html.Div([
                    html.H3('Previsão'),
                    html.Button('Previsão', id='previsao'),
                    html.Div(id='output-container-button',
                            children=''),
                ], className="six columns"),

                html.Div([
                    html.H3('Maiores ' +  ' Tarifas'),
                    html.H5(['idTaxi ',' | estimated_fare | ',' | fare_amount']),
                    html.Table(
                        children = '',
                        id='tabela',
                    ),
                ], className="six columns"),

            ], className="row")
        ]),
    ])



@app.callback(
    Output(component_id='taxi-variables', component_property='figure'),
    [Input(component_id='taxi_selection', component_property='value')]
)
def update_taxi_variables(selected_taxi):
    if isinstance(selected_taxi, str):
        selected_taxi = [selected_taxi]
    taxi_vars = taxi_table[taxi_table.idTaxi.isin([selected_taxi])].copy()
    taxi_vars = (taxi_vars.drop(['idTaxi', 'year','eucl_distance','manh_distance'], axis=1)
                          .reset_index(drop=True)
                          .T
                          .rename({0:'Valor'}, axis=1)
                          .rename_axis("Atributos")
                          .reset_index())
    return px.bar(taxi_vars, x="Atributos", y="Valor")        

@app.callback(
    Output(component_id='output-container-button', component_property='children'),
    [Input(component_id='previsao', component_property='n_clicks')]
)
def previsao_botao(n_clicks):
    if n_clicks:
        result = model.predict([data_prev[globalTrainResults['variables']]][0])
        data_prev['estimated_fare'] = result
        result = "US $ "+ str(result[n_clicks-1])
        return result
    else:
        return "Aperte o botão para realizar uma previsão"
    
@app.callback(
    Output(component_id='tabela', component_property='children'),
    [Input(component_id='previsao', component_property='n_clicks')]
)
def update_tabela(n_clicks):
    if n_clicks:
        return make_dash_table(data_prev[['idTaxi','estimated_fare','fare_amount']].head(n_clicks))
    else:
        return make_dash_table(data_prev[['idTaxi','estimated_fare','fare_amount']].head(0)) 

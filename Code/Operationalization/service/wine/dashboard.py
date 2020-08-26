import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas
import plotly.express as px


from django_plotly_dash import DjangoDash

from wine import models
from wine import serializers
import plotly.figure_factory as ff

import numpy as np

from service.settings import WINE_MODEL_WORKDIR



dev_data = WINE_MODEL_WORKDIR + '/Data/Modeling/dev_results.jbl'



# Training data
data = pandas.read_parquet(dev_data)

# Read operation data
# ALERTA: COMENTAR ANTES DE FAZER python manage.py migrate.
# DESCOMENTAR DEPOIS PARA FUNCIONAR CORRETAMENTE
wine_list = models.Wine.objects.order_by('-estimated_score')
wine_data = serializers.WineSerializer(wine_list, many=True)
wine_table = pandas.DataFrame(wine_data.data)



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



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash(
    "WineDashboard",
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    # external_stylesheets=external_stylesheets
)

def update_dash():
    # Create dist plots
    hist_data = [wine_table['estimated_score'].values, data.estimated_score.values]
    fig_dist = ff.create_distplot(hist_data, ['Menu Ofertado', 'Menu Referencia'],show_hist=False)
    ntop = 10

    app.layout = html.Div(children=[
        html.H1(children='Dashboard do Menu de Vinhos'),

        html.P(children='''
            Desenvolvimento de modelos de previsão de vendas de uma grande rede de lojas de departamentos.
        '''),

        html.Div([
            # New Div for both plots
            html.Div([
                html.Div([
                    html.H3('Top ' + str(ntop) + ' Vinhos'),
                    html.Table(make_dash_table(wine_table[['name','estimated_score']].head(ntop)))
                ], className="six columns"),

                html.Div([
                    html.H3('Distribuição do score dos Vinhos'),
                    dcc.Graph(
                        id='score-dist',
                        figure=fig_dist
                    )
                ], className="six columns"),

                html.Div([
                    html.H3('Variáveis do Vinho'),
                    dcc.Dropdown(
                        id='wine_selection',
                        options = [{'label': val, 'value': val} for val in wine_table.name.sort_values().unique()],
                        value=wine_table.name.sort_values().unique()[0],
                        multi=False,
                        placeholder='Escolha um Vinho',
                    ),
                    dcc.Graph(
                        id='wine-variables'
                    )
                ], className="six columns"),

            ], className="row")
        ]),

    ])




@app.callback(
    Output(component_id='wine-variables', component_property='figure'),
    [Input(component_id='wine_selection', component_property='value')]
)
def update_wine_variables(selected_wine):
    if isinstance(selected_wine, str):
        selected_wine = [selected_wine]
    wine_vars = wine_table[wine_table.name.isin(selected_wine)].copy()
    wine_vars = (wine_vars.drop(['name', 'estimated_score'], axis=1)
                          .reset_index(drop=True)
                          .T
                          .rename({0:'Valor'}, axis=1)
                          .rename_axis("Atributos")
                          .reset_index())
    return px.bar(wine_vars, x="Atributos", y="Valor")

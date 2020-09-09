import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas
import plotly.express as px
import dash_table as dt
from django_plotly_dash import DjangoDash

from get_breed import models
from get_breed import serializers
import plotly.figure_factory as ff
import requests
import urllib.request
import numpy as np


dev_data = 'C:/Users/cammy/OneDrive/MIT IA/git/projeto_dogs/dogs_brand/Data/Modeling/dev_results.jbl'
classes_file = 'C:/Users/cammy/OneDrive/MIT IA/git/projeto_dogs/dogs_brand/Data/Modeling/classes.jbl'

baseurl = 'https://dog.ceo/api/'
randomappend = '/images/random/'


#with open(classes_file, 'rb') as f:
#    classes = pd.read_parquet(f, engine='pyarrow')
classes = pandas.read_parquet(classes_file)

# Training data
data = pandas.read_parquet(dev_data)

# Read operation data
# ALERTA: COMENTAR ANTES DE FAZER python manage.py migrate.
# DESCOMENTAR DEPOIS PARA FUNCIONAR CORRETAMENTE
pictures_list = models.Pictures.objects
pictures_data = serializers.PicturesSerializer(pictures_list, many=True)
pictures_table = pandas.DataFrame(pictures_data.data)

app = DjangoDash(
    "DogsDashboard",
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    # external_stylesheets=external_stylesheets
)

@app.callback([
    dash.dependencies.Output('image', 'src'),
    dash.dependencies.Output('real_breed', 'children'),
    dash.dependencies.Output('classification', 'children'),
    dash.dependencies.Output('estimated_score1', 'children'),
    dash.dependencies.Output('estimated_score2', 'children'),
    dash.dependencies.Output('estimated_score3', 'children')],
    [dash.dependencies.Input('image-dropdown', 'value')])

def update_image_src(value):
    return value[0], value[1], value[2], value[3], value[4], value[5]

@app.callback([
    dash.dependencies.Output('image_random', 'src'),
    dash.dependencies.Output('real_breed_random', 'children'),
    dash.dependencies.Output('classification_random', 'children'),
    dash.dependencies.Output('estimated_score1_random', 'children'),
    dash.dependencies.Output('estimated_score2_random', 'children'),
    dash.dependencies.Output('estimated_score3_random', 'children')],
    [dash.dependencies.Input('my-button', 'n_clicks'),
    dash.dependencies.Input('classes-dropdown', 'value')])

def on_click(n_clicks, value):
    filesurl = baseurl + 'breed/' + value + randomappend
    imageurl = requests.get(filesurl).json()
    breedimage = imageurl['message']

    payload = {
        'address' : breedimage,
        'real_breed' : value
    }
    posturl = 'http://127.0.0.1:8000/pictures_classifier/'

    picture_obj = requests.post(posturl, json=payload).json()

    return breedimage, value, picture_obj['classification'], picture_obj['estimated_score1'], picture_obj['estimated_score2'], picture_obj['estimated_score2']


def update_dash():

    # Read operation data
    # ALERTA: COMENTAR ANTES DE FAZER python manage.py migrate.
    # DESCOMENTAR DEPOIS PARA FUNCIONAR CORRETAMENTE
    pictures_list = models.Pictures.objects
    pictures_data = serializers.PicturesSerializer(pictures_list, many=True)
    pictures_table = pandas.DataFrame(pictures_data.data)

    hist_data1 = [pictures_table['estimated_score1'].values, data.estimated_score1.values]
    hist_data2 = [pictures_table['estimated_score2'].values, data.estimated_score2.values]
    hist_data3 = [pictures_table['estimated_score3'].values, data.estimated_score3.values]
    fig_dist1 = ff.create_distplot(hist_data1, ['Base Produção', 'Treinamento'],show_hist=False)
    fig_dist2 = ff.create_distplot(hist_data2, ['Base Produção', 'Treinamento'],show_hist=False)
    fig_dist3 = ff.create_distplot(hist_data3, ['Base Produção', 'Treinamento'],show_hist=False)
    ntop = 10

    app.layout = html.Div([
        html.H1(children='Dashboard de Raça de Cachorros'),

        html.P(children='''
            Desenvolvimento de modelos de previsão da raça a partir da foto de um cachorro
        '''),

        html.Div([
            html.H2('Distribuição do score das raças'),
            html.H3(classes.values[0]),
            dcc.Graph(
                id='score-dist',
                figure=fig_dist1
            ),
            html.H3(classes.values[1]),
            dcc.Graph(
                id='score-dist2',
                figure=fig_dist2
            ),
            html.H3(classes.values[2]),
            dcc.Graph(
                id='score-dist3',
                figure=fig_dist3
            )
        ], className="six columns"),

        html.H3('Visualização das classificações'),

        dcc.Dropdown(
            id='image-dropdown',
            options=[{'label': i[0], 'value': i}  for i in pictures_table.values],
        value=pictures_table.values[0]
        ),
        html.Div([
            html.Table(
                html.Tr([
                    html.Td(html.Img(id='image')),
                    html.Td(
                        html.Table([
                            html.Tr([html.Td('Real Breed:'), html.Td(id='real_breed')]),
                            html.Tr([html.Td('Classification:'), html.Td(id='classification')]),
                            html.Tr([html.Td('Estimated Score:')]),
                            html.Tr([html.Td(classes.values[0]), html.Td(id='estimated_score1')]),
                            html.Tr([html.Td(classes.values[1]), html.Td(id='estimated_score2')]),
                            html.Tr([html.Td(classes.values[2]), html.Td(id='estimated_score3')]),
                        ])
                    )
                ])
            )
        ]),
        html.Div([
            html.H3('Imagem Randômica'),
            html.Table(
                html.Tr([
                    html.Td(dcc.Dropdown(
                        id='classes-dropdown',
                        options=[{'label': i[0], 'value': i[0]}  for i in classes.values],
                        value=classes.values[0]
                    )),
                    html.Td(
                         html.Button('Pegar Imagem', id='my-button')
                    )
                ])
            )
        ]),
        html.Div([
            html.Table(
                html.Tr([
                    html.Td(html.Img(id='image_random')),
                    html.Td(
                        html.Table([
                            html.Tr([html.Td('Real Breed:'), html.Td(id='real_breed_random')]),
                            html.Tr([html.Td('Classification:'), html.Td(id='classification_random')]),
                            html.Tr([html.Td('Estimated Score:')]),
                            html.Tr([html.Td(classes.values[0]), html.Td(id='estimated_score1_random')]),
                            html.Tr([html.Td(classes.values[1]), html.Td(id='estimated_score2_random')]),
                            html.Tr([html.Td(classes.values[2]), html.Td(id='estimated_score3_random')]),
                        ])
                    )
                ])
            )
        ])
    ])


# if __name__ == '__main__':
#     app.run_server(debug=True)

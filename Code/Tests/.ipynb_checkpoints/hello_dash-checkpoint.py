import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash Again!'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)

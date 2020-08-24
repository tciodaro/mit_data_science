# Plot imports
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd



# FILE CONFIGURATION
WORKDIR = 'C:/Users/BZ241WX/Documents/InfNet/CursoPosDataScience/mit_data_science/'
forecast_file = WORKDIR + '/Data/Modeling/forecast_results.parquet'

# LOAD FILE
data = pd.read_parquet(forecast_file)
data = data.dropna().groupby('Date')['Weekly_Sales','forecast'].sum()


def make_scatter(id_fig, x, y, xtitle, ytitle):
    # GRAPH
    return  dcc.Graph(
                id=id_fig,
                figure={
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
            )


# CREATE APP
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)



# CREATE LAYOUT
app.layout = html.Div(children=[
    # Main Header
    html.H1(children='Dashboard de Previsão de Vendas'),    
    # Subtitle
    html.P('''Desenvolvimento de modelos de previsão de vendas de uma
              grande rede de lojas de departamentos.
           '''),
    
    # New Div for both plots
    html.Div(children=[
        html.Div([
            html.H3('Gráfico de Resíduos'),
            make_scatter('residuos', data.Weekly_Sales, data.Weekly_Sales-data.forecast,
                         xtitle='Historico de Vendas', ytitle='Erro da Previsão (Real - Previsto)')
        ], className="six columns"),

        html.Div([
            html.H3('Dispersão dos Resultados'),
            make_scatter('dispersao', data.Weekly_Sales, data.forecast,
                         xtitle='Historico de Vendas', ytitle='Previsão de Vendas')
        ], className="six columns"),
    ], className="row")    
    
])



app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

# RUN SERVER
if __name__ == '__main__':
    app.run_server(debug=True, port=8000)

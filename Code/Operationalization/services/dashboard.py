import dash
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash
import pandas as pd
import plotly.express as px
from  applications.models import predicao, estatistica
from  dash.dependencies import Input, Output
from  datetime import datetime
import dash_table

app = DjangoDash('DashboardSIN')   # replaces dash.Dash

# Recupera os dados do relatório
df_relatorio = pd.DataFrame(estatistica.objects.all().values())

# Faz o setup do gráfico do relatório
fig = px.bar(df_relatorio , x="din_execucao"
                          , y="qtd_registro"
                          , color="tip_legenda"
                          , title="Estatistica Sobre Supervisão"
                          , labels = { "din_execucao":"Mês/Dia",
                                       "qtd_registro":"Quantidade",
                                       "tip_legenda":"Previsão"
                                     }
            )

fig.update_layout(
    font_family="Courier New",
    font_color="blue",
    title_font_family="Times New Roman",
    title_font_color="red",
    legend_title_font_color="black",
    xaxis={'type': 'category'},
    barmode='group'
)



# Faz o setup da tabela dos registros

# Recupera os dados dos registros do dia
dat_inicio = datetime.strptime('01/08/2020', '%d/%m/%Y')

# Filtra dataframe para a data específica
df_insumosin = pd.DataFrame(predicao.objects.values('id','dsc_texto','tip_supervisao','din_execucao','tip_predicao','pct_predicao','val_realpredicao'))

# Ajusta textos das colunas
df_insumosin['dsc_texto'] = df_insumosin['dsc_texto'].str.slice(0, 50) + '...'


#Renomeando as colunas
renome_coluna = {'id':"Identificador"
                ,'dsc_texto':'Texto'                
                ,'tip_supervisao': "Supervisao-Predição"
                ,'din_execucao':'Data da Previsão'
                ,'tip_predicao':'Previsão'
                ,'pct_predicao':'% Acerto'
                ,'val_realpredicao': 'Supervisão-Validada'
                }

df_insumosin.rename(columns = renome_coluna, inplace = True)



df_insumosin['index'] = range(1, len(df_insumosin) + 1)

PAGE_SIZE = 10

app.layout = html.Div(
    children=[
                html.H1(children='Dashboard Operacional - Supervisão da Manutenção de Equipamentos'),

                html.Div([
                                dcc.Graph(
                                id='relatorio-graph',
                                figure=fig,
                                responsive=True
                        )
                ]),
                dash_table.DataTable(
                                    id='datatable-paging',
                                    columns=[
                                        {"name": i, "id": i} for i in df_insumosin.columns
                                    ],
                                    page_current=0,
                                    page_size=PAGE_SIZE,
                                    page_action='custom'
                                )
             ]
)

@app.callback(
    Output('datatable-paging', 'data'),
    [Input('datatable-paging', "page_current"),
     Input('datatable-paging', "page_size")])
def update_table(page_current,page_size):
    return df_insumosin.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')


import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as  pd
import numpy as np
import os
from pathlib import Path
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path_database = BASE_DIR + '\db.sqlite3'
print(BASE_DIR)


#path_database = 'C:/Users/Janine/Documents/infnet/01projeto/Code/Operacao/raiz/api/db.sqlite3'
sqliteConnection = sqlite3.connect(path_database)
df_insumo = pd.read_sql_query("SELECT tip_supervisao FROM applications_dadospredicao", sqliteConnection)
df_predicao = pd.read_sql_query("SELECT tip_predicao, tip_evento FROM applications_dadospredicao order by tip_predicao desc", sqliteConnection)
df_estatistica = pd.read_sql_query("SELECT dsc_predicao, qtd_registro FROM applications_dadosestatistica", sqliteConnection)

#print(dataframe.head())
sqliteConnection.close()

# Grafico de Barras - Origem SQl Lite
# --------------------------------------------
var_alvo = df_insumo.groupby('tip_supervisao').tip_supervisao.count()
x = var_alvo.index
y = var_alvo.values
#print (x)
var_alvo_p = df_predicao.groupby('tip_predicao').tip_predicao.count()
x_p = var_alvo_p.index
y_p = var_alvo_p.values
#print (x_p)
var_alvo_e = df_predicao.groupby('tip_evento').tip_predicao.count()
x_e = var_alvo_e.index
y_e = var_alvo_e.values
#print (x_p)


# Grafico de Pizza - Origem SQl Lite
# --------------------------------------------
var_alvo2 = df_estatistica.groupby('dsc_predicao').dsc_predicao.count()  
x2 = var_alvo2.index
y2 = var_alvo2.values         


# Grafico de PIZZA - CSV
# --------------------------------------------
#source_file = 'C:/Users/Janine/Documents/infnet/01projeto/Data/Operacao/dados_result.parquet'
#dataframe_csv = pd.read_parquet(source_file)
#var_alvo_csv = dataframe_csv.groupby('tip_predicao').tip_predicao.count()
#x_csv = var_alvo_csv.index
#y_csv = var_alvo_csv.values


# Grafico DASH
# --------------------------------------------
app = dash.Dash()

app.layout = html.Div(children=[
    html.H1('G R A F I C O S  DO P R O J E T O'),
    dcc.Graph(id='graf_01',
              figure={
                'data':[ 
                        {'x':x, 'y': y, 'type':'bar','color':'medal'}                   
                       ],
                'layout':{
                    'title':'Quantitativo de Insumos'                      
                }
             })
    ,     
    dcc.Graph(id='graf_02',
              figure={
                'data':[ 
                        {'x':x_p, 'y': y_p, 'type':'bar','color':'medal'}                   
                       ],
                'layout':{
                    'title':'Quantitativo de Predição'                      
                }
             })
    ,        
    dcc.Graph(id='graf_03',
              figure={
                'data': [
                     {'names':x_p, 'values': y_p, 'type':'pie'}                     
                     ],
                'layout':{
                    'title':'Gráfico Predicao'                        
                }
             })   
    ,     
    dcc.Graph(id='graf_04',
             figure={
               'data': [
                    {'x':x_e , 'y': y_e,   'type':'bar','name':'Insumo' },
                    {'x':x_p , 'y': y_p, 'type':'bar','name':'Predicao' },
                    ],
               'layout':{
                   'title':'Insumo x Predicao'                    
               }
            })
    ,                
    dcc.Graph(id='graf_05',
             figure={
               'data': [
                    {'x':x2, 'y': y2, 'type':'bar','name':'Insumo' }
                    ],
               'layout':{
                   'title':'Estatistica',                    
               }
            })
    #,   
         
])


if __name__ == '__main__':
	app.run_server(debug=True)
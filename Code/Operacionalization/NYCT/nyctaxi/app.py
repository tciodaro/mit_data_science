import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
import joblib
from sklearn.preprocessing import MinMaxScaler

WORKDIR = 'C:/Users/Paulo/NYC-Taxi/'

dev_data = WORKDIR + '/Data/Modeling/dev_results.jbl'
anl_data = WORKDIR + '/Data/Processed/nyctaxi_data_analysis.parquet'

# função para carregar o dataset
@st.cache
def get_data():
    return pd.read_parquet(dev_data)


# função para treinar o modelo
def train_model():
    data = pd.read_parquet(anl_data)
    #x = data.drop(["fare_amount",'estimated_fare','idTaxi'],axis=1) 
    x = data.drop(["fare_amount"],axis=1)
    y = data["fare_amount"]

    modGBR = GradientBoostingRegressor()
    modGBR.fit(x, y)
    return modGBR

# criando um dataframe
data = get_data()

# treinando o modelo
model = train_model()

# título
st.title("Data App - Prevendo Tarifas de Taxi")

# subtítulo
st.markdown("Este é um Data App utilizado para exibir a solução de Machine Learning para o problema de predição de valores de tarifas de Taxi de Nova York.")

# verificando o dataset
st.subheader("Selecionando apenas um pequeno conjunto de atributos")

# atributos para serem exibidos por padrão
defaultcols = ["pickup_longitude","year","eucl_distance","fare_amount"]

# defindo atributos a partir do multiselect
cols = st.multiselect("Atributos", data.columns.tolist(), default=defaultcols)

# exibindo os top 10 registro do dataframe
st.dataframe(data[cols].head(10))


st.subheader("Distribuição de tarifas de taxi por preço")

# definindo a faixa de valores
faixa_valores = st.slider("Faixa de preço", float(data.fare_amount.min()), 100., (0.0, 100.0))

# filtrando os dados
dados = data[data['fare_amount'].between(left=faixa_valores[0],right=faixa_valores[1])]

# plot a distribuição dos dados
f = px.histogram(dados, x="fare_amount", nbins=100, title="Distribuição de Preços")
f.update_xaxes(title="fare_amount")
f.update_yaxes(title="Total Tarifas")
st.plotly_chart(f)

g = px.line(dados, y=["fare_amount",'estimated_fare'],  title="Distribuição de Preços")
g.update_yaxes(title="fare_amount")
g.update_xaxes(title="Total Tarifas")
st.plotly_chart(g)


st.sidebar.subheader("Defina os atributos do imóvel para predição")

# mapeando dados do usuário para cada atributo
plat = st.sidebar.number_input("Latitude de Saida", value=data.pickup_latitude.mean(), format="%.4f")
plon = st.sidebar.number_input("Longitude de Saida", value=data.pickup_longitude.mean(), format="%.4f")

dlat = st.sidebar.number_input("Latitude de Chegada", value=data.dropoff_latitude.mean(), format="%.4f")
dlon = st.sidebar.number_input("Longitude de Chegada", value=data.dropoff_longitude.mean(), format="%.4f")

npas = st.sidebar.number_input("Número de Passageiros", value=1);

hour = st.sidebar.number_input("Hora do Dia", value=data.hour_of_day.min());
dayW = st.sidebar.number_input("Dia da Semana", value=data.day_of_week.min());
dayY = st.sidebar.number_input("Dia do Ano", value=data.day_of_year.min());
year = st.sidebar.number_input("Ano", value=data.year.min());

eucl = st.sidebar.number_input("Distância Euclidiana", value=data.eucl_distance.mean(), format="%.6f")
manh = st.sidebar.number_input("Distância Manhattan", value=data.manh_distance.mean(), format="%.6f")


# inserindo um botão na tela
btn_predict = st.sidebar.button("Realizar Predição")

# verifica se o botão foi acionado
if btn_predict:
    result = model.predict([[plat,plon,dlat,dlon,npas,hour,dayW,dayY,year,eucl,manh]])
    st.subheader("O valor previsto para a tarifa é:")
    result = "US $ "+str(round(result[0]))
    st.write(result)


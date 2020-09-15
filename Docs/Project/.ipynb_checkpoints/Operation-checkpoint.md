# Operação

# Coleta de Dados

Rodar o notebook [data_collection](../../Code/DataPrep/data_collection.jpnb "Data Collection")

# Geração do Modelo

Rodar o notebook [modeling](../../Code/Model/modeling.jpnb "Data Collection")

# Dashboard

Para acessar o dashboard, após rodar o server Django, acessar http://127.0.0.1:8000/dash/

# Serviços

Além do dashboard, é possível acessar os serviços diretamente:

http://127.0.0.1:8000/classifybreed/
Ao passar no formato json uma url de uma foto retorna a classificação

http://127.0.0.1:8000/pictures_classifier/
Acessar o método post enviando dados no seguinte formato (json):
{
    "address": "<endereço url>",
    "real_breed": "<raça real (opcional)>",
}
Retorna a classificação e os scores, além de gravar no banco de operações.
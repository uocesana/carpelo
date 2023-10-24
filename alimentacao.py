import requests
import json
import pandas as pd
import streamlit as st
import datetime

st.set_page_config(page_title='Acompanhamento de Requisição de Alimentação', page_icon='refeicao.png', layout='wide')
# st.set_page_config(
#     page_title="Acompanhamento de Requisição de Alimentação",
#     layout="wide"

st.header(":spaghetti: Solicitações de Alimentação")
st.markdown("#")
st.markdown("""---""")
# qmokh1qdw1cs8k4cc04ow4wckkggcww
# #     )
# st.title('Solicitação de Alimentação')
# st.image('logo_refeicao.png')
# URL da API
url = "https://coletum.com/api/graphql?query={answer(formId:29174){answer{dataDaRetirada425488,encarregado425489,restaurante425490,almoco425491,janta429511,cafeDaManha429512,observacao438633},metaData{userId,userName,createdAtSource,friendlyId,createdAt,createdAtDevice,createdAtCoordinates,updatedAt,updatedAtCoordinates}}}&token=" # delimitando intervalo de dados de 2000 a 2024

# Faz a requisição GET à API
response = requests.get(url)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    # Converte a resposta para formato JSON
    data = response.json()

    # Cria um DataFrame a partir dos dados JSON
    df = pd.DataFrame(data)

else:
    print("Falha na requisição à API:", response.status_code)


carrega_dados = pd.json_normalize(df['data']['answer']).query("`answer.restaurante425490` == 'RESTAURANTE BRASEIRO DO SUL'")

# seleciona apenas as colunas necessarias do dataframe. No segundo bloco de código renomeia as colunas do dataframe e aplica o método fillna para substituir os valores NaN por zero (0)
carrega = carrega_dados[['answer.dataDaRetirada425488',
                         'answer.encarregado425489',
                        #  'answer.restaurante425490',
                         'answer.almoco425491',
                         'answer.janta429511',
                         'answer.cafeDaManha429512',
                         ]].rename(columns={
                            "answer.dataDaRetirada425488":"data",
                            "answer.encarregado425489":"encarregado",
                            #"answer.restaurante425490":"restaurante",
                            "answer.almoco425491":"almoco","answer.janta429511":"jantar",
                            "answer.cafeDaManha429512":"cafe_da_manha",
                            }).fillna(0)

# answer.observacao438633":"observacoes ultima coluna


# carrega[["almoco","jantar","cafe_da_manha"]] = carrega[["almoco","jantar","cafe_da_manha"]].astype(float).astype(int)
# datas = carrega_dados['answer.dataDaRetirada425488']

encarregados = carrega['encarregado'].unique()

col1, col2 = st.columns(2)

with col1:
    encarregado = st.multiselect("Selecione o encarregado", 
                                 options=encarregados,
                                 default=encarregados)

# with col2:
#     inicial = st.date_input("Período Inicial", datetime.datetime.now())
#     final = st.date_input("Período Final",datetime.datetime.now())

    
carregando = carrega.query("encarregado == @encarregado").groupby(['data', 'encarregado']).sum().astype(float).astype(int).reset_index()
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(carregando)


# almoco = carregando['almoco'].sum()
# carrega_2 = carregando.groupby(['data', 'encarregado']).sum() 

# st.dataframe(carregando)
# st.dataframe(almoco) 
st.dataframe(carregando)  


# Defaults to 'application/octet-stream'
st.download_button(
    label="Download arquivo",
    data=csv,
    file_name='arquivo.csv',
    mime='text/csv',
)
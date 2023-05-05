import numpy as np
import geobr
import plotly as plt
import matplotlib.pyplot as plt
import pandas as pd
from time import time
from time import sleep
from datetime import datetime
from datetime import timedelta
from random import randint
from time import time
import pickle
from sys import argv
import os

tempo_inicial = time()

pd_df = pd.DataFrame([])
param = argv[1]
print('Brasil:', param)
with open(f'./matplotimages/{argv[1]}', 'rb') as handle:
    try:
        pd_df = pickle.load(handle)
    except ModuleNotFoundError:
        pd_df = pd.read_pickle(handle)

# faixa = {'value': 'Crianças e adultos'}

# filtro = None
# if(faixa['value'] == 'Criança'):
#   filtro = 'CRI. IMC X IDADE'
# elif(faixa['value'] == 'Adulto'):
#   filtro = 'ADO. IMC X IDADE'
# elif(faixa['value'] == 'Crianças e adultos'):
#   filtro = '*'

mapa_brasil = geobr.read_state()
fig, ax = plt.subplots(figsize=(10, 15), dpi=100)

# mapa_brasil.plot(facecolor="#2D3E50", edgecolor="#FEBF57", ax=ax)

# A partir da faixa definida acima, classifica se o estado está saudável
def classificar(estado):
  estado_filtrado = None
  mode = None
  try:
    estado_filtrado = pd_df[pd_df['SG_UF'] == estado]
    # mode = pd.DataFrame([x for x in estado_filtrado['CRI. IMC X IDADE'].values if x != -1]+[x for x in estado_filtrado['ADO. IMC X IDADE'].values if x != -1]).mean()
    mode = estado_filtrado['DS_IMC'].mean()
  except:
     #print('except\n\n\n', estado)
     return 0
  # if(faixa['value'] == 'Crianças e adultos'):
  #   estado_filtrado = pd_df[pd_df['SG_UF'] == estado]
  #   mode = pd.DataFrame([x for x in estado_filtrado['CRI. IMC X IDADE'].values if x != -1]+[x for x in estado_filtrado['ADO. IMC X IDADE'].values if x != -1]).mean()
  #   # mode = pd.DataFrame([x for x in estado_filtrado['CRI. IMC X IDADE'].values if x != -1]+[x for x in estado_filtrado['ADO. IMC X IDADE'].values if x != -1]).mode()[0].values[0]
  # elif(faixa['value'] == 'Criança' or faixa['value'] == 'Adulto'):
  #   estado_filtrado = pd_df[((pd_df['SG_UF'] == estado) & (pd_df[filtro] != -1))]
  #   # print(len(estado_filtrado))
  #   mode = estado_filtrado[filtro].mean()#.values[0]
  # else:
  #   raise TypeError('Adicione um filtro de idade para gerar o mapa corretamente!')
  return mode

estado_moda = {}
for estado in ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG',
               'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR',
               'RS', 'SC', 'SE', 'SP', 'TO']:
  estado_moda.update({estado: classificar(estado)})
mapa_brasil['situacao_nutricional'] = mapa_brasil['abbrev_state'].apply(lambda x: estado_moda[x])

fig = mapa_brasil.plot(
    cmap="Blues_r",
    legend=True,
    column='situacao_nutricional',
    legend_kwds={
        "label": "Situação nutricional nacional (de magreza-acentuada a obesidade)",
        "orientation": "horizontal",
        "shrink": 0.6,
    },
    ax=ax,
)
ax.set_title(f"Mapa da média nutricional nacional", fontsize=20)
ax.axis("off")
print('Tempo total:', int((time()-tempo_inicial)/60), 'minutos e', int(time()-tempo_inicial)%60, 'segundos.')

fig.get_figure().savefig(f'./matplotimages/{argv[1]}.png', bbox_inches='tight')

if os.path.exists(f"./{argv[1]}"):
    os.remove(f"./{argv[1]}")

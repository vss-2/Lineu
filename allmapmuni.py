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

muni = []

with open(f'./citiesjsons/{argv[1]}', 'rb') as handle:
    try:
        muni = pickle.load(handle)
    except ModuleNotFoundError:
        muni = pd.read_pickle(handle)

tempo_inicial = time()

fig, ax = plt.subplots(figsize=(10, 10), dpi=50)
estado = geobr.read_state(code_state=argv[1], year=2010)
estado.plot(facecolor="#2D3E50", edgecolor="#FEBF57", ax=ax, cmap="Blues_r")

pd_df = pd.DataFrame([])

with open(f'./df.pickle', 'rb') as handle:
    try:
        pd_df = pickle.load(handle)
    except ModuleNotFoundError:
        pd_df = pd.read_pickle(handle)


pd_df = pd_df[pd_df['SG_UF'] == argv[1]]

for m in muni:
    # Como destacar uma cidade
    temp_df = pd_df[pd_df['CO_MUNICIPIO_IBGE'] == int(str(m)[:-1])]
    #mode = pd.DataFrame([x for x in temp_df['CRI. IMC X IDADE'].values if x != -1]+[x for x in temp_df['ADO. IMC X IDADE'].values if x != -1]).mode()[0].values[0]
    mode = pd.DataFrame([x for x in temp_df['CRI. IMC X IDADE'].values if x != -1]+[x for x in temp_df['ADO. IMC X IDADE'].values if x != -1]).mean()[0]

    color = None

    mode = int(mode)

    if mode == 1: color = "#fde8b8"
    if mode == 2: color = "#f5db97"
    if mode == 3: color = "#d9df93"
    if mode == 4: color = "#8fc57e"
    if mode == 5: color = "#f28c83"
    if mode == 6: color = "#fa6164"

    cidade = argv[2]
    if(mode == None):
        cidade = geobr.read_municipality(code_muni=m, year=2010)
        cidade.plot(facecolor="#808080", edgecolor="#FEBF57", ax=ax)
    else:
        cidade = geobr.read_municipality(code_muni=m, year=2010)
        cidade.plot(facecolor=color, edgecolor="#FEBF57", ax=ax)

    ax.set_title(f"Municípios de {argv[1]}")
    ax.axis("off")

fig.get_figure().savefig(f'./matplotimages/{argv[1]}.png', bbox_inches='tight')

print('Tempo total:', int((time()-tempo_inicial)/60), 'minutos e', int(time()-tempo_inicial)%60, 'segundos.')

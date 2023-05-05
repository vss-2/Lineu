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

pd_df = pd.DataFrame([])

with open('./df.pickle', 'rb') as handle:
    try:
        pd_df = pickle.load(handle)
    except ModuleNotFoundError:
        pd_df = pd.read_pickle(handle)

tempo_inicial = time()
faixa = {'value': 'Crianças e adultos'}

filtro = None
if(faixa['value'] == 'Criança'):
  filtro = 'CRI. IMC X IDADE'
elif(faixa['value'] == 'Adulto'):
  filtro = 'ADO. IMC X IDADE'
elif(faixa['value'] == 'Crianças e adultos'):
  filtro = '*'

muni = [2600054, 2600104, 2600203, 2600302, 2600401, 2600500,
2600609, 2600708, 2600807, 2600906, 2601003, 2601052,
2601102, 2601201, 2601300, 2601409, 2601508, 2601607,
2601706, 2601805, 2601904, 2602001, 2602100, 2602209,
2602308, 2602407, 2602506, 2602605, 2602704, 2602803,
2602902, 2603009, 2603108, 2603207, 2603306, 2603405,
2603454, 2603504, 2603603, 2603702, 2603801, 2603900,
2603926, 2604007, 2604106, 2604155, 2604205, 2604304,
2604403, 2604502, 2604601, 2604700, 2604809, 2604908,
2605004, 2605103, 2605152, 2605202, 2605301, 2605400,
2605459, 2605509, 2605608, 2605707, 2605806, 2605905,
2606002, 2606101, 2606200, 2606309, 2606408, 2606507,
2606606, 2606705, 2606804, 2606903, 2607000, 2607109,
2607208, 2607307, 2607406, 2607505, 2607604, 2607653,
2607703, 2607752, 2607802, 2607901, 2607950, 2608008,
2608057, 2608107, 2608206, 2608255, 2608305, 2608404,
2608453, 2608503, 2608602, 2608701, 2608750, 2608800,
2608909, 2609006, 2609105, 2609154, 2609204, 2609303,
2609402, 2609501, 2609600, 2609709, 2609808, 2609907,
2610004, 2610103, 2610202, 2610301, 2610400, 2610509,
2610608, 2610707, 2610806, 2610905, 2611002, 2611101,
2611200, 2611309, 2611408, 2611507, 2611533, 2611606,
2611705, 2611804, 2611903, 2612000, 2612109, 2612208,
2612307, 2612406, 2612455, 2612471, 2612505, 2612554,
2612604, 2612703, 2612802, 2612901, 2613008, 2613107,
2613206, 2613305, 2613404, 2613503, 2613602, 2613701,
2613800, 2613909, 2614006, 2614105, 2614204, 2614303,
2614402, 2614501, 2614600, 2614709, 2614808, 2614857,
2615003, 2615102, 2615201, 2615300, 2615409, 2615508,
2615607, 2615706, 2615805, 2615904, 2616001, 2616100,
2616183, 2616209, 2616308, 2616407, 2616506 ]

fig, ax = plt.subplots(figsize=(10, 10), dpi=50)
estado = geobr.read_state(code_state='PE', year=2010)
estado.plot(facecolor="#2D3E50", edgecolor="#FEBF57", ax=ax, cmap="Blues_r")

pd_df = pd_df[pd_df['SG_UF'] == 'PE']
# mode = pd.DataFrame([x for x in pd_df['CRI. IMC X IDADE'].values if x != -1]+[x for x in pd_df['ADO. IMC X IDADE'].values if x != -1]).mode()[0].values[0]

for m in muni:
    # Como destacar uma cidade
    temp_df = pd_df[pd_df['CO_MUNICIPIO_IBGE'] == int(str(m)[:-1])]
    #mode = pd.DataFrame([x for x in temp_df['CRI. IMC X IDADE'].values if x != -1]+[x for x in temp_df['ADO. IMC X IDADE'].values if x != -1]).mode()[0].values[0]
    mode = pd.DataFrame([x for x in temp_df['CRI. IMC X IDADE'].values if x != -1]+[x for x in temp_df['ADO. IMC X IDADE'].values if x != -1]).mean()[0]

    #print(mode.mean()[0])

    color = None
    # if mode == 1: color = "#fde8b8"
    # if mode == 2: color = "#f5db97"
    # if mode == 3: color = "#d9df93"
    # if mode == 4: color = "#8fc57e"
    # if mode == 5: color = "#f28c83"
    # if mode == 6: color = "#fa6164"

    if int(mode) == 1: color = "#fde8b8"
    if int(mode) == 2: color = "#f5db97"
    if int(mode) == 3: color = "#d9df93"
    if int(mode) == 4: color = "#8fc57e"
    if int(mode) == 5: color = "#f28c83"
    if int(mode) == 6: color = "#fa6164"

    cidade = None
    if(mode == None):
        cidade = geobr.read_municipality(code_muni=m, year=2010)
        cidade.plot(facecolor="#808080", edgecolor="#FEBF57", ax=ax)
    else:
        cidade = geobr.read_municipality(code_muni=m, year=2010)
        cidade.plot(facecolor=color, edgecolor="#FEBF57", ax=ax)

    ax.set_title(f"Município de Pernambuco")
    ax.axis("off")

fig.get_figure().savefig('./pernambuco.png', bbox_inches='tight')

print('Tempo total:', int((time()-tempo_inicial)/60), 'minutos e', int(time()-tempo_inicial)%60, 'segundos.')

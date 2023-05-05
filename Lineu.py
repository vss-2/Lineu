from flask import Flask, request, send_file, render_template, jsonify
from time import sleep, time
from queue import Queue
import pandas as pd
import threading
import pickle
from geobr import read_municipality, read_municipal_seat
from os import path
import uuid
import sys
import subprocess
from os.path import exists, realpath
import json
import base64

sys.setrecursionlimit(1024)

# Init global variables
queue = Queue()
max_threads = 2
threads = [None]*max_threads
outputs = [None]*max_threads
images  = [None]*max_threads
user_execution = {}
pd_df = None

start_time = time()

def read_csvs(pd_df: pd.DataFrame) -> pd.DataFrame:
    altura_idade = {
        -1: -1,
        0: 0,
        None: 0,
        'Muito baixa estatura para idade': 1,
        'Baixa estatura para idade': 2,
        'Estatura adequada para a idade': 3,
    }

    imc_idade = {
        -1: -1,
        0: 0,
        None: 0,
        'Magreza acentuada': 1,
        'Magreza': 2,
        'Eutrofia': 3,
        'Risco de sobrepeso': 4,
        'Sobrepeso': 5,
        'Obesidade': 6
    }

    raca_cor = {
        '01': 1, '02': 2, '03': 3, '04': 4, '05': 5, 'X': 0, '99': 99, 
        0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 99: 99, None: 0, -1: -1
    }
    pd_df = pd.read_csv(realpath('./')+'/xaa', encoding='latin-1', sep=';')

    pd_df.drop(['CO_ACOMPANHAMENTO', 'CO_PESSOA_SISVAN', 'ST_PARTICIPA_ANDI', 
                'NO_MUNICIPIO', 'DS_FASE_VIDA', 'DS_RACA_COR',
                'PESO X IDADE', 'PESO X ALTURA', 'CO_SISTEMA_ORIGEM_ACOMP', 
                'SISTEMA_ORIGEM_ACOMP', 'NU_COMPETENCIA', 
                'DS_ESCOLARIDADE', 'DS_POVO_COMUNIDADE'], axis=1, inplace=True)
    pd_df['NU_PESO'] = pd_df['NU_PESO'].apply(lambda x: float(x.replace(',', '.')) if isinstance(x, str) else -1)
    pd_df['NU_ALTURA'] = pd_df['NU_ALTURA'].apply(lambda x: float(x.replace(',', '.')) if isinstance(x, str) else -1)
    pd_df['DS_IMC'] = pd_df['DS_IMC'].apply(lambda x: float(x.replace(',', '.')) if isinstance(x, str) else -1)
    pd_df['DS_IMC_PRE_GESTACIONAL'] = pd_df['DS_IMC_PRE_GESTACIONAL'].apply(lambda x: int(float(x.replace(',', '.'))*100) if isinstance(x, str) else -1)
    pd_df['SG_SEXO'] = pd_df['SG_SEXO'].apply(lambda x: False if x=='F' else True)
    pd_df['SG_SEXO'] = pd_df['SG_SEXO'].astype('bool')
    pd_df['CO_CNES'] = pd_df['CO_CNES'].astype('category')
    pd_df['DT_ACOMPANHAMENTO'] =  pd.to_datetime(pd_df['DT_ACOMPANHAMENTO'], format='%d/%m/%Y')
    pd_df['NU_PESO'] = pd_df['NU_PESO'].astype('float16')
    pd_df['NU_ALTURA'] = pd_df['NU_ALTURA'].astype('float16')
    pd_df['DS_IMC'] = pd_df['DS_IMC'].astype('float16')
    pd_df['DS_IMC_PRE_GESTACIONAL'] = pd_df['DS_IMC_PRE_GESTACIONAL'].astype('int16')
    pd_df['CO_POVO_COMUNIDADE'] = pd_df['CO_POVO_COMUNIDADE'].astype('category')
    pd_df['CO_ESCOLARIDADE'] = pd_df['CO_ESCOLARIDADE'].astype('category')
    pd_df['CRI. ALTURA X IDADE'].fillna(-1, inplace=True)
    pd_df['CRI. ALTURA X IDADE'] = pd_df['CRI. ALTURA X IDADE'].apply(lambda x: altura_idade[x]).astype('int8')
    pd_df['ADO. ALTURA X IDADE'].fillna(-1, inplace=True)
    pd_df['ADO. ALTURA X IDADE'] = pd_df['ADO. ALTURA X IDADE'].apply(lambda x: altura_idade[x]).astype('int8')
    pd_df['CRI. IMC X IDADE'].fillna(-1, inplace=True)
    pd_df['CRI. IMC X IDADE'] = pd_df['CRI. IMC X IDADE'].apply(lambda x: imc_idade[x]).astype('int8')
    pd_df['ADO. IMC X IDADE'].fillna(-1, inplace=True)
    pd_df['ADO. IMC X IDADE'] = pd_df['ADO. IMC X IDADE'].apply(lambda x: imc_idade[x]).astype('int8')
    pd_df['CO_ESTADO_NUTRI_ADULTO'] = pd_df['CO_ESTADO_NUTRI_ADULTO'].astype('category')
    pd_df['CO_ESTADO_NUTRI_IDOSO'] = pd_df['CO_ESTADO_NUTRI_IDOSO'].astype('category')
    pd_df['CO_ESTADO_NUTRI_IMC_SEMGEST'] = pd_df['CO_ESTADO_NUTRI_IMC_SEMGEST'].astype('category')
    pd_df['NU_FASE_VIDA'] = pd_df['NU_FASE_VIDA'].astype('category')
    pd_df['CO_RACA_COR'].fillna(-1, inplace=True)
    pd_df['CO_RACA_COR'] = pd_df['CO_RACA_COR'].apply(lambda x: raca_cor[x]).astype('int8')
    pd_df['NU_IDADE_ANO'].fillna(-1, inplace=True)
    pd_df['NU_IDADE_ANO'] = pd_df['NU_IDADE_ANO'].apply(lambda x: -1 if x == None else x)
    pd_df['NU_IDADE_ANO'] = pd_df['NU_IDADE_ANO'].astype('int8')
    pd_df['SG_UF'] = pd_df['SG_UF'].astype('category')

    count = 0
    
    required_files = ['xab', 'xac', 'xad', 'xae', 'xaf', 'xag', 'xah', 'xai', 'xaj', 'xak', 'xal', 'xam', 'xan', 'xao']
    if(not all([exists(realpath('./')+'/'+f) for f in required_files])):
        print("ERROR: some files are missing, try running: python3 setup.py")
        exit()

    for splitted_file in required_files:
        temp_pd_df = pd.read_csv(realpath('.')+'/'+splitted_file, 
                                sep=';', encoding='latin-1')
        temp_pd_df.drop(['CO_ACOMPANHAMENTO', 'CO_PESSOA_SISVAN', 'ST_PARTICIPA_ANDI', 
                    'NO_MUNICIPIO', 'DS_FASE_VIDA', 'DS_RACA_COR',
                    'PESO X IDADE', 'PESO X ALTURA', 'CO_SISTEMA_ORIGEM_ACOMP', 
                    'SISTEMA_ORIGEM_ACOMP', 'NU_COMPETENCIA', 
                    'DS_ESCOLARIDADE', 'DS_POVO_COMUNIDADE'], axis=1, inplace=True)
        temp_pd_df['NU_PESO'] = temp_pd_df['NU_PESO'].apply(lambda x: float(x.replace(',', '.')) if isinstance(x, str) else -1)
        temp_pd_df['NU_ALTURA'] = temp_pd_df['NU_ALTURA'].apply(lambda x: float(x.replace(',', '.')) if isinstance(x, str) else -1)
        temp_pd_df['DS_IMC'] = temp_pd_df['DS_IMC'].apply(lambda x: float(x.replace(',', '.')) if isinstance(x, str) else -1)
        temp_pd_df['DS_IMC_PRE_GESTACIONAL'] = temp_pd_df['DS_IMC_PRE_GESTACIONAL'].apply(lambda x: int(float(x.replace(',', '.'))*100) if isinstance(x, str) else -1)
        temp_pd_df['SG_SEXO'] = temp_pd_df['SG_SEXO'].apply(lambda x: False if x=='F' else True)
        temp_pd_df['SG_SEXO'] = temp_pd_df['SG_SEXO'].astype('bool')
        temp_pd_df['CO_CNES'] = temp_pd_df['CO_CNES'].astype('category')
        temp_pd_df['DT_ACOMPANHAMENTO'] =  pd.to_datetime(pd_df['DT_ACOMPANHAMENTO'], format='%d/%m/%Y')
        temp_pd_df['NU_PESO'] = temp_pd_df['NU_PESO'].astype('float16')
        temp_pd_df['NU_ALTURA'] = temp_pd_df['NU_ALTURA'].astype('float16')
        temp_pd_df['DS_IMC'] = temp_pd_df['DS_IMC'].astype('float16')
        temp_pd_df['DS_IMC_PRE_GESTACIONAL'] = temp_pd_df['DS_IMC_PRE_GESTACIONAL'].astype('int16')
        temp_pd_df['CO_POVO_COMUNIDADE'] = temp_pd_df['CO_POVO_COMUNIDADE'].astype('category')
        temp_pd_df['CO_ESCOLARIDADE'] = temp_pd_df['CO_ESCOLARIDADE'].astype('category')
        temp_pd_df['CRI. ALTURA X IDADE'].fillna(-1, inplace=True)
        temp_pd_df['CRI. ALTURA X IDADE'] = temp_pd_df['CRI. ALTURA X IDADE'].apply(lambda x: altura_idade[x]).astype('int8')
        temp_pd_df['ADO. ALTURA X IDADE'].fillna(-1, inplace=True)
        temp_pd_df['ADO. ALTURA X IDADE'] = temp_pd_df['ADO. ALTURA X IDADE'].apply(lambda x: altura_idade[x]).astype('int8')
        temp_pd_df['CRI. IMC X IDADE'].fillna(-1, inplace=True)
        temp_pd_df['CRI. IMC X IDADE'] = temp_pd_df['CRI. IMC X IDADE'].apply(lambda x: imc_idade[x]).astype('int8')
        temp_pd_df['ADO. IMC X IDADE'].fillna(-1, inplace=True)
        temp_pd_df['ADO. IMC X IDADE'] = temp_pd_df['ADO. IMC X IDADE'].apply(lambda x: imc_idade[x]).astype('int8')
        temp_pd_df['CO_ESTADO_NUTRI_ADULTO'] = temp_pd_df['CO_ESTADO_NUTRI_ADULTO'].astype('category')
        temp_pd_df['CO_ESTADO_NUTRI_IDOSO'] = temp_pd_df['CO_ESTADO_NUTRI_IDOSO'].astype('category')
        temp_pd_df['CO_ESTADO_NUTRI_IMC_SEMGEST'] = temp_pd_df['CO_ESTADO_NUTRI_IMC_SEMGEST'].astype('category')
        temp_pd_df['NU_FASE_VIDA'] = temp_pd_df['NU_FASE_VIDA'].astype('category')
        temp_pd_df['CO_RACA_COR'].fillna(-1, inplace=True)
        temp_pd_df['CO_RACA_COR'] = temp_pd_df['CO_RACA_COR'].apply(lambda x: raca_cor[x]).astype('int8')
        temp_pd_df['NU_IDADE_ANO'].fillna(-1, inplace=True)
        temp_pd_df['NU_IDADE_ANO'] =  temp_pd_df['NU_IDADE_ANO'].apply(lambda x: -1 if x == None else x)
        temp_pd_df['NU_IDADE_ANO'] =  temp_pd_df['NU_IDADE_ANO'].astype('int8')
        temp_pd_df['SG_UF'] = temp_pd_df['SG_UF'].astype('category')
        pd_df = pd.concat([pd_df, temp_pd_df], copy=False, ignore_index=True)
        del temp_pd_df
        count += 1
        print(count,'/ 14')

    with open('./df.pickle', 'wb') as handle:
        pickle.dump(pd_df, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return pd_df


if path.exists('./df.pickle'):
    with open('./df.pickle', 'rb') as handle:
        try:
            pd_df = pickle.load(handle)
        except ModuleNotFoundError:
            pd_df = pd.read_pickle(handle)
else:
    pd_df = read_csvs(pd_df)

def create_selectors() -> None:
    estado_cidade = {}
    for val in read_municipal_seat().values:
        if(not val[3] in estado_cidade):
            estado_cidade.update({val[3]: []})
        else:
            if '.' in str(val[0]):
                val[0] = str(val[0])[:str(val[0]).index('.')]
            estado_cidade[val[3]].append({val[1]: str(val[0])})
    with open('estado_cidade_codigo.json', 'w') as f:
        json.dump(estado_cidade, f)

if not path.exists('./estado_cidade_codigo.json'):
    create_selectors()

end_time = time()
time_taken = end_time - start_time
print("Time taken to start cached pandas: {:.2f} seconds".format(time_taken))

def thread_filter(filters: dict, id_thread: int, queue: Queue) -> dict:
    # Using global variables
    global pd_df
    global outputs
    global images

    pd_copy = None
    pd_copy = pd_df.copy(deep=True)
    outputs[id_thread-1] = pd_copy

    print('filters:', filters, 'columns', pd_copy.columns)

    # print('len', len(pd_copy))

    # If Brasil is selected, do not apply state filter
    if(filters['state'] != 'BR' and filters['state'] != ''):
        pd_copy = pd_copy[pd_copy['SG_UF'] == filters['state']]
        print('1')
    # print('len', len(pd_copy))
    if(filters['city'] != ''):
        pd_copy = pd_copy[pd_copy['CO_MUNICIPIO_IBGE'] == int(filters['city'][:-1])]
        print('2')
    # print('len', len(pd_copy))


    # Weight range filter
    if(filters['minWeight']):
        pd_copy = pd_copy[pd_copy['NU_PESO'] > filters['minWeight']]
        print('3')
    if(filters['maxWeight']):
        pd_copy = pd_copy[pd_copy['NU_PESO'] < filters['maxWeight']]
        print('4')

    # print(pd_copy['NU_PESO'].values.tolist())
    # pd_copy['NU_PESO'] = pd_copy['NU_PESO'].dropna()
    pd_copy['NU_PESO'] = pd_copy['NU_PESO'].astype('float32')

    # Height range filter
    if(filters['minHeight']):
        pd_copy = pd_copy[pd_copy['NU_ALTURA'] > filters['minHeight']]
        print('5')
    if(filters['maxHeight']):
        pd_copy = pd_copy[pd_copy['NU_ALTURA'] < filters['maxHeight']]
        print('6')

    # pd_copy['NU_ALTURA'] = pd_copy['NU_ALTURA'].dropna()

    # Date range filter
    if(filters['minDate']):
        pd_copy = pd_copy[pd_copy['DT_ACOMPANHAMENTO'] > filters['minDate']]
        print('7')
    if(filters['maxDate']):
        pd_copy = pd_copy[pd_copy['DT_ACOMPANHAMENTO'] < filters['maxDate']]
        print('8')

    # print('len', len(pd_copy))

    # Age range filter
    if(filters['minAge']):
        print('9')
        pd_copy = pd_copy[pd_copy['NU_IDADE_ANO'] > filters['minAge']]
    if(filters['maxAge']):
        print('10')
        pd_copy = pd_copy[pd_copy['NU_IDADE_ANO'] < filters['maxAge']]

    pd_copy['DS_IMC'] = pd_copy['DS_IMC'].astype('int32')

    # IMC range filter
    if(filters['minIMC']):
        print('11')
        pd_copy = pd_copy[pd_copy['DS_IMC'] > filters['minIMC']]
    if(filters['maxIMC']):
        print('12')
        pd_copy = pd_copy[pd_copy['DS_IMC'] < filters['maxIMC']]

    # CNES filter
    if(filters['CNES']):
        print('13')
        pd_copy = pd_copy[pd_copy['CO_CNES'] == filters['CNES']]

    # School level filter
    if(filters['education']):
        print('14')
        pd_copy = pd_copy[pd_copy['CO_ESCOLARIDADE'] == filters['education']]

    # Genre filter
    if(filters['genre']):
        genre = filters['genre']
        if genre != 'Ambos': 
            print('15')
            if genre == 'Masculino':
                pd_copy = pd_copy[pd_copy['SG_SEXO'] == True]
            else:
                pd_copy = pd_copy[pd_copy['SG_SEXO'] == False]

    # Color/race
    if(filters['etnicity']):
        print('16')
        pd_copy = pd_copy[pd_copy['CO_RACA_COR'] == filters['genre']]

    if(filters['community']):
        print('17')
        pd_copy = pd_copy[pd_copy['CO_POVO_COMUNIDADE'] == filters['community']]

    # if(filters['group']):
    #     group = filters['group']
    #     if group != 'Todos': 
    #         if group == 'Criança':
    #             pd_copy = pd_copy[pd_copy['SG_SEXO'] == 1]
    #         elif group == 'Adulto':
    #             pd_copy = pd_copy[pd_copy['SG_SEXO'] == 0]
    #         else:
    #             # Idoso

    cidade = None
    try:
        cidade = read_municipality(code_muni=int(filters['city']), year=2010)
    except:
       images[id_thread-1] = 'undefined muni'
       if(cidade != None):
            print('dei except')
            return {'msg': 'error: undefined muni'}

    # print('len', len(pd_copy))

    image_uuid = uuid.uuid4().__str__()
    images[id_thread-1] = image_uuid
    queue.put(cidade)

    # print('new file at', realpath('.')+'/matplotimages/'+str(images[id_thread-1]))
    if(filters['state'] == 'BR'):
        with open(realpath('.')+'/matplotimages/'+str(images[id_thread-1]), 'wb') as imagefile:
            pickle.dump(pd_copy, imagefile)
        subprocess.run(["python3", f"{realpath('.')}/national_map.py", str(image_uuid)])
        return {'msg': 'success'}

    with open(realpath('.')+'/matplotimages/'+str(images[id_thread-1]), 'wb') as imagefile:
        pickle.dump(cidade, imagefile)
    
    # Outside with because it will run faster than the file is closed
    subprocess.run(["python3", f"{realpath('.')}/image_builder.py", 'cidade', str(image_uuid)])
    
    with open(realpath('.')+'/citiesjsons/'+str(images[id_thread-1]) + '.json', 'w') as jsonfile:
        # json.dump(pd_copy.describe().to_json(), jsonfile)
        # print(pd_copy.describe())
        # print(pd_copy['NU_PESO'].describe())
        jsonfile.write(pd_copy.describe().to_json())
    
    with open(realpath('.')+'/citiesjsons/'+str(images[id_thread-1]) + 'CNES.json', 'w') as jsonfile:
        jsonfile.write(pd_copy['CO_CNES'].value_counts().to_json())
    
    return {'msg': 'success'}


app = Flask('Lineu')
@app.route('/data', methods=['POST'])
def get_slash():
    while(all(threads)):
        print('Waiting while all threads are busy:', threads)
        sleep(0.2)

    id_thread = -1
    
    # Find first not None in threads array
    for i, thr in enumerate(threads):
        if thr == None:
            id_thread = i
            print('New thread in:', i)
            break

    if id_thread == -1:
        return 'System is unavailable'

    # Verify if request.json is a valid format (only asks a state or city)
    t = threading.Thread(target=thread_filter, args=(request.json, id_thread, queue))
    threads.append(t)

    t.start()
    t.join()
    # output = outputs[id_thread-1]

    if(images[id_thread-1] == 'undefined muni'):
        return 'Undefined Municipality'

    # Free threads and outputs
    outputs[id_thread-1] = None
    threads[id_thread-1] = None

    # print(images)
    while(not exists(realpath('.')+'/matplotimages/'+images[id_thread-1]+'.png')):
        print('to dormindo')
        sleep(1)

    # Probably there's a better way to transfer a file to buffer without using PIL    
    # img = Image.open('./'+images[id_thread-1]+'.png')
    # buffer = io.BytesIO()
    # img.save(buffer, 'png')
    # buffer.seek(0)
    # data = buffer.read()
    # data = base64.b64encode(data).decode()
    data = None
    with open(realpath('.')+'/matplotimages/'+ images[id_thread-1] + '.png', 'rb') as f:
        data = f.read()

    data = base64.b64encode(data).decode()

    json_data = None
    if(exists(realpath('.')+'/citiesjsons/'+ images[id_thread-1] + '.json')):
        with open(realpath('.')+'/citiesjsons/'+ images[id_thread-1] + '.json', 'r') as j:
            json_data = j.read()
    
    cnes_data = None
    if(exists(realpath('.')+'/citiesjsons/'+ images[id_thread-1] + 'CNES.json')):
        with open(realpath('.')+'/citiesjsons/'+ images[id_thread-1] + 'CNES.json', 'r') as j:
            cnes_data = j.read()

    response = jsonify({'msg': 'success', 'format': 'png', 'data': json_data, 'image': data, 'cnes': cnes_data})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    # return send_file(f'{images[id_thread-1]}.png', mimetype='image/png')
    return f"<img src='data:application/html;base64,'/>"
    return render_template('oi.html')

@app.route('/municipalities', methods=['GET'])
def get_municipalities():
    response = send_file('estado_cidade_codigo.json', mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/frontend/scripts.js', methods=['GET'])
def scripts():
    return send_file('./frontend/scripts.js', mimetype='application/json')

@app.route('/frontend/static/Lineu.png', methods=['GET'])
def lineu_logo():
    return send_file('./frontend/static/Lineu.png', mimetype='image/png')


# @app.route('/frontend/static/<path:path>')
# def serve_static(path):
#     return send_from_directory('static', path)

# Adicionar HOST e PORT vindos do .env
app.run()
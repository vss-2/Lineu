from zipfile import ZipFile
from os import mkdir
from os.path import realpath, exists
import requests
from subprocess import run
from time import sleep
from colorama import Fore, Style


def check_if_has_dataset() -> bool:

    if not exists(realpath('.')+'/'+'matplotimages'):
        mkdir(realpath('.')+'/'+'matplotimages')

    if exists(realpath('.')+'/'+'df.pickle'):
        return True

    # One of these two files should exist
    if(not (exists(realpath('.')+'/'+'sisvan_estado_nutricional_2021.zip') or
        exists(realpath('.')+'/'+'sisvan_estado_nutricional.zip'))):

            response = input(Fore.YELLOW + 'AVISO: Se você está vendo isso: não foi \
                    identificado arquivo sisvan_estado_nutricional.zip, \
                    ou arquivo processado .pickle na pasta. \
                    Mova o arquivo para esta pasta e execute novamente \"python3 Lineu.py\" ou \
                    pressione 1 para baixar o arquivo: sisvan_estado_nutricional_2021.zip' + Style.RESET_ALL)

            if(response == '1'):
                url = 'https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SISVAN/estado_nutricional/sisvan_estado_nutricional_2021.zip'
                filename = 'sisvan_estado_nutricional.zip'

                with requests.get(url, stream=True) as r:
                    r.raise_for_status()
                    with open(filename, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)

                with ZipFile('sisvan_estado_nutricional.zip', 'r') as zip_ref:
                    for year in ['2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008']:
                        try:
                            zip_ref.extract(f'sisvan_estado_nutricional_{year}.csv', str(realpath('.')))
                        except:
                            continue
                        break

                run(['bash', './splitter.sh'])
                print('Descompactando e fragmentando arquivos. Isso vai demorar mais que dois minuto!')
                sleep(30)

                stop = False
                while(stop):
                    for f in ['xaa', 'xab', 'xac', 'xad', 'xae', 'xaf', 'xag', 'xah', 'xai', 'xaj', 'xak', 'xal', 'xam', 'xan', 'xao']:
                        if(not exists(realpath('.')+'/'+f)):
                            sleep(5)
                            stop = True
                        else:
                            stop = False

                return True
            else:
                return False
    return True

check_if_has_dataset()

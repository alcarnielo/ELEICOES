"""
This function intents to:
1 - manage the Brazilian election databak 
"""
import os
from zipfile import ZipFile

import pandas as pd

from functions.read_buletin import read_buletin_file
from functions.write_db_data import manage_db
from functions.db_tables import tables

def db_update(user, passord, database, fl_base_path, year):
    map_keys = {
        'DS_TIPO_VOTAVEL':{
            '1': 'Nominal',
            '2': 'Branco',
            '3': 'Nulo',
            '4': 'Legenda',
        },
        'NM_VOTAVEL':{
            '95': 'Branco',
            '96': 'Nulo',
            '97': ' anulado e apurado em separado',
            '98':'anulado',
        }
    }



    # list all files for the given year:    
    zip_fl_list = os.listdir(os.path.join(fl_base_path, f'{year}'))
    for zip_fl in zip_fl_list:
        data = None
        fl_path = os.path.join(fl_base_path, f'{year}', zip_fl)
        print(year, zip_fl)

        if year == 2016:
            imposed_keys = [
                'DT_GERACAO','HH_GERACAO','CD_PLEITO','CD_TIPO_ELEICAO','SG_UF','CD_CARGO_PERGUNTA',
                'DS_CARGO_PERGUNTA','NR_ZONA','NR_SECAO','NR_LOCAL_VOTACAO','NR_PARTIDO',
                'NM_PARTIDO','CD_MUNICIPIO','NM_MUNICIPIO','DT_BU_RECEBIDO','QT_APTOS',
                'QT_ABSTENCOES','QT_COMPARECIMENTO','CD_ELEICAO','CD_TIPO_URNA','DS_TIPO_URNA',
                'NR_VOTAVEL','NM_VOTAVEL','QT_VOTOS','CD_TIPO_VOTAVEL','NR_URNA_EFETIVADA',
                'CD_CARGA_1_URNA_EFETIVADA','CD_CARGA_2_URNA_EFETIVADA','DT_CARGA_URNA_EFETIVADA',
                'CD_FLASHCARD_URNA_EFETIVADA',
                '_'
            ]
            get_keys = False

        else:
            get_keys = True



        # read file and apply corrections according to the file year
        sep=";";
        data_to_register = pd.DataFrame()
            # data_to_return = {}
        with ZipFile(fl_path, 'r') as zfl:
            for zname in zfl.namelist():
                data=None
                # Modify only csv files
                if zname.endswith('.csv') or zname.endswith('.txt'):
                    with zfl.open(zname) as zcsv:
                        for i, line in enumerate(zcsv):
                            
                            if i == 0:
                                if get_keys == True:
                                    # extract the keys from the file first line
                                    keys = line.decode('ISO-8859-1').strip().replace('"','').split(f'{sep}')
                                    
                                else:
                                    keys = imposed_keys
                                    vals = line.decode('ISO-8859-1').strip().replace('"','').split(f'{sep}')
                                    data = dict(zip(keys,vals))
                    
                            else:
                                # extract the values from the lines
                                vals = line.decode('ISO-8859-1').strip().replace('"','').split(f'{sep}')
                            
                                # ensemble a dictionary with all keys and values from the read line
                                data = dict(zip(keys,vals))

                            if data:
                                # complment year data dict
                                if year==2016:
                                # filling missing columns to register in the databank
                                    data['ANO_ELEICAO'] = 2016
                                    data['SG_PARTIDO'] = data['NM_PARTIDO'] 
                                    
                                    data['DS_TIPO_VOTAVEL'] = map_keys['DS_TIPO_VOTAVEL'][data['CD_TIPO_VOTAVEL']] 
                                    data['DT_ABERTURA'] = 'NONE' 
                                    data['DT_ENCERRAMENTO'] = 'NONE'
                                    data['QT_ELEI_BIOM_SEM_HABILITACAO'] = 'NONE'
                                    data['DT_EMISSAO_BU'] = 'NONE'
                                    
                                    if '_1t_' in zip_fl:
                                        data['DT_PLEITO'] = '02/10/2024'
                                        data['NR_TURNO'] = '1'

                                    elif '_2t_' in zip_fl:
                                        data['DT_PLEITO'] = '30/10/2024'
                                        data['NR_TURNO'] = '2'


                                # appending data
                                data_to_register = pd.concat([data_to_register, pd.DataFrame(data.values(), data.keys()).T],ignore_index=True)

                            if data_to_register.shape[0] >= 10000:
                                manage_db(user, passord, database, tables, data_to_register)
                                data_to_register = pd.DataFrame()
            
            # registering the last lines from the data into the DB
            manage_db(user, passord, database, tables, data)
            

if __name__ == '__main__':
    years = [
        2024, 2022, 2020, 2018, #2016,
              ]

    # user information
    usr='test_user'
    pwd='sua_senha'
    db_name = 'ballot_box'

    # file informaton
    base_path = '/home/alvaro/Documentos/estudos_python/eleicoes/data'
    for year in years:
        print('# ---------------------------------------------------------------------- #')
        db_update(usr, pwd, db_name, base_path, year)


    
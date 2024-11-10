#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 10:25:21 2024

@author: alvaro

    This function reads the Brazilian ballot box bulletin and prepare 
it to be registered in a databank


"""

from zipfile import ZipFile
import requests
import io

# zipfl = "https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2024/buweb/bweb_1t_AC_091020241636.zip"


def read_buletin_file(
        zipfl: str, 
        # keys_to_return: list
        ):
    '''
    This function reads the zipped file containing the ballot box bulletin,
and returns a dictionary containing all the selected keys to be exported.

    INPUT:
    -----
        zipfl : str
            Ballot box bulletin zip file path

        # keys_to_return : list
        #     List containing the dictionary keys to be exported
    '''
    data_to_return = {
        # key:[] for key in keys_to_return
        }
    # # Download online file to be processed
    # zipfl = read_online_file(zipfl)
    # access the ffiles
    with ZipFile(zipfl, 'r') as zfl:
        for zname in zfl.namelist():
            # Modify only csv files
            if zname.endswith('.csv'):
                with zfl.open(zname) as zcsv:
                    for i, line in enumerate(zcsv):
                        
                        if i == 0:
                            # extract the keys from the file first line
                            keys = line.decode('ISO-8859-1').strip().replace('"','').split(';')
                
                        else:
                            # extract the values from the lines
                            vals = line.decode('ISO-8859-1').strip().replace('"','').split(';')
                        
                            # ensemble a dictionary with all keys and values from the read line
                            line_dict = dict(zip(keys, vals))
                        
                            for key in keys:
                                # if key in keys_to_return:
                                #     data_to_return[key].append(line_dict[key])
                                if key not in data_to_return:
                                    data_to_return[key] = []
                                data_to_return[key].append(line_dict[key])
    return data_to_return

def read_online_file(link):
    # access file
    response = requests.get(link)

    if response == 200:
        # save file in the memory
        zip_file = io.BytesIO(response.content)
        return zip_file

    else:
        print("Download failed")
    


if __name__ == '__main__':
    zipfl = '/home/alvaro/Documentos/estudos_python/eleicoes/data/2024/bweb_1t_AC_091020241636.zip'
    data_to_return = read_buletin_file(zipfl, keys_to_return)
    print(
        len(data_to_return.keys()),
        len(data_to_return.values())
    )
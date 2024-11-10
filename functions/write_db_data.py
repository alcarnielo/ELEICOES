#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 06:25:00 2024

@author: alvaro
# ---------------------------------------------------------------------- #
    This code manages the creation an manipulation of a databank that
contains the registered votes from the ballot box bulletins from the
Brazilian elections

# ---------------------------------------------------------------------- #
Version control:
version     Date            Notes
/           2024-11-2       -...
                                -
                                -
                            - ...
                                -

1.0 
"""
import pymysql
import pandas as pd

from db_tables import tables
from read_boletim import read_buletin_file

def db_connection(user, password, db_name):
    connection=None
    try:
        connection = pymysql.connect(
            host='localhost',
            user=user,
            password=password,
            database=db_name,
            # auth_plugin='mysql_native_password'
        )
        print('successfully connected')

        # Create cursor to db
        
        return connection

    except pymysql.connect.Error as err:
        print(f'Error: {err}')
        return None


def db_table_creator(cursor, table_name, cols):
    tables_structure = ''.join(
                            [f"    {key} {val},\n" 
                                for (key, val) in cols.items()]
                            )
    query = f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        {tables_structure[:-2]}
        );
    '''
    print(query)
    cursor.execute(query)


def write_data_to_db(cursor, tables, data):

    df_data = pd.DataFrame.from_dict(data, orient='columns')
    # adding new composite columns
    df_data['ID_local_votacao'] = df_data['NR_ZONA']+df_data['NR_SECAO']+df_data['NR_LOCAL_VOTACAO']
    df_data['ID_candidato'] = df_data['CD_MUNICIPIO']+df_data['NR_VOTAVEL']
    for table_name in tables.keys():
        # select only tables within the table
        cols = list(tables[table_name].keys())
        filtered_df_data = df_data[cols].drop_duplicates()
        cols_string = ', '.join(cols)
#         vals_string = ''
#         for i in range(filtered_df_data.shape[0]):
#             vals_line=', '.join([f'"{var}"' 
#                                     if not var.replace('.', '', 1).isdigit() 
#                                     else var 
#                                     for var in filtered_df_data.iloc[i].values])
#             vals_string+=f'({vals_line}), \n\t'

#         query = f'''
# INSERT IGNORE INTO {table_name} ({cols_string})
#     VALUES 
#         {vals_string[:-4]};
#     '''
#         cursor.execute(query)
        vals_placeholder = ', '.join(['%s'] * len(cols))
        query = f'''
        INSERT IGNORE INTO {table_name} ({cols_string})
        VALUES ({vals_placeholder});
        '''
        data_to_insert = [tuple(row) for row in filtered_df_data.to_numpy()]
        cursor.executemany(query, data_to_insert)
        


def manage_db(
        user, password, db_name,    # db connection inputs
        tables,                     # tables to be managed
        data,                       # data to be insert into the db
):
    # creating a DBconnect
    conn = db_connection(user=user, password=password, db_name=db_name)
    if conn is None:
        print("Failed to connec to database")
        return
    
    # creating cursor
    cursor = conn.cursor()

    try:
        # creating tables if not exists
        for table_name in tables.keys():
            cols = tables[table_name]
            db_table_creator(cursor, table_name, cols)


        # zriting data into the db
        write_data_to_db(cursor, tables, data)

        # commit changes:
        conn.commit()
        print("Data commited to database")
    
    except Exception as err:
        print(f'Error: {err}')
        conn.rollback()
    
    finally:
        # closing db connection
        cursor.close()
        conn.close()


if __name__ == '__main__':
    # user information
    usr='test_user'
    pwd='sua_senha'
    db_name = 'ballot_box'
    # connection=None

    # file informaton
    zipfl = '/home/alvaro/Documentos/estudos_python/eleicoes/data/2024/bweb_1t_AC_091020241636.zip'
    data = read_buletin_file(zipfl)

    # managing db
    manage_db(usr, pwd, db_name, tables, data)
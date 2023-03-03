import pandas as pd
from typing import List
from collections import defaultdict
import json
import requests
import glob
from CONFIG import config_csv as cf

def obtener_token ():

    url = "http://127.0.0.1:8000/user/signing"

    payload='username=feyamil95%40globant.com.ar&password=12345'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST", url, headers=headers, data=payload)
    datos = response.json()
    return datos["access_token"] 

def enviar_csv (payload,endpoint,contador):
    token = obtener_token()
    url = f"http://127.0.0.1:8000/{endpoint}"
    token = f"Bearer {token}"
    with open(endpoint + str(contador) + ".json", 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=4)
    payload = json.dumps(payload)
    headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    contador = 0
    print(response.content)





def crear_diccionario (valores_dataframe,nombre_archivo):

    diccionario_principal = {"items": list()}
    
    if nombre_archivo != "empleados.csv":
        for valor in valores_dataframe:
            diccionario_aux = {}
            diccionario_aux[cf[nombre_archivo]["columna_1"]] = valor[0]
            diccionario_aux[cf[nombre_archivo]["columna_2"]] = valor[1]
            diccionario_principal["items"].append(diccionario_aux)
    else :
            
        for valor in valores_dataframe:

            diccionario_aux = {}
            diccionario_aux[cf[nombre_archivo]["columna_1"]] = valor[0]
            diccionario_aux[cf[nombre_archivo]["columna_2"]] = valor[1]
            diccionario_aux[cf[nombre_archivo]["columna_3"]] = valor[2]
            diccionario_aux[cf[nombre_archivo]["columna_4"]] = valor[3]
            diccionario_aux[cf[nombre_archivo]["columna_5"]] = valor[4]
            diccionario_principal["items"].append(diccionario_aux)


    return diccionario_principal


def read_csv ():
    
    archivos_csv = glob.glob('**/*.csv', recursive=True)
    
    for archivo in archivos_csv:
        with pd.read_csv(archivo, chunksize=1000,header=None,dtype=str) as reader:
            contador = 0
            for chunk in reader:
                #nombre_archivo = archivo.split("\\")[1]
                endpoint = archivo.split(".")[0]
                payload = crear_diccionario(chunk.values,archivo)
                enviar_csv(payload,endpoint,contador) 
            contador = 0
        
           
        

if __name__ == '__main__':

    read_csv()

#Altera o access tier dos backups físicos e lógicos com mais de 30 dias

#Imports
import pytz
import os
import json
from pytz import timezone
from datetime import datetime, timedelta
from azure.storage.blob import ContainerClient

abs_path = os.path.dirname(__file__)

with open(abs_path + '\\enviroment.json') as file:
    variables = json.load(file)

#Declaração do container_client que acessa o container bkporacle dentro do tjadisco
container_client = ContainerClient.from_connection_string(variables['connStr'], container_name="bkporacle")

#Constrói a data de 30 dias atrás
date_thirty_days_before = datetime.now(pytz.utc).astimezone(timezone("America/Sao_Paulo")) - timedelta(days=30)

#Recupera a lista de backups com data anterior a 30 dias
blobs_list = list(filter(lambda item: item['creation_time'].astimezone(timezone("America/Sao_Paulo")) < date_thirty_days_before and item['blob_tier'] == 'Hot', container_client.list_blobs()))
print("Quantidade de blobs que serão modificados: ", len(blobs_list))

if(len(blobs_list) == 0):
    print("Não existem blobs a serem modificados.")
else:
    try:
        for blob in blobs_list:
            container_client.set_standard_blob_tier_blobs("Cool", blob)
        print("Access tier dos blobs modificados com sucesso.")
    except:
        print("Ocorreu um erro ao modificar o access tier dos blobs")
        blobs_list = list(filter(lambda item: item['creation_time'].astimezone(timezone("America/Sao_Paulo")) < date_thirty_days_before and item['blob_tier'] == 'Hot', container_client.list_blobs()))
        print("Quantidade de blobs não modificados: ", len(blobs_list))
        
# Imports
import os
import json
from azure.storage.blob import ContainerClient
from datetime import datetime,timedelta
from pytz import timezone

# Pega as datas necessárias para a retenção dos arquivos, convertendo para Local
today_date = datetime.now(timezone("America/Sao_Paulo"))

retention_date = today_date - timedelta(days=5)

abs_path = os.path.dirname(__file__)

with open(abs_path + '\\enviroment.json') as file:
    variables = json.load(file)

# Declaração do container_client que acessa o container
container_client = ContainerClient.from_connection_string(variables['connStr'], container_name="backupoci")

# Recupera a lista com os backups com data superior a 5 dias
backup_list = list(filter(lambda item: (item['creation_time'].astimezone(timezone("America/Sao_Paulo")) < retention_date), container_client.list_blobs(name_starts_with="BACKUP")))

backup_list_senior = list()
# Deleta todos os arquivos de backup listados, menos os da pasta SENIOR
for backup in backup_list:
    if('BASES' in backup['name']):
        print(backup['name'])
        # Retirar o comentário desta linha para colocar em produção
        #container_client.delete_blob(backup)
    else:
        backup_list_senior.append(backup)

if(len(backup_list_senior) > 1):
    # Define a key ao qual será ordenada a lista
    def get_key(obj):
        return obj['creation_time'].astimezone(timezone("America/Sao_Paulo"))

    # Ordena a lista de backups para que seja possível pegar o último backup realizado
    backup_list_senior.sort(reverse=True, key=get_key)

    for backup in backup_list_senior:
        if(backup != backup_list_senior[0]):
            print(backup['name'])
            # Retirar o comentário desta linha para colocar em produção
            #container_client.delete_blob(backup)

import json
import os
from azure.storage.blob import BlobServiceClient

abs_path = os.path.dirname(__file__)

with open(abs_path + '\\enviroment.json') as file:
    variables = json.load(file)

blob_service_client = BlobServiceClient.from_connection_string(variables['connStr'])

containers = blob_service_client.list_containers()
for container in containers:
    container_client = blob_service_client.get_container_client(container.name)
    blobs_list = container_client.list_blobs()
    container_size = 0
    for blob in blobs_list:
        blob_client = blob_service_client.get_blob_client(container=container.name, blob=blob.name)
        blob_properties = blob_client.get_blob_properties()
        container_size += blob_properties.size
    print("{}: {} Gb".format(container.name, container_size/1024/1024/1024))

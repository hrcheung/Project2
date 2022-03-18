from azure.cosmos import exceptions,CosmosClient, PartitionKey

url= "https://hrcheung.documents.azure.com:443/"
key="noWg0r6jaCs6ukqGgUuwQIhTB9F2zr5oHEn5AqHsLtndtAqIPYqJvSHH2drQqM2suqGpXHyq370aatVuxnmS2Q=="

#create client
client=CosmosClient(url,key)

#create database
database_name='GroceriesInSJ'
database=client.create_database_if_not_exists(id=database_name)

#create container

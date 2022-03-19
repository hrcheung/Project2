from azure.cosmos import exceptions,CosmosClient, PartitionKey
import grocery
url= "https://hrcheung.documents.azure.com:443/"
key="noWg0r6jaCs6ukqGgUuwQIhTB9F2zr5oHEn5AqHsLtndtAqIPYqJvSHH2drQqM2suqGpXHyq370aatVuxnmS2Q=="

#create client
client=CosmosClient(url,key)

#create database

database_name='GroceryDatabase'
try:
    database=client.create_database(id=database_name)
except exceptions.CosmosResourceExistsError:
    database=client.get_database_client(database_name)
    print('database already exists')

#create container
container_name='GroceryContainer'
try:
    container=database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/zipcode"), #we use zip code to do partition
        offer_throughput=400
    )
except exceptions.CosmosResourceExistsError:
    print('container already exists')

#CREATE: create & add 4 items to container.
safeway=grocery.get_grocery_item('1','safeway','95133','san jose',True)
wholefoods=grocery.get_grocery_item('2','wholefoods','95112','san jose',True)
sprouts=grocery.get_grocery_item('3','sprouts','95133','san jose',False)
tradejoe=grocery.get_grocery_item('4','tradejoe','95126','santa clara',False)
grocery_item_to_add=[safeway,wholefoods,sprouts,tradejoe]

for i in range(4):
    try:
        container.create_item(body=grocery_item_to_add[i])
    except exceptions.CosmosResourceExistsError:
        print('item already exists')

#READ: key-value search
for grocery_item in grocery_item_to_add:
    item_response=container.read_item(item=grocery_item['id'],partition_key=grocery_item['zipcode'])
    request_cost=container.client_connection.last_response_headers['x-ms-request-charge']
    print('read item {0}. This costs {1} request units'.format(item_response['id'],(request_cost)))


#QUERY with SQL API ; it can also be done through platform Explorer Query
query="SELECT * FROM container where container.zipcode = '95133'"
items=list(container.query_items(
    query=query,
    enable_cross_partition_query=True
))

request_cost=container.client_connection.last_response_headers['x-ms-request-charge']

print('selects {0} items and costs {1} RU'.format(len(items),request_cost))

#UPSERT items with upsert_item SDK
for grocery_item in grocery_item_to_add:
    read_item=container.read_item(item=grocery_item['id'],partition_key=grocery_item['zipcode'])
    read_item['zipcode']="94007"
    item_response=container.upsert_item(body=read_item)

    print('Upsert item id is {0} and new zipcode = {1}'.format(read_item['id'],read_item['zipcode']))

#DELETE items with delete_item SDK
grocery_item=grocery_item_to_add[0]
try:
    item_deleted = container.delete_item(item=grocery_item['id'],partition_key=grocery_item['zipcode'])
    print('DELETE item id is 1')
except: #if exception
    print('item not exists')

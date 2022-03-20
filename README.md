# Project2

## Learning resources

I refer to [CosmosDB document](https://docs.microsoft.com/en-us/azure/cosmos-db) by Microsoft Azure. 

## Prerequisites
1. Register for Azure CosmosDB account
2. Install Python on laptop
3. Pip install Cosmos PyPi, azure-cosmos and related packages
4. Import grocery.py (created by myself) to facilitate item creation

## CosmosDB NoSQL Database Structure

from high level to low level, the structure of above concepts are as below:

                CosmosDB Account
                        ⬇️
                     Database
                        ⬇️
                     Container
                        ⬇️
                       Item
                       

## Perform CRUD in Item 

### 1.Create: 

> Use SDK to create item
```Python
container.create_item(body=grocery_item_to_add[i])
```

<img width="573" alt="image" src="https://user-images.githubusercontent.com/40035441/159138731-bf66bff0-76c6-4d92-8768-84604832c8d7.png">


### 2.Read & Query / SELECT

> Use SDK to Read item. 
```Python
for grocery_item in grocery_item_to_add:
    item_response=container.read_item(item=grocery_item['id'],partition_key=grocery_item['zipcode'])
    request_cost=container.client_connection.last_response_headers['x-ms-request-charge']
    print('read item {0}. This costs {1} request units'.format(item_response['id'],(request_cost)))

```

>Use SQL API to do query. 
>
```Python
query="SELECT * FROM container where container.zipcode = '95133'"
items=list(container.query_items(
    query=query,
    enable_cross_partition_query=True
))

request_cost=container.client_connection.last_response_headers['x-ms-request-charge']

print('selects {0} items and costs {1} RU'.format(len(items),request_cost))
```

> We can also use CLI to check costs (RU).
<img width="517" alt="image" src="https://user-images.githubusercontent.com/40035441/159138046-96007f14-4e16-4da3-aa42-90cb1e1b97df.png">

> SELECT query can also be performed on Azure CosomosDB Platform which also monitors cost.

<img width="329" alt="image" src="https://user-images.githubusercontent.com/40035441/159139017-02dedfd1-f6a9-4452-a822-be4d1d1f0670.png">

<img width="994" alt="image" src="https://user-images.githubusercontent.com/40035441/159139056-93c35b98-e12f-4dba-a40b-fa96fb3c666a.png">


### 3.Update
> Use SDK to update item. 
> If item exists, update; else insert
> Note: watch out for the replace_item SDK, which prompts exception if not exists

```Python
for grocery_item in grocery_item_to_add:
    read_item=container.read_item(item=grocery_item['id'],partition_key=grocery_item['zipcode'])
    read_item['zipcode']="94007"
    item_response=container.upsert_item(body=read_item)

    print('Update item id is {0} and new zipcode = {1}'.format(grocery_item['id'],grocery_item['zipcode']))
```
<img width="393" alt="image" src="https://user-images.githubusercontent.com/40035441/159139912-5c47f667-08b8-4000-8ea0-2d67dd3e7ebb.png">
<img width="401" alt="image" src="https://user-images.githubusercontent.com/40035441/159140378-d759bbf0-c820-4d7f-8624-8eb756576a28.png">

### 4.Delete
> use SDK to delete certain item. 

```Python
grocery_item=grocery_item_to_add[0]
try:
    item_deleted = container.delete_item(item=grocery_item['id'],partition_key=grocery_item['zipcode'])
    print('DELETE item id is 1')
except: #if exception
    print('item not exists')

```

<img width="346" alt="image" src="https://user-images.githubusercontent.com/40035441/159139885-c3c5b293-cfb0-455b-9f06-6df4ab99a5d1.png">



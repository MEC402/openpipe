import json
import requests
import sys
sys.path.append('c:/Users/Kenny/source/repos/openpipe/backend/')

from openpipeAPI.ORM.BL import BL

#collection id = 39 name = Test
#asset id = 4979 name = Test
#asset id = 4980 name = Test2
#asset id = 4981 name = Test3

#image id = 3403 name = Test
#image id = 3404 name = Test2
#image id = 3405 name = Test3

#metadata id 5065
#metadata id 5066
#metadata id 5067

#collectionMember id = 4981
#collectionMember id = 4982
#collectionMember id = 4983

#collection id = 39


results = BL().getCollections()



collections = {
    "records":[

    ]
}

fd = {
    "fields": {
        'CollectionName': "",
        'CollectionMembers': []
    }
}
count = 0
for result in results['data']:
    print(result['name'][0])
    print(result['uri'][0])

    if result['name'][0] == fd['fields']['CollectionName'] :
        fd['fields']['CollectionMembers'].append({
            "url" : result['uri'][0]
        })
    else:
        if count == 0:
            count += 1
        else:
            collections['records'].append(fd)

        fd = {
            "fields": {
                'CollectionName': result['name'][0],
                'CollectionMembers': []
            }
        }
        fd['fields']['CollectionMembers'].append({
            "url": result['uri'][0]
        })
collections['records'].append(fd)
print(collections)
data = json.dumps(collections)



headers = {'Content-type': 'application/json'}
post_url = 'https://api.airtable.com/v0/appeMt0ZuU1mUWGSv/Collections?api_key=keyIsqsd4CZprRaAX'
response = requests.post(post_url,data=data, headers=headers)
print(response)

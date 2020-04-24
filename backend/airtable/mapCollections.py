import json
import requests
import sys
sys.path.append('c:/Users/Kenny/source/repos/openpipe/backend/')

from ORM.BL import BL

results = BL().getAllImages()


images = {
    "records":[

    ]
}

for result in results['data']:
    filename = result['filename']
    uri = result['uri']

    images["records"].append({"fields": {
        "Name": filename[0],
        "URL":[{
            "url": uri[0]
        }]
    }})

data = json.dumps(images)

print()
print(data)
print()

headers = {'Content-type': 'application/json'}
post_url = 'https://api.airtable.com/v0/appeMt0ZuU1mUWGSv/Images?api_key=keyIsqsd4CZprRaAX'
response = requests.post(post_url,data=data, headers=headers)
print(response)

import re

from ORM.BL import BL
from ORM.ORM import ORM
from oracles.Oracle import Oracle


def getGISInfo():
    orm = ORM()
    results = orm.executeSelect("""SELECT 
    a.id, a.metaDataId, tagName, value
FROM
    (SELECT 
        *
    FROM
        asset
    WHERE
        metaDataId IN (SELECT 
                metaDataId
            FROM
                metaTag
            WHERE
                (tagName = 'openpipe_canonical_nation'
                    OR tagName = 'openpipe_canonical_culture'
                    OR tagName = 'openpipe_canonical_city')
                    AND value <> ''
                    AND value <> 'OpenPipe City'
                    AND value <> 'OpenPipe Culture')
    GROUP BY asset.id) AS a
        JOIN
    metaTag ON a.metaDataId = metaTag.metaDataId
WHERE
    tagname = 'openpipe_canonical_culture'
        OR tagname = 'openpipe_canonical_city'
        OR tagname = 'openpipe_canonical_nation'""")
    print(results['data'])
    i=0
    ids={-1}
    for asset in results['data']:
        print(i)
        i=i+1
        if asset['tagName'][0] == 'openpipe_canonical_nation' \
                or asset['tagName'][0] == 'openpipe_canonical_city' \
                or asset['tagName'][0] == 'openpipe_canonical_culture':
            if asset['value'][0] != '' \
                    and 'openpipe' not in asset['value'][0] \
                    and 'OpenPipe' not in asset['value'][0]\
                    and asset['id'][0] not in ids and asset['id'][0]>288:
                ids.add(asset['id'][0])
                val = asset['value'][0]
                print(asset['id'])
                location = re.split(' |, ', val)
                temp=[]
                for l in location:
                    if not re.search(r'\d', l) \
                            and l != 'century' \
                            and l != 'dynasty' \
                            and l != 'painting' \
                            and l != 'possibly' \
                            and l != 'probably' \
                            and l != 'late' \
                            and l != 'period'\
                            and l != 'Period' \
                            and l != '(painting)' \
                            and l != '(carving);' \
                            and l != 'Upper' \
                            and l != 'North' \
                            and l != 'Southern' \
                            and l != 'or' \
                            and l != 'the' \
                            and l != 'Northeastern' \
                            and l != 'Southern'\
                            and l != 'Northern' \
                            and l!= 'early'\
                            and l!= 'and'\
                            and l!= 'Western'\
                            and l!= 'school'\
                            and l!= "Century"\
                            and l!= 'periods':
                            temp.append(l)
                location=[]
                if len(temp)>0:
                    location.append(temp[0])
                    location.append(temp[-1])
                res=Oracle().getLocationInfo(location[-1],'',location[0])
                lon=0
                lat=0
                for r in res:
                    if location[-1] in r['name'] or location[0] in r['name']:
                        lat=r['coordinates']['latitude']['decimal']
                        lon=r['coordinates']['longitude']['decimal']
                        break
                BL().insertIntoMetaTags({'metaDataId':asset['metaDataId'][0],
                                         'openpipe_canonical_latitude':lat,
                                         'openpipe_canonical_longitude':lon})


getGISInfo()

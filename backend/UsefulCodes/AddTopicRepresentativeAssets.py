import re

from sqlalchemy import and_

from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

orm = ORM()
tables = TO().getClasses()
Topic = tables["topic"]

assetResultSet = orm.executeSelect(
    """select * from asset join
(SELECT metadataId as mid,topic_id as tid FROM artmaster.metaTag where topic_code!='b00' group by topic_id) as a on asset.metaDataId=a.mid;""")


mappings=[]

for d in assetResultSet['data']:
    # print(d)
    info = {'id': d['tid'][0], "repAssetId": d['id'][0]}
    mappings.append(info)

print(mappings)

updateSize=len(mappings)
biteSize=1000
q=int(updateSize / biteSize)
r= updateSize % biteSize

for i in range(0,q):
    print("************** commiting to DB **************")
    orm.session.bulk_update_mappings(Topic, mappings[i*biteSize:i*biteSize+biteSize])
    orm.session.flush()
    orm.session.commit()
    print("************** Done commiting to DB **************")
orm.session.bulk_update_mappings(Topic,mappings[q*biteSize:q*biteSize+r])
orm.commitClose()
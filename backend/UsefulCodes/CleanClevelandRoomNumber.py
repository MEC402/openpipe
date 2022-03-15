import re

from sqlalchemy import and_

from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

orm = ORM()
tables = TO().getClasses()
Topic = tables["metaTag"]

assetResultSet = orm.executeSelect(
    """select * from metaTag where tagName='openpipe_canonical_genre' and value!='' and metaDataId in (select metaDataId from metaTag where tagName='openpipe_canonical_source' and value='Cleveland Museum of Art');""")


mappings=[]

for d in assetResultSet['data']:
    value=d['value'][0]
    value = re.sub(r'(^\d+\s+|^\d+[a-zA-Z]*\s+)','', value)
    print(d['id'][0],d['value'][0],value)
    info = {'id': d['id'][0], "value": value}
    mappings.append(info)

print(mappings)

updateSize=len(mappings)
biteSize=1000
q=int(updateSize / biteSize)
r= updateSize % biteSize

# for i in range(0,q):
#     print("************** commiting to DB **************")
#     orm.session.bulk_update_mappings(Topic, mappings[i*biteSize:i*biteSize+biteSize])
#     orm.session.flush()
#     orm.session.commit()
#     print("************** Done commiting to DB **************")
# orm.session.bulk_update_mappings(Topic,mappings[q*biteSize:q*biteSize+r])
# orm.commitClose()
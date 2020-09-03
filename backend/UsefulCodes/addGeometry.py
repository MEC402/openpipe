import json

from openpipeAPI.ORM.BL import BL
from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO

orm=ORM()
tables = TO().getClasses()
collectionMember = tables["collectionMember"]
res=orm.executeSelect("""SELECT * FROM artmaster.collectionMember order by collectionId;""")

foldernum=0
i=0
j=0
wall=0
wallstr=""
for r in res['data']:
    if r["collectionId"][0]>foldernum:
        foldernum=r["collectionId"][0]
        print(r["collectionId"])
        i = 0
        j = 0
        wall = 0
    else:
        if i<20:
            i+=1
        else:
            i=0
            if j<20:
                j+=1
            else:
                j=0
        if i==20 and j==20:
            wall+=1

    if wall==0:
        wallstr="right"
    elif wall==1:
        wallstr="center"
    else:
        wallstr="left"

    x=100*j
    y=100*i
    pos="100 x 100 + "+str(x)+" + "+str(y)

    orm.session.query(collectionMember).filter(collectionMember.id == int(r['id'][0])).update({"geometry": pos,"wall":wallstr})
orm.commitClose()



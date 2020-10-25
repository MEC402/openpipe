from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO

orm =ORM()
tables = TO().getClasses()
MetaTag = tables["metaTag"]
res =orm.executeSelect("""SELECT * FROM artmaster.metaTag where tagName like 'Latitude%' or tagName like 'Longitude%';""")
i=0
j=0
for r in res['data']:
    print(r["id"][0])
    if(r["tagName"][0].lower().strip()=="latitude"):
        i+=1
        orm.session.query(MetaTag).filter(MetaTag.id == int(r['id'][0])).update(
            {"tagName": "openpipe_canonical_latitude"})
    if (r["tagName"][0].lower().strip() == "longitude"):
        j+=1
        orm.session.query(MetaTag).filter(MetaTag.id == int(r['id'][0])).update(
            {"tagName": "openpipe_canonical_longitude"})

print(i,j,i+j)
orm.commitClose()

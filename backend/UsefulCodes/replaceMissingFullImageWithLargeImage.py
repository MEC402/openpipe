from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

orm = ORM()
tables = TO().getClasses()
MetaTags = tables["metaTag"]

stm = """select f.id as fid, f.metaDataId, f.tagname as ftag, f.value as fv,l.id as lid, l.tagname as ltag, l.value as lv,  from
(select id,metaDataId,tagname,value from metaTag where tagName="openpipe_canonical_fullImage") as f
join (select id,metaDataId,tagname,value from metaTag where tagName="openpipe_canonical_largeImage") as l
on f.metaDataId=l.metaDataId
where f.value not like '%mec402%';"""


tagResultSet = orm.executeSelect(stm)

for ta in tagResultSet["data"]:
    print(ta)
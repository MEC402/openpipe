from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

orm = ORM()
tables = TO().getClasses()
MetaTag = tables["metaTag"]
MetaData = tables["metaData"]

mappings = []

assetMetaDataList = orm.session.query(MetaTag).filter(MetaTag.tagName == "openpipe_canonical_date")
for amd in assetMetaDataList:
    id = amd.id
    mid = amd.metaDataId
    value = str(amd.value).split(" ")
    if len(value) != 5:
        print(id,value,"Bad format")
        mappings.append({"id":id,"value":None,"note":"bad date"})
    else:
        if not value[1].isnumeric():
            print(id, value, "Bad Year")
            mappings.append({"id": id, "value": None, "note": "bad date"})

# updateSize=len(mappings)
# biteSize=1000
# q=int(updateSize / biteSize)
# r= updateSize % biteSize
#
# for i in range(0,q):
#     print("************** commiting to DB **************")
#     orm.session.bulk_update_mappings(MetaTag, mappings[i*biteSize:i*biteSize+biteSize])
#     orm.session.flush()
#     orm.session.commit()
#     print("************** Done commiting to DB **************")
# orm.session.bulk_update_mappings(MetaTag,mappings[q*biteSize:q*biteSize+r])
# orm.commitClose()
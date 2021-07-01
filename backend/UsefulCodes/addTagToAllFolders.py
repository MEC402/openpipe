import json
import time

from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.Schema import AssetSchema, MetaTagSchema, FolderSchema
from openpipeAPI.ORM.TO import TO

batched_data = []
orm = ORM()
tables = TO().getClasses()
FolderTable = tables["collection"]
MetaTagTable = tables["metaTag"]


foldersResultSet=orm.session.query(FolderTable).all()
for folder in foldersResultSet:
    print(folder.metaDataId)
    print(folder.image)
    orm.insert(MetaTagTable(metaDataId=folder.metaDataId, tagName="FolderImage", value=folder.image))

orm.commitClose()
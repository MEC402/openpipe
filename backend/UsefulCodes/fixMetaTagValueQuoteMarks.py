import re

from sqlalchemy import and_

from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

orm = ORM()
tables = TO().getClasses()
MetaTag = tables["metaTag"]


resultSet = orm.executeSelect(
    """SELECT * FROM artmaster.metaTag where value like '\"%\"';""")

for tag in resultSet["data"]:
    print(tag)
    ct= re.sub(r"\"", "", str(tag["value"][0]))
    orm.session.query(MetaTag).filter(MetaTag.id == tag["id"][0]).update({"value": ct})


orm.commitClose()





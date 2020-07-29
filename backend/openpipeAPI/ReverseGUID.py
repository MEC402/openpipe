from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO

tables = TO().getClasses()
orm = ORM()
data=orm.executeSelect("select a.id,artist_tags.topic_id from (SELECT * FROM artmaster.metaTag where tagName='openpipe_canonical_artist') as a join artist_tags on a.value=artist_tags.value")
MetaTag = tables["metaTag"]
for d in data["data"]:
    orm.session.query(MetaTag).filter(MetaTag.id == int(d["id"][0])).update({"topic_name": "artist", "topic_id": int(d["topic_id"][0])})
orm.commitClose()

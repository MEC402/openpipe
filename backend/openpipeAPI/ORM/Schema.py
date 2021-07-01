from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from openpipeAPI.ORM.TO import TO


class AssetSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TO().getClasses()["asset"]
        include_relationships = True
        load_instance = True


class FolderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TO().getClasses()["collection"]
        include_relationships = True
        load_instance = True


class MetaTagSchema():
    def manyToJson(self, data):
        res = {}
        for d in data:
            res[d.tagName] = {
                "id": d.id,
                "value": d.value,
                "verified": d.verified,
                "topic_name": d.topic_name,
                "topic_code": d.topic_code,
                "topic_id": d.topic_id,
                "note": d.note,
                "timestamp": d.timestamp,
                "insertTime": d.insertTime,
                "lastModified": d.lastModified,
                "status": d.status
            }
        return res

    def toJson(self, d):
        res = {}
        res[d.tagName] = {
            "id": d.id,
            "value": d.value,
            "verified": d.verified,
            "topic_name": d.topic_name,
            "topic_code": d.topic_code,
            "topic_id": d.topic_id,
            "note": d.note,
            # "timestamp": d.timestamp,
            # "insertTime": d.insertTime,
            # "lastModified": d.lastModified,
            "status": d.status
        }
        return res

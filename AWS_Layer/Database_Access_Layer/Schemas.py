from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from TO import TO


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
    def toJson(self, data):
        res = {}
        for d in data:
            res[d.tagName] = {
                "id": d.id,
                "value": d.value,
                "verified": d.verified,
            }
        return res


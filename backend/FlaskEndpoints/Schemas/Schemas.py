from flask_marshmallow import Schema
from flask_marshmallow.fields import Hyperlinks, URLFor


class AssetSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "shortName", "uri", "IdAtSource", "sourceId", "metaDataId", "type", "scope", "verified", "GUIDs")

    # Smart hyperlinking
    GUIDs = Hyperlinks(
        {
            "self": URLFor("asset", values=dict(id="<id>"), _external=True),
            "collection": URLFor("assets"),
        }
    )

class FolderSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "image", "layoutType", "metaDataId", "verified", "note", "insertTime", "lastModified", "GUIDs")

    # Smart hyperlinking
    GUIDs = Hyperlinks(
        {
            "self": URLFor("folder", values=dict(id="<id>"), _external=True),
            "collection": URLFor("folders"),
        }
    )

class FolderContentSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "assetId", "collectionId", "searchTerm", "metaDataId", "geometry", "wall", "GUIDs")

    # Smart hyperlinking
    GUIDs = Hyperlinks(
        {
            "self": URLFor("asset", values=dict(id="<assetId>"), _external=True),
        }
    )


class MetaTagSchema():
    # class Meta:
    #     # Fields to expose
    #     fields = (
    #         "id", "metaDataId", "tagName", "value", "topic_name", "topic_id", "verified", "note", "lastModified",
    #         "_links")

    def toJson(self, data):
        res = {}
        for d in data:
            res[d.tagName] = {
                "id": d.id,
                "value": d.value,
                "verified": d.verified,
            }
        return res

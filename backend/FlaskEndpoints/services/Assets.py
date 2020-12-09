from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm import load_only

from FlaskEndpoints.Schemas.Schemas import MetaTagSchema, AssetSchema
from openpipeAPI.ORM.BL import BL

# AllAssets_request_parser = RequestParser(bundle_errors=True)
# AllAssets_request_parser.add_argument("p", type=int, required=False, default=1)
# AllAssets_request_parser.add_argument("ps", type=int, required=False, default=10)
# AllAssets_request_parser.add_argument("changeStart", type=str, required=False, default='1900-01-01')
# AllAssets_request_parser.add_argument("changeEnd", type=str, required=False, default='5000-01-01')
from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO


class Assets(Resource):
    def get(self):
        AssetTable = TO().getClasses()["asset"]
        orm = ORM()
        assets = orm.session.query(AssetTable).all()
        assets_schema = AssetSchema(many=True)
        response = {"total": len(assets), "data": assets_schema.dump(assets)}
        print(response)
        return response


class Asset(Resource):
    def get(self, id):
        Tables = TO().getClasses()
        AssetTable = Tables["asset"]
        MetaTagTable = Tables["metaTag"]
        orm = ORM()
        asset_schema = AssetSchema()
        metaTag_schema = MetaTagSchema()
        folderInfo = asset_schema.dump(orm.session.query(AssetTable).filter(AssetTable.id == id).first())
        metaTagInfo = metaTag_schema.toJson(
            orm.session.query(MetaTagTable).filter(MetaTagTable.metaDataId == folderInfo["metaDataId"]).all())
        response = {"assetInfo": folderInfo, "metaTags": metaTagInfo}
        return response

    # def put(self, id):
    #     args = subscriber_request_parser.parse_args()
    #     user = get_user_by_id(id)
    #     if user:
    #         users.remove(user)
    #         users.append(args)
    #
    #     return args
    #
    # def delete(self, id):
    #     user = get_user_by_id(id)
    #     if user:
    #         users.remove(user)
    #
    #     return {"message": "Deleted"}

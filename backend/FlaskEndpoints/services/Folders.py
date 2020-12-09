from flask_restful import Resource

from FlaskEndpoints.Schemas.Schemas import FolderSchema
from FlaskEndpoints.Schemas.Schemas import MetaTagSchema
from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO


class Folders(Resource):
    def get(self):
        FolderTable = TO().getClasses()["collection"]
        orm = ORM()
        foldersInfo = orm.session.query(FolderTable).all()
        folders_schema = FolderSchema(many=True)
        response = {"total": len(foldersInfo), "data": folders_schema.dump(foldersInfo)}
        print(response)
        return response


class Folder(Resource):
    def get(self, id):
        Tables = TO().getClasses()
        FolderTable = Tables["collection"]
        MetaTagTable = Tables["metaTag"]
        orm = ORM()
        folder_schema = FolderSchema()
        metaTag_schema = MetaTagSchema()
        folderInfo = folder_schema.dump(orm.session.query(FolderTable).filter(FolderTable.id == id).first())
        metaTagInfo = metaTag_schema.toJson(
            orm.session.query(MetaTagTable).filter(MetaTagTable.metaDataId == folderInfo["metaDataId"]).all())
        response = {"folderInfo": folderInfo, "metaTags": metaTagInfo}
        return response

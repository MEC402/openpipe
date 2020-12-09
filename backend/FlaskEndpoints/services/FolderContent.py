from flask_restful import Resource

from FlaskEndpoints.Schemas.Schemas import FolderContentSchema
from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO


class FolderContent(Resource):
    def get(self, id):
        Tables = TO().getClasses()
        FolderContentTable = Tables["collectionMember"]
        orm = ORM()
        folderContent_schema = FolderContentSchema(many=True)
        folderContentInfo = folderContent_schema.dump(
            orm.session.query(FolderContentTable).filter(FolderContentTable.collectionId == id).all())
        response = {"total": len(folderContentInfo), "data": folderContentInfo}
        return response

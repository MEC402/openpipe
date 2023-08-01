from sqlalchemy import and_

from DataAccess import DataAccess as da
from TO import TO
from Schemas import AssetSchema, MetaTagSchema, FolderSchema


def getAllFolderIDs():
    results = {"total": 0, "data": []}

    tables = TO().getClasses()
    AssetTable = tables["collection"]

    session = da().getSession()
    folderIds = session.query(AssetTable.id).all()

    response = {"total": len(folderIds), "data": [fid[0] for fid in folderIds]}

    session.close()
    return response

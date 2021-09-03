import json

from sqlalchemy import and_

from DataAccess import DataAccess as da
from TO import TO
from Schemas import AssetSchema, MetaTagSchema, FolderSchema


def getAllFolderIDs():
    results = {"total": 0, "data": []}

    tables = TO().getClasses()
    FolderTable = tables["collection"]

    session = da().getSession()
    folderIds = session.query(FolderTable.id).order_by(FolderTable.name).all()

    response = {"total": len(folderIds), "data": [fid[0] for fid in folderIds]}

    session.close()
    return response


def getFolderByID(fid):
    tables = TO().getClasses()
    FolderTable = tables["collection"]

    session = da().getSession()
    folder = session.query(FolderTable).filter(FolderTable.id == fid).all()
    response = FolderSchema().dumps(folder[0])

    session.close()
    return response


def getFolders(page, pageSize):
    page = int(page)
    pageSize = int(pageSize)
    if page < 1:
        page = 1
    start = (page - 1) * pageSize
    step = pageSize

    results = {"total": 0, "data": []}

    tables = TO().getClasses()
    FolderTable = tables["collection"]

    session = da().getSession()
    rows = session.query(FolderTable).count()
    folderResultSet = session.query(FolderTable).order_by(FolderTable.name).offset(start).limit(
        step).all()

    folders = FolderSchema(many=True).dumps(folderResultSet)

    session.close()

    response = {"total": rows, "data": json.loads(folders)}

    return response
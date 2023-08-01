from sqlalchemy import and_

from DataAccess import DataAccess as da
from TO import TO
from Schemas import AssetSchema, MetaTagSchema


def getAllAssets(page, pageSize, changeStart, changeEnd):
    if (page < 1):
        page = 1
    start = (page - 1) * pageSize
    step = pageSize

    results = {"total": 0, "data": []}

    if int(page) < 0:
        return results

    tables = TO().getClasses()
    AssetTable = tables["asset"]
    MetaTagTable = tables["metaTag"]

    session = da().getSession()
    assets = session.query(AssetTable).filter(
        and_(AssetTable.lastModified >= changeStart, AssetTable.lastModified <= changeEnd)).offset(start).limit(
        step).all()

    metaTag_schema = MetaTagSchema()
    assets_schema = AssetSchema(many=True)

    response = {"total": len(assets), "data": []}
    assets = assets_schema.dump(assets)

    for asset in assets:
        metaTag = session.query(MetaTagTable).filter(MetaTagTable.metaDataId == asset["metaDataId"])
        metaTag_ser = metaTag_schema.toJson(metaTag)
        response["data"].append({**asset, **metaTag_ser})
    session.close()
    return response

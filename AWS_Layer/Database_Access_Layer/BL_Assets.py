import json
import math
import re

from sqlalchemy import and_, func
from sqlalchemy.orm import aliased

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


#
# def test(page, pageSize, changeStart, changeEnd, none):
#     stm = "select * from metaTag join (select * from asset WHERE asset.`lastModified` BETWEEN '" + changeStart + "' AND '" + changeEnd + "'LIMIT " + page + ", " + pageSize + ") as a on a.metaDataId=metaTag.metadataId where tagName like '%openpipe_canonical%';"
#
#     r = da().executeSelect(stm)
#     print(r[0])


def getFolderAssets(page, pageSize, folderId):
    tables = TO().getClasses()
    MetaTag = tables["metaTag"]
    Asset = tables["asset"]
    CollectionMember = tables["collectionMember"]

    if (page < 1):
        page = 1
    start = (page - 1) * pageSize
    step = pageSize

    results = {"total": 0, "data": []}

    if int(page) < 0:
        return results

    session = da().getSession()

    q1 = session.query(Asset.id, Asset.metaDataId, Asset.verified). \
        join(CollectionMember, Asset.id == CollectionMember.assetId). \
        filter(CollectionMember.collectionId == folderId). \
        offset(start). \
        limit(step). \
        subquery()

    resultSet = session.query(q1, MetaTag.tagName, MetaTag.value, MetaTag.id). \
        join(MetaTag, MetaTag.metaDataId == q1.c.metaDataId). \
        all()

    assetMetaDataMap = {}

    for r in resultSet:
        assetId = r[0]
        mid = r[1]
        verified = r[2]
        tagName = r[3]
        value = r[4]

        if assetId not in assetMetaDataMap:
            assetMetaDataMap[assetId] = {"assetId": assetId,
                                         "metaDataId": mid,
                                         "assetVerified": verified,
                                         tagName: value}
        else:
            assetMetaDataMap[assetId][tagName] = value

    results["data"] = list(assetMetaDataMap.values())
    results["total"] = len(results["data"])

    return results


def getFolders(page, pageSize):
    page = int(page)
    pageSize = int(pageSize)
    if page < 1:
        page = 1
    start = (page - 1) * pageSize
    step = pageSize

    tables = TO().getClasses()
    FolderTable = tables["collection"]
    CollectionMember = tables["collectionMember"]

    session = da().getSession()
    folderResultSet = session.query(FolderTable).order_by(FolderTable.name).offset(start).limit(
        step).all()

    folderAssetNum = session.query(CollectionMember.collectionId, func.count(CollectionMember.assetId)). \
        group_by(CollectionMember.collectionId). \
        order_by(CollectionMember.collectionId). \
        all()

    folderMap = {}
    resultMap = []

    for fn in folderAssetNum:
        folderMap[int(fn[0])] = fn[1]

    print(folderMap)
    print(len(folderMap.keys()))

    for folder in folderResultSet:

        if folder.id not in folderMap:
            folderMap[folder.id] = 0

        r = {"id": folder.id,
             "name": folder.name,
             "image": folder.image,
             "layoutType": folder.layoutType,
             "metaDataId": folder.metaDataId,
             "verified": folder.verified,
             "assetCount": folderMap[int(folder.id)]}
        resultMap.append(r)

    session.close()

    response = {"total": len(resultMap), "data": resultMap}

    return response


# def update_test():
#     tables = TO().getClasses()
#     MetaTag = tables["metaTag"]
#
#     session=da().session
#     session.query(MetaTag).filter(and_(MetaTag.metaDataId==4,MetaTag.tagName=='reign')).update({"value":""})
#     session.query(MetaTag).filter(and_(MetaTag.metaDataId == 4, MetaTag.tagName == 'region')).update({"value": ""})
#     session.commit()
#     session.close()


def getChangedAssets(page, pageSize, date):
    tables = TO().getClasses()
    MetaTag = tables["metaTag"]
    Asset = tables["asset"]

    if (page < 1):
        page = 1
    start = (page - 1) * pageSize
    step = pageSize

    results = {"total": 0, "data": []}

    if int(page) < 0:
        return results

    session = da().getSession()
    rows = session.query(Asset).filter(Asset.lastModified >= date).count()

    q1 = session.query(Asset.id, Asset.metaDataId, Asset.verified, Asset.score, Asset.type, Asset.lastModified). \
        filter(Asset.lastModified >= date). \
        offset(start). \
        limit(step). \
        subquery()

    resultSet = session.query(q1, MetaTag.tagName, MetaTag.value, MetaTag.id). \
        join(MetaTag, MetaTag.metaDataId == q1.c.metaDataId). \
        all()

    session.close()

    assetMetaDataMap = {}

    for r in resultSet:
        assetId = r[0]
        mid = r[1]
        verified = r[2]
        score = r[3]
        assetType = r[4]
        lastModified = r[5].strftime("%Y-%m-%d")
        tagName = r[6]
        value = r[7]

        if assetId not in assetMetaDataMap:
            assetMetaDataMap[assetId] = {"assetId": assetId,
                                         "metaDataId": mid,
                                         "assetVerified": verified,
                                         "assetScore": score,
                                         "assetType": assetType,
                                         "lastModified": lastModified,
                                         tagName: [value]}
        else:
            assetMetaDataMap[assetId][tagName] = [value]

    results["data"] = list(assetMetaDataMap.values())
    results["total"] = rows

    return results


def getAllAssetsWithGUID(page, pageSize, changeStart, changeEnd, none):
    tables = TO().getClasses()
    MetaTag = tables["metaTag"]
    Asset = tables["asset"]

    guidmap = {"city": "500", "classification": "600",
               "culture": "700", "genre": "800", "medium": "900", "nation": "a00",
               "artist": "400", "title": "000", "tags": "000"
               }
    guidURL = "http://mec402.boisestate.edu/cgi-bin/openpipe/data/"
    sguidURL = "http://mec402.boisestate.edu/"
    if (page < 1):
        page = 1
    start = (page - 1) * pageSize
    step = pageSize

    results = {"total_assets": 0,
               "assets_in_page": 0,
               "guidbase": "http://mec402.boisestate.edu/",
               "data": []}

    if int(page) < 0:
        return results

    session = da().getSession()

    rows = session.query(Asset). \
        filter(Asset.lastModified >= changeStart, Asset.lastModified <= changeEnd).count()

    q1 = session.query(Asset). \
        filter(Asset.lastModified.between(changeStart, changeEnd)). \
        offset(start). \
        limit(step). \
        subquery()

    q1 = aliased(Asset, q1)

    resultSet = session.query(q1, MetaTag).join(MetaTag, q1.metaDataId == MetaTag.metaDataId). \
        filter(MetaTag.tagName.like("%{}%".format("openpipe_canonical_"))). \
        order_by(q1.metaDataId). \
        all()

    # print(t1 - t0)

    assetMetaDataMap = {}
    # print(len(resultSet))

    for r in resultSet:
        assetInfo = r[0]
        metaTagInfo = r[1]
        # print(assetInfo.metaDataId, metaTagInfo.metaDataId)
        tagName = metaTagInfo.tagName.split("_")[2]

        tagGuid = {str(metaTagInfo.topic_code) + "/" + str(metaTagInfo.topic_id): metaTagInfo.value}
        if metaTagInfo.topic_name is None and none == 1:
            if tagName == "id":
                tagGuid = "100" + "/" + str(assetInfo.id)
            else:
                tagGuid = {"ba0" + "/" + str(metaTagInfo.id): metaTagInfo.value}

        if assetInfo.metaDataId not in assetMetaDataMap:
            assetMetaDataMap[assetInfo.metaDataId] = {"guid": "100/" + str(assetInfo.id),
                                                      "metaDataId": [assetInfo.metaDataId],
                                                      "name": [assetInfo.shortName],
                                                      "openpipe_canonical": {
                                                          tagName: tagGuid
                                                      }}
        else:
            assetMetaDataMap[assetInfo.metaDataId]["openpipe_canonical"][tagName] = tagGuid

    error_rec = ""
    final_assets=[]
    for key in assetMetaDataMap.keys():
        # try:
            can = assetMetaDataMap[key]["openpipe_canonical"]
            guid = assetMetaDataMap[key]["guid"]
            # print(can)
            # print(guid)
            res = validate_asset(can, guid)
            if len(res) > 1:
                error_rec += (",".join(res))+"\n"
            else:
                final_assets.append(assetMetaDataMap[key])
        # except:
        #     pass

    # file1 = open("badAssets.txt", "a")  # append mode
    # file1.write(error_rec)
    # file1.close()

    results["total_assets"] = rows
    results["data"] = final_assets
    results["assets_in_page"] = len(final_assets)

    return results


def get_canon_value_from_guid(canon):
    values_view = canon.values()
    value_iterator = iter(values_view)
    return next(value_iterator)


def is_Json(st):
    try:
        a_json = json.loads(st)
        return True
    except:
        return False


def validate_asset(asset, asset_id):
    # check if all canonicals tags exists
    # tables = TO().getClasses()
    # CanonicalMetaTag = tables["canonicalMetaTag"]
    # session = da().getSession()
    #
    # resultSet = session.query(CanonicalMetaTag.name).filter(CanonicalMetaTag.req == 'yes').all()
    # results = set([r.split("_")[2] for r, in resultSet])

    error_list=[asset_id]

    # results = {'medium', 'fullImageDimensions', 'subject', 'pgRating', 'physicalDimensions', 'artist', 'period',
    #            'largeImageDimensions', 'biography', 'largeImage', 'date', 'latitude', 'style', 'country', 'fullImage',
    #            'culture', 'smallImageDimensions', 'smallImage', 'longitude', 'title', 'nation'}

    results = {'medium', 'fullImageDimensions', 'pgRating', 'physicalDimensions', 'artist',
               'largeImageDimensions', 'biography', 'largeImage', 'date', 'fullImage',
               'culture', 'smallImageDimensions', 'smallImage', 'title'}

    possible_json_canon = ['medium', 'physicalDimensions', 'biography','culture']

    canon_name = set(asset.keys())

    if results.issubset(canon_name):
        # check if the canonical values are correct

        # Check date follows BC|CE YYYYYY MMM DD HH:MM:SS format
        date = get_canon_value_from_guid(asset["date"])
        if re.fullmatch(
                "^(bc|ce) ([0-9]{1,5}) (jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec) ([0-9][0-9]) ([0-9][0-9]:[0-9][0-9]:[0-9][0-9])$",
                date.lower()) is None:
            error_list.append("bad date")

        # Check image url exists
        small_img = get_canon_value_from_guid(asset["smallImage"])
        large_img = get_canon_value_from_guid(asset["largeImage"])
        full_img = get_canon_value_from_guid(asset["fullImage"])

        if small_img == '' or small_img is None:
            error_list.append("bad smallImage")
        if large_img == '' or large_img is None:
            error_list.append("bad largeImage")
        if full_img == '' or full_img is None:
            error_list.append("bad fullImage")

        # Check image dimensions follows Width,height format
        if re.fullmatch("[0-9]+,[0-9]+", get_canon_value_from_guid(asset["smallImageDimensions"])) is None:
            error_list.append("bad smallImageDimensions")
        if re.fullmatch("[0-9]+,[0-9]+", get_canon_value_from_guid(asset["largeImageDimensions"])) is None:
            error_list.append("bad largeImageDimensions")
        # if re.fullmatch("[0-9]+,[0-9]+", get_canon_value_from_guid(asset["fullImageDimensions"])) is None:
        #     error_list.append("bad fullImageDimensions")

        for pc in possible_json_canon:
            canon_var = get_canon_value_from_guid(asset[pc])
            if is_Json(canon_var):
                error_list.append(pc + " = " + canon_var + " has bad canon value contains json")

    else:
        # print(results)
        # print(canon_name)

        diff = results.difference(canon_name)
        # print(diff)
        error_list.append( "Bad canon set missing: "+str(diff))

    return error_list


page=1
pageSize=100
for page in range(1,int(11371/pageSize)+2):
    print("page: "+str(page))
    assets = getAllAssetsWithGUID(page, pageSize, '1100-01-25', '5000-01-01', 1)
    print(assets["assets_in_page"])




import json
import re

from backend.openpipeAPI.ORM.ORM import ORM as da
from backend.openpipeAPI.ORM.TO import TO
from sqlalchemy.orm import aliased


def getAllAssetsWithGUID(page, pageSize, changeStart, changeEnd, none, verify):
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
                                                          tagName: [tagGuid]
                                                      }}
        else:
            if tagName in assetMetaDataMap[assetInfo.metaDataId]["openpipe_canonical"]:
                assetMetaDataMap[assetInfo.metaDataId]["openpipe_canonical"][tagName].append(tagGuid)
            else:
                assetMetaDataMap[assetInfo.metaDataId]["openpipe_canonical"][tagName] = [tagGuid]


    final_assets = []

    if verify == 1:
        error_rec = ""
        for key in assetMetaDataMap.keys():
            can = assetMetaDataMap[key]["openpipe_canonical"]
            guid = assetMetaDataMap[key]["guid"]
            res = validate_asset(can, guid)
            if len(res) > 1:
                error_rec += (",".join(res)) + "\n"
            else:
                final_assets.append(assetMetaDataMap[key])
    else:
        final_assets = list(assetMetaDataMap.values())

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

    error_list = [asset_id]

    results = {'medium', 'fullImageDimensions', 'subject', 'pgRating', 'physicalDimensions', 'artist', 'period',
               'largeImageDimensions', 'biography', 'largeImage', 'date', 'latitude', 'style', 'country', 'fullImage',
               'culture', 'smallImageDimensions', 'smallImage', 'longitude', 'title', 'nation'}

    # results = {'medium', 'fullImageDimensions', 'pgRating', 'physicalDimensions', 'artist',
    #           'largeImageDimensions', 'biography', 'largeImage', 'date', 'fullImage',
    #           'culture', 'smallImageDimensions', 'smallImage', 'title'}

    possible_json_canon = ['medium', 'physicalDimensions', 'biography', 'culture']

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
        if re.fullmatch("[0-9]+,[0-9]+", get_canon_value_from_guid(asset["fullImageDimensions"])) is None:
            error_list.append("bad fullImageDimensions")

        for pc in possible_json_canon:
            canon_var = get_canon_value_from_guid(asset[pc])
            if is_Json(canon_var):
                error_list.append(pc + " = " + canon_var + " has bad canon value contains json")

    else:
        # print(results)
        # print(canon_name)

        diff = results.difference(canon_name)
        # print(diff)
        error_list.append("Bad canon set missing: " + str(diff))

    return error_list


def lambda_handler(event, context):
    dict = event['queryStringParameters']

    if dict is None:
        dict = {"a": "b"}

    if 'p' not in dict.keys():
        dict['p'] = 1

    if 'ps' not in dict.keys():
        dict['ps'] = 10

    if 'changeStart' not in dict.keys():
        dict['changeStart'] = '1900-01-01'

    if 'changeEnd' not in dict.keys():
        dict['changeEnd'] = '5000-01-01'

    if 'type' not in dict.keys():
        dict['type'] = 1

    if 'verify' not in dict.keys():
        dict['verify'] = 0

    data = getAllAssetsWithGUID(int(dict["p"]), int(dict["ps"]), dict['changeStart'], dict['changeEnd'],
                                int(dict['type']), int(dict['verify']))

    # encode in utf8 before sending
    # json.dumps("ברי צקלה", ensure_ascii=False).encode('utf8')

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            "Content-Type": "application/json",
        },
        "body": json.dumps(data, ensure_ascii=False).encode('utf8')
    }


a=lambda_handler({
  "queryStringParameters": {
    "pageNumber": 1,
    "pageSize": 10,
    "changeStart": "2023-06-01",
  }
},None)

print(a["body"])
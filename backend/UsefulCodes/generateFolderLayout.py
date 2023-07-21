# 2160px high.
# Total width: 21802px.
# Left/East: 7266px.
# Center/South: 6065px.
# Right/West: 8480px.
#
import math

from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO


def findNewSize(binW, binH, w, h):
    nw = 0
    nh = 0
    r = w / binW
    ph = h / r
    r = h / binH
    pw = w / r
    if ph > binH:
        nw = pw
        nh = binH
    else:
        nw = binW
        nh = ph

    return math.floor(nw), math.floor(nh)


def getAssetsInFolder(folderId):
    orm = ORM()
    stm = """SELECT a.*, tagname, value 
        FROM metaTag JOIN
        (SELECT 
            asset.metaDataId,
                assetId,
                collectionMember.id AS cmid,
                geometry,
                wall
            FROM
                asset JOIN collectionMember ON assetId = asset.id
            WHERE collectionId =:fid) AS a ON metaTag.metaDataId = a.metaDataId
        WHERE (tagName = 'openpipe_canonical_largeImage' OR tagName = 'openpipe_canonical_largeImageDimensions')
        ORDER BY metaDataId;""";
    resultSet = orm.session.execute(stm, {"fid": folderId})
    assets = {}
    for r in resultSet:
        metaDataId = r[0]
        assetId = r[1]
        cmid = r[2]
        geometry = r[3]
        wall = r[4]
        tagname = r[5]
        value = r[6]

        if assetId in assets:
            assets[assetId][tagname] = value
        else:
            assets[assetId] = {"cmid": cmid, "geometry": geometry, "wall": wall, tagname: value,
                               "metaDataId": metaDataId, "assetId": assetId}

    return assets


def generate2RowLayout(folderId):
    assets = getAssetsInFolder(folderId)
    totalAssets = len(assets.keys())

    binWidth = math.floor(21802 / (totalAssets / 2))
    binHeight = math.floor(2160 / 2)

    # print(binWidth, binHeight)
    cx = 0
    cy = 0
    nWall = "left"
    updates = []
    ba = []
    for a in assets.keys():
        if assets[a]["openpipe_canonical_largeImageDimensions"] != "":
            dim = assets[a]["openpipe_canonical_largeImageDimensions"].split(",")
            newDim = findNewSize(binWidth, binHeight, int(dim[0]), int(dim[1]))

            if 7266 < cx < 13331:
                x = cx - 7266
                nWall = "center"
            elif cx > 13331:
                x = cx - 13331
                nWall = "right"
            else:
                x = cx

            y = cy * binHeight

            if cy:
                cx += binWidth
            else:
                y = math.floor((binHeight - newDim[1]) / 2)

            cy = not cy

            # Left/East: 7266px.
            # Center/South: 6065px.
            # Right/West: 8480px.

            g = str(newDim[0]) + " x " + str(newDim[1]) + " + " + str(x) + " + " + str(y)
            updates.append({"id": assets[a]["cmid"], "geometry": g, "wall": nWall})
        else:
            ba.append(assets[a]["assetId"])
    # print(updates)
    orm = ORM()
    tables = TO().getClasses()
    CollectionMember = tables["collectionMember"]
    orm.bulkUpdate(updates, CollectionMember, 100)
    orm.session.commit()
    orm.session.close()
    print("Bad assets", ba)


def generateNRowLayout(folderId, n):
    assets = getAssetsInFolder(folderId)

    # print(assets)
    totalAssets = len(assets.keys())

    binWidth = math.floor(21802 / (totalAssets / n))
    binHeight = math.floor(2160 / n)

    # print(binWidth, binHeight)
    cx = 0
    cy = 0
    nWall = "left"
    updates = []
    ba = []

    for a in assets.keys():
        if assets[a]["openpipe_canonical_largeImageDimensions"] != "":
            dim = assets[a]["openpipe_canonical_largeImageDimensions"].split(",")
            newDim = findNewSize(binWidth, binHeight, int(dim[0]), int(dim[1]))

            if 7266 < cx < 13331:
                x = cx - 7266 + math.floor((binWidth - newDim[0]) / 2)
                nWall = "center"
            elif cx > 13331:
                x = cx - 13331 + math.floor((binWidth - newDim[0]) / 2)
                nWall = "right"
            else:
                x = cx + math.floor((binWidth - newDim[0]) / 2)

            y = cy * binHeight + math.floor((binHeight - newDim[1]) / 2)
            cy = cy + 1

            if cy == n:
                cx += binWidth
                cy = 0
            elif cy == 1:
                y = binHeight - newDim[1]


            g = str(newDim[0]) + " x " + str(newDim[1]) + " + " + str(x) + " + " + str(y)
            updates.append({"id": assets[a]["cmid"], "geometry": g, "wall": nWall})
        else:
            ba.append(assets[a]["assetId"])
    print(updates)
    orm = ORM()
    tables = TO().getClasses()
    CollectionMember = tables["collectionMember"]
    orm.bulkUpdate(updates, CollectionMember, 100)
    orm.session.commit()
    orm.session.close()
    print("Bad assets", ba)


def generateNRow(folderId, n):
    assets = getAssetsInFolder(folderId)

    # print(assets)
    totalAssets = len(assets.keys())

    binWidth = math.floor(21802 / (totalAssets / n))
    binHeight = math.floor(2160 / n)

    # print(binWidth, binHeight)
    cx = 0
    cy = 0
    nWall = "left"
    updates = []
    ba = []

    assetsList=[]
    for a in assets.keys():
        if assets[a]["openpipe_canonical_largeImageDimensions"] != "":
            dim = assets[a]["openpipe_canonical_largeImageDimensions"].split(",")
            newDim = findNewSize(binWidth, binHeight, int(dim[0]), int(dim[1]))
            assets[a]["ratio"]=int(dim[0])/ int(dim[1])
            assetsList.append(assets[a])
        else:
            ba.append(assets[a]["assetId"])

    print(assetsList)
    assetsList=sorted(assetsList,key=lambda x: x["ratio"],reverse=False)

    for assetItem in assetsList:
        if assetItem["openpipe_canonical_largeImageDimensions"] != "":
            dim = assetItem["openpipe_canonical_largeImageDimensions"].split(",")
            newDim = findNewSize(binWidth, binHeight, int(dim[0]), int(dim[1]))

            if 7266 < cx < 13331:
                x = cx - 7266 + math.floor((binWidth - newDim[0]) / 2)
                nWall = "center"
            elif cx > 13331:
                x = cx - 13331 + math.floor((binWidth - newDim[0]) / 2)
                nWall = "right"
            else:
                x = cx + math.floor((binWidth - newDim[0]) / 2)

            y = cy * binHeight + math.floor((binHeight - newDim[1]) / 2)
            cy = cy + 1

            if cy == n:
                cx += binWidth
                cy = 0
            elif cy == 1:
                y = binHeight - newDim[1]


            g = str(newDim[0]) + " x " + str(newDim[1]) + " + " + str(x) + " + " + str(y)
            updates.append({"id": assetItem["cmid"], "geometry": g, "wall": nWall})
        else:
            ba.append(assetItem["assetId"])

    print(updates)
    orm = ORM()
    tables = TO().getClasses()
    CollectionMember = tables["collectionMember"]
    orm.bulkUpdate(updates, CollectionMember, 100)
    orm.session.commit()
    orm.session.close()
    print("Bad assets", ba)

def generateLayoutForAllFolders():
    orm1 = ORM()
    badFolders = []
    ignoreFolderIds = [191, 192, 86]
    folderIds = []
    resultset = orm1.session.execute("select distinct collectionId from collectionMember order by collectionId", )
    for fid in resultset:
        if fid[0] not in ignoreFolderIds and fid[0] > 140:
            folderIds.append(fid[0])

    for f in folderIds:
        print("Generating Layout for FolderId:", f)
        try:
            generate2RowLayout(f)
        except Exception as e:
            print("Layout generation Failed", f)
            badFolders.append(f)

    print(badFolders)


# generateLayoutForAllFolders()

# generateNRowLayout(238, 2)

# generateNRow(238, 2)


# generate2RowLayout(20)

# ids = [41,59,83,84,115,120,123,140,143,148,179,182,204,205,209,213,222,228,231,234,168,141,214,167,173,90,197,239,185,207,211,142,238,130,192]
#
# for i in ids:
#     generateNRowLayout(int(i), 1)


def generateLayoutForFoldersMissingLayout():
    orm1 = ORM()
    badFolders = []
    ignoreFolderIds = []
    folderIds = []
    resultset = orm1.session.execute("select collectionId, count(assetId) from collectionMember where collectionId in (select distinct collectionId from collectionMember where geometry is null) group by collectionId;", )
    for fid in resultset:
        if fid[0] not in ignoreFolderIds :
            print("Generating Layout for FolderId:", fid[0])
            try:
                if fid[1] < 20:
                    generateNRow(fid[0], 1)
                elif 20 <= fid[1] < 45:
                    generateNRow(fid[0], 2)
                elif 45 <= fid[1] < 100:
                    generateNRow(fid[0], 3)
                elif 100 <= fid[1] < 200:
                    generateNRow(fid[0], 4)
                elif 200 <= fid[1] < 400:
                    generateNRow(fid[0], 5)
                else:
                    generateNRow(fid[0], 6)
            except Exception as e:
                print("Layout generation Failed", fid[0])
                badFolders.append(fid[0])

    print(badFolders)


generateLayoutForFoldersMissingLayout()

# generateNRow(240, 1)


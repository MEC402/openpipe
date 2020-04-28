import json

import pandas
import os

from openpipeAPI.ORM.BL import BL
from assetSources.CanonicalSchema import CanonicalSchema
from assetSources.ClevelandMuseum import ClevelandMuseum
from assetSources.MetMuseum import MetMuseum
from assetSources.RijksMuseum import RijksMuseum

dir = "curatorsData"
files = os.listdir(dir)
cs = CanonicalSchema().getSchema(1)
sourceTable={'MET':1,'Rijks':2,'Cleveland':3}


def createFolder(name):
    BL().insertIntoCollection(name)


def getAsset(id, museumName):
    if 'Metropolitan' in museumName or "MET" in museumName:
        museumObj = MetMuseum(cs)
    elif 'Cleveland' in museumName:
        museumObj = ClevelandMuseum(cs)
    elif 'Rijksmuseum' in museumName:
        museumObj = RijksMuseum(cs)
    return museumObj.getAssetMetaData(id)


def folderWTAssetsJson(folderName, assetList):
    data = {"folderName": folderName, "assets": assetList}

    with open("curatorsData/cleanData/" + folderName + '.json', 'w') as outfile:
        json.dump(data, outfile)


def readJsonFile(filePath):
    with open(filePath) as f:
        data = json.load(f)
    return data


def transportIndiaData():
    india = pandas.read_excel(dir + "/" + "Checklist - India.xlsx")
    # print(india)
    res = []
    assets = zip(india['Image'].tolist(), india['Museum'])
    for asset in assets:
        res.append({"id": asset[0].split("/")[-1], "source": asset[1]})
    a = []
    for r in res:
        if "?" in r["id"]:
            r["id"] = r["id"].split("?")[0]
        elif "-" in r["id"]:
            r["id"] = (r["id"].split(",")[0])

    for re in res:
        a.append(getAsset(re["id"], re["source"]))

    data = {"folderName": "India", "assets": a}

    with open("curatorsData/cleanData/" + 'india.json', 'w') as outfile:
        json.dump(data, outfile)


def transportIslamicData():
    islamic = pandas.read_excel(dir + "/" + "Checklist - Islamic Ceramics.xlsx")
    res = []
    idList = []
    metaTagList = []
    assets = islamic['MET ASSET ID'].tolist()
    for asset in assets:
        if str(asset).isnumeric():
            idList.append(asset)

    for id in idList:
        metaTagList.append(getAsset(id, "Metropolitan"))

    folderWTAssetsJson("islamic", metaTagList)


def transportPacificData():
    india = pandas.read_excel(dir + "/" + "Checklist - South Pacific.xlsx")
    res = []
    assets = zip(india['URL'].tolist(), india['Museum'])
    for asset in assets:
        res.append({"id": asset[0].split("/")[-1], "source": asset[1]})
    a = []
    for r in res:
        if "?" in r["id"]:
            r["id"] = r["id"].split("?")[0]
        elif "-" in r["id"]:
            r["id"] = (r["id"].split(",")[0])

    for re in res:
        a.append(getAsset(re["id"], re["source"]))

    data = {"folderName": "South Pacific", "assets": a}

    with open("curatorsData/cleanData/" + 'south Pacific.json', 'w') as outfile:
        json.dump(data, outfile)


def transportAfricaData():
    assetData = pandas.read_excel(dir + "/" + "Checklist-Africa.xlsx")
    res = []
    assets = assetData['Persistent URL'].tolist()
    for asset in assets:
        res.append({"id": asset.split("/")[-1], "source": "MET"})
    a = []
    for r in res:
        if "?" in r["id"]:
            r["id"] = r["id"].split("?")[0]
        elif "-" in r["id"]:
            r["id"] = (r["id"].split(",")[0])

    for re in res:
        a.append(getAsset(re["id"], re["source"]))

    data = {"folderName": "Africa", "assets": a}

    with open("curatorsData/cleanData/" + 'africa.json', 'w') as outfile:
        json.dump(data, outfile)


def transportMedievalData():
    excelFile = pandas.ExcelFile(dir + "/" + "Checklist - Medieval Europe with Religious_Secular_Castles_Knights.xlsx")
    sheets=excelFile.sheet_names    # see all sheet names
    for sheet in sheets:
        print(sheet)
        assetData=excelFile.parse(sheet)  # read a specific sheet to DataFrame
        res = []
        assets = zip(assetData['Persistent URLs'].tolist(), assetData['Museum'])
        for asset in assets:
            if("met" in asset[0] or "cleveland" in asset[0]):
                res.append({"id": asset[0].split("/")[-1], "source": asset[1]})
        a = []
        for r in res:
            if "?" in r["id"]:
                r["id"] = r["id"].split("?")[0]
            elif "-" in r["id"]:
                r["id"] = (r["id"].split(",")[0])

        for re in res:
            print(re)
            a.append(getAsset(re["id"], re["source"]))

        data = {"folderName": "Medieval_"+ sheet, "assets": a}

        with open("curatorsData/cleanData/" + "Medieval_"+ sheet +'.json', 'w') as outfile:
            json.dump(data, outfile)


def addAssetsToNewFolder(data):
    print(data["folderName"])
    folderId=BL().insertIntoCollection(data["folderName"])
    assetIDs=[]
    for asset in data["assets"]:
        aid=BL().addAsset(asset)
        assetIDs.append(aid)
    BL().addAssetsToFolder(folderId,assetIDs,'exported from curator Excel file')


def jsonToFolders(filePath):
    data=readJsonFile(filePath)
    addAssetsToNewFolder(data)


files = os.listdir("curatorsData/cleanData/")
for file in files:
    print(file)
    jsonToFolders("curatorsData/cleanData/"+file)

# transportMedievalData()

# transportAfricaData()
# jsonToFolders("curatorsData/cleanData/" + 'africa.json')

# jsonToFolders("curatorsData/cleanData/" + 'islamic.json')

# data = readJsonFile("curatorsData/cleanData/" + 'india.json')
#
# **********************************************************************************************
# *                                   Openpipe data cleaning code                              *
# * ___________________________________________________________________________________________*
# * This code insures that the openpipe assets follow the following specs:                     *
# * a. The openpipe_canonical_date format should be:                                           *
# *     i.    it should not be null                                                            *
# *     ii.   it should be in the format of BC|CE YYYY MMM DD hh:mm:ss                        *
# *                                                                                            *
# * b. Each Asset should have:                                                                 *
# *     i.    All canonical required tags                                                      *
# *     ii.   not null small, large and full Image                                             *
# *                                                                                            *
# *                                                                                            *
# *                                                                                            *
# *                                                                                            *
# **********************************************************************************************
import calendar
import json

from backend.openpipeAPI.ORM.ORM import ORM
import re

from backend.openpipeAPI.ORM.TO import TO

orm = ORM()
tables = TO().getClasses()
MetaTags = tables["metaTag"]


def find_bad_openpipe_canonical_dates():
    stm = """SELECT * FROM metaTag WHERE tagName="openpipe_canonical_date" and value not REGEXP '^(BC)|(CE) [0-9]{1,5} ... [0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]$'"""
    resultSet = orm.session.execute(stm)
    bad_canonical_dates = []
    for r in resultSet:
        info = {"tagId": r.id,
                "metaDataId": r.metaDataId,
                "tagName": r.tagName,
                "value": r.value}
        bad_canonical_dates.append(info)
    return {"total": len(bad_canonical_dates), "data": bad_canonical_dates}


# print(json.dumps(find_bad_openpipe_canonical_dates(), ensure_ascii=False, indent=4, sort_keys=True))


def fixEmptyDates():
    stm = """select * from metaTag where metaDataId in (select metaDataId from metaTag where tagName="openpipe_canonical_date" and value is null)"""
    resultSet = orm.session.execute(stm)
    bad_assets = {}
    for r in resultSet:
        if r.metaDataId in bad_assets:
            bad_assets[r.metaDataId][r.tagName] = {"id": r.id, "value": r.value, 'it': r.insertTime}
        else:
            bad_assets[r.metaDataId] = {r.tagName: {"id": r.id, "value": r.value, 'it': r.insertTime}}

    updates = []
    for asset in bad_assets:
        mid = asset
        # print(asset)
        ba = bad_assets[asset]
        # Fix the ones that have display date
        # ddate=str(ba["openpipe_canonical_displayDate"]['value'])
        # pattern = re.compile("^([0-9]+) CE$")
        # if pattern.match(ddate):
        #     arr=ddate.split(" ")
        #     date_format="CE "+ arr[0] +" JAN 01 00:00:00"
        #     updates.append({"id":ba["openpipe_canonical_date"]["id"],"value":date_format})

        # Fix Local source Dates
        # if "openpipe_canonical_source" in ba:
        #     if ba["openpipe_canonical_source"]["value"] == "Local":
        #         date = ba["openpipe_canonical_date"]["it"]
        #         date_format = "CE " + str(date.year) + " " + str(calendar.month_abbr[date.month]) + " " + str(date.day).zfill(2) + " " + str(date.hour).zfill(2) + ":" + str(date.minute).zfill(2) + ":" + str(date.second).zfill(2)
        #         updates.append({"id": ba["openpipe_canonical_date"]["id"], "value": date_format})
        # else:
        #     print(a)

        # Fix the one with last Date
        # pattern = re.compile("^(BC)|(CE) [0-9]{1,5} ... [0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]$")
        # if "openpipe_canonical_lastDate" in ba:
        #     dd = ba["openpipe_canonical_lastDate"]["value"]
        #     if pattern.match(dd):
        #         updates.append({"id": ba["openpipe_canonical_date"]["id"], "value": dd})
        # elif "openpipe_canonical_firstDate" in ba:
        #     dd = ba["openpipe_canonical_firstDate"]["value"]
        #     if pattern.match(dd):
        #         updates.append({"id": ba["openpipe_canonical_date"]["id"], "value": dd})

        # Fix Cleveland missing date with culture
        dd = re.findall('[0-9]+', ba["culture"]["value"])
        if len(dd) > 0:
            date_format = "CE " + dd[0] + "00" + " JAN 01 00:00:00"
            # print(ba["culture"]["value"], dd[0],date_format)
            updates.append({"id": ba["openpipe_canonical_date"]["id"], "value": date_format})
        else:
            print(ba["culture"]["value"])

        # print(asset)
    orm.bulkUpdate(updates, MetaTags, 100)


def get_file_in_directory(path):
    from os import listdir
    from os.path import isfile, join

    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    return onlyfiles

def set_time_to_zero():
    stm = """SELECT * FROM metaTag WHERE tagName="openpipe_canonical_date" and value not REGEXP '^(BC)|(CE) [0-9]{1,5} ... [0-9][0-9] [0][0]:[0][0]:[0][0]$'"""
    resultSet = orm.session.execute(stm)
    updates=[]
    for r in resultSet:
        date=r.value.split(" ")
        date_format=date[0]+" "+date[1]+" "+date[2]+" "+date[3]+" 00:00:00"
        updates.append({"id": r.id, "value": date_format})
    print(updates)
    orm.bulkUpdate(updates, MetaTags, 100)


# get_file_in_directory()

print(find_bad_openpipe_canonical_dates())

# set_time_to_zero()


def
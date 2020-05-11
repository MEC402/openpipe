#!/bin/python3

"""

    Running Command : python ConvertDataBaseImageToPNG <Integer ID of the image in the DataBase>


"""

import requests
import os
from webdav3.client import Client
from backend.ORM.ORM import ORM


def dl_convert_img(asset):
    # check if the image is already converted and sotred in the image table in the dataBase
    # add the image id if not with the path for the image if it was not converted before.

    filename = asset["filename"][0]
    newFormat = asset["shortname"][0] + ".PNG"
    ImageToConvert = os.getcwd() + "/" + filename

    response = requests.get(asset['uri'][0])

    file = open(filename, "wb")
    file.write(response.content)
    file.close()

    os.system("dcraw -c {0} | pnmtopng >>{1}".format(ImageToConvert, newFormat))
    os.system("rm *.CR2")
    command = "curl -T {} -u openpipedev:openPipeArtMaster51 http://mec402.boisestate.edu/webdav/".format(newFormat)
    os.system(command)

    return "http://mec402.boisestate.edu/webdav/{}.PNG".format(newFormat)


def converting_images():
    orm = ORM()
    select_query_images = "SELECT id, shortname ,filename,uri,master FROM images where master=\"master5\";"
    insert_query_metaData = 'INSERT INTO metaData values ()'
    select_ID_metaData = "SELECT id FROM metaTag ORDER BY id DESC LIMIT 1;"
    meta_data_ids = orm.executeSelect(select_ID_metaData)

    result = orm.executeSelect(select_query_images)
    id_counter = meta_data_ids["data"][0]['id'][0]
    for item in result["data"]:
        id_counter + 1
        # print(item["shortname"][0])
        orm.insert(insert_query_metaData)
        url = dl_convert_img(item)
        insert_query_metaTags = " INSERT INTO metaTag VALUES ( {},\"web_image\" ,{} )".format(id_counter, url)
        orm.insert(insert_query_metaTags)


if __name__ == '__main__':
    converting_images()

#!/bin/python3

"""

    Running Command : python ConvertDataBaseImageToPNG <Integer ID of the image in the DataBase>


"""

import urllib.request

import os
from webdav3.client import Client
import urllib
from backend.ORM.ORM import ORM

# connect to the WebDav Server

options = {
    'webdav_hostname': "http://mec402.boisestate.edu/webdav/",
    'webdav_login': "openpipedev",
    'webdav_password': "openPipeArtMaster51",
}
web_dav = Client(options)


def dl_convertImg(asset):
    # check if the image is already converted and sotred in the image table in the dataBase
    # add the image id if not with the path for the image if it was not converted before.

    filename = asset["filename"][0]
    newFormat = asset["shortname"][0] + ".PNG"
    ImageToConvert = os.getcwd() + "/" + filename

    urllib.request.urlretrieve(asset['uri'][0], filename)

    os.system("dcraw -c {0} | pnmtopng >>{1}".format(ImageToConvert, newFormat))
    os.system("rm *.CR2")
    command = "curl -T {} -u openpipedev:openPipeArtMaster51 http://mec402.boisestate.edu/webdav/".format(newFormat)
    os.system(command)

    return "http://mec402.boisestate.edu/webdav/{}.PNG".format(newFormat)


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
    url = dl_convertImg(item)
    insert_query_metaTags = " INSERT INTO metaTag VALUES ( {},\"web_image\" ,{} )".format(id_counter, url)
    orm.insert(insert_query_metaTags)

if __name__ == '__main__':
    pass

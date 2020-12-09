import traceback
import urllib
import urllib.request as urllib2
from io import BytesIO
from PIL import Image
from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO


def convertImageFromURL(url, path, thPath, fileName, thFileName):
    try:
        url = urllib.parse.quote(url, safe="%/:=&?~#+!$,;'@()*[]")
        response = urllib2.urlopen(url)
        status_code = response.getcode()
        if status_code == 200:
            file = response.read()
            image = Image.open(BytesIO(file))
            thImage = image.resize((300, 300))
            image.save(path + fileName + ".jpeg")
            thImage.save(thPath + thFileName + ".jpeg")
            return True
    except Exception as e:
        print(e)
        return False


orm = ORM()
tables = TO().getClasses()
MetaTag = tables["metaTag"]
res = orm.executeSelect(
    """select asset.id,asset.metaDataId,a.value,a.id as tagId from (select * from metaTag where tagName='openpipe_canonical_smallImage') as a join asset on asset.metaDataId=a.metaDataId where a.value not like '%mec402%';""")

path = "/WorldMuseum/fileStore/assetImages/"
thPath = "/WorldMuseum/fileStore/imageThumbnails/"

# path = "assetImages/"
# thPath = "imageThumbnails/"

destURL = "http://mec402.boisestate.edu/wmuseum/fileStore/assetImages/"
thDestURL = "http://mec402.boisestate.edu/wmuseum/fileStore/imageThumbnails/"

substURL = "http://mec402.boisestate.edu/assets/smallImage.jpg"
thSubstURL = "http://mec402.boisestate.edu/assets/thumbnail.jpg"

for r in res['data']:
    if r['value'][0] != "{BASEURI}/smallImage.jpg":
        print(r["id"][0], r["metaDataId"][0], r['value'][0])
        fileName = "Local_Copy_" + str(r["id"][0])
        thFileName = "Thumbnail_" + str(r["id"][0])
        if convertImageFromURL(r['value'][0], path, thPath,fileName,thFileName):
            # print("Image Found")
            orm.insert(MetaTag(metaDataId=r["metaDataId"][0], tagName="openpipe_ImageLocalCopy",
                               value=destURL + fileName + ".jpeg"))
            orm.insert(MetaTag(metaDataId=r["metaDataId"][0], tagName="openpipe_Thumbnails",
                               value=thDestURL + thFileName + ".jpeg"))
        else:
            print("Image Not Found")
            orm.insert(MetaTag(metaDataId=r["metaDataId"][0], tagName="openpipe_ImageLocalCopy", value=substURL))
            orm.insert(MetaTag(metaDataId=r["metaDataId"][0], tagName="openpipe_Thumbnails",
                               value=thSubstURL))
#
# # print(i,j,i+j)
orm.commitClose()

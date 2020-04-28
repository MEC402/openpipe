import traceback
import urllib.request as urllib2
from io import BytesIO
from multiprocessing.pool import ThreadPool

from PIL import Image
from requests import get

#import Slack


class ImageUtil:
    def __init__(self):
        self.fullImage = None

    def getPixelDimentions(self, url):
        """ Get all the canonical tags from DB and Returns a json obj.
            Parameter
            ---------

            Returns
            -------
            JSON
                {
                ...,
                tagName:Default value,
                ...
                }
        """
        width = 0
        height = 0
        if url is not None and url != "":
            try:
                url = url.replace(" ", "%20")
                print(url)
                file = get(url)
                im = Image.open(BytesIO(file.content))
                width, height = im.size
            except Exception as e:
                track = traceback.format_exc()
#                Slack.sendMessage(track)
        return width, height

    def concatTiles(self, tilesData, imageWidth, imageHeight):
        tileWidth, tileHeight = self.getPixelDimentions(tilesData[0]["url"])
        fullImage = Image.new('RGB', (imageWidth, imageHeight))
        pool = ThreadPool(len(tilesData))
        results = []
        for tileInfo in tilesData:
            results.append(pool.apply_async(self.getTile, args=[tileInfo, tileWidth, tileHeight]))
        pool.close()
        pool.join()
        results = [r.get() for r in results]
        for r in results:
            # print(r)
            fullImage.paste(r["image"], (r["width"], r["height"]))
        return fullImage

    def getTile(self, tileInfo, tileWidth, tileHeight):
        url = tileInfo["url"].replace(" ", "%20")
        file = urllib2.urlopen(urllib2.Request(url, headers={"Range": "5000"})).read()
        tileImage = Image.open(BytesIO(file))
        # print(str(int(tileInfo["x"]) * tileWidth) + "," + str(int(tileInfo["y"]) * tileHeight))
        return {"image": tileImage,
                "width": int(tileInfo["x"]) * tileWidth,
                "height": int(tileInfo["y"]) * tileHeight}

    def convertImageFromURL(self, url, path, fileName, conversionType):
        # TODO: Check for the conversion type to be a valid type that pil supports
        file = urllib2.urlopen(urllib2.Request(url, headers={"Range": "5000"})).read()
        image = Image.open(BytesIO(file))
        image.save(path + fileName + "." + conversionType)

import urllib.request as urllib2
from io import BytesIO
from multiprocessing.pool import ThreadPool

from PIL import Image


class ImageUtil:
    def __init__(self):
        self.fullImage = None

    def getPixelDimentions(self, url):
        url = url.replace(" ", "%20")
        file = urllib2.urlopen(urllib2.Request(url, headers={"Range": "5000"})).read()
        im = Image.open(BytesIO(file))
        width, height = im.size
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
            #print(r)
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

    def convertImageFromURL(self,url,conversionType):
        file = urllib2.urlopen(urllib2.Request(url, headers={"Range": "5000"})).read()
        image = Image.open(BytesIO(file))
        image.save("a"+"."+conversionType)

# def getImageInfo(data):
#     data = data
#     size = len(data)
#     #print(size)
#     height = -1
#     width = -1
#     content_type = ''
#
#     # handle GIFs
#     if (size >= 10) and data[:6] in (b'GIF87a', b'GIF89a'):
#         # Check to see if content_type is correct
#         content_type = 'image/gif'
#         w, h = struct.unpack(b"<HH", data[6:10])
#         width = int(w)
#         height = int(h)
#
#     # See PNG 2. Edition spec (http://www.w3.org/TR/PNG/)
#     # Bytes 0-7 are below, 4-byte chunk length, then 'IHDR'
#     # and finally the 4-byte width, height
#     elif ((size >= 24) and data.startswith(b'\211PNG\r\n\032\n')
#           and (data[12:16] == b'IHDR')):
#         content_type = 'image/png'
#         w, h = struct.unpack(b">LL", data[16:24])
#         width = int(w)
#         height = int(h)
#
#     # Maybe this is for an older PNG version.
#     elif (size >= 16) and data.startswith(b'\211PNG\r\n\032\n'):
#         # Check to see if we have the right content type
#         content_type = 'image/png'
#         w, h = struct.unpack(b">LL", data[8:16])
#         width = int(w)
#         height = int(h)
#
#     # handle JPEGs
#     elif (size >= 2) and data.startswith(b'\377\330'):
#         content_type = 'image/jpeg'
#         jpeg = io.BytesIO(data)
#         jpeg.read(2)
#         b = jpeg.read(1)
#         try:
#             while (b and ord(b) != 0xDA):
#                 while (ord(b) != 0xFF): b = jpeg.read(1)
#                 while (ord(b) == 0xFF): b = jpeg.read(1)
#                 if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
#                     jpeg.read(3)
#                     h, w = struct.unpack(b">HH", jpeg.read(4))
#                     break
#                 else:
#                     jpeg.read(int(struct.unpack(b">H", jpeg.read(2))[0])-2)
#                 b = jpeg.read(1)
#             width = int(w)
#             height = int(h)
#         except struct.error:
#             pass
#         except ValueError:
#             pass
#
#     return content_type, width, height
#
#

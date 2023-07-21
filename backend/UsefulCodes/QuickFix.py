from PIL import Image


def fixUploadedImageSizes():
    alist = [12286, 12604, 12606, 12608, 12609, 12610, 12611, 12649, 12650, 12651, 12652]
    inPath = "/var/www/html/assets/uploads/"
    thpath = "/WorldMuseum/fileStore/imageThumbnails/"
    lpath = "/WorldMuseum/fileStore/assetImages/"

    for asset in alist:
        print(asset)
        fileName = "Local_Copy_"+str(asset)
        thFileName = "Thumbnail_"+str(asset)
        image = Image.open(inPath + "Local_uploaded_asset_" + str(asset) + ".png")
        thImage = image.resize((300, 300))
        image.save(lpath + fileName + ".png")
        thImage.save(thpath + thFileName + ".jpg")

        print(lpath + fileName + ".png")
        print(thpath + thFileName + ".jpg")


# fixUploadedImageSizes()

def fixUploadedAssetsDim():


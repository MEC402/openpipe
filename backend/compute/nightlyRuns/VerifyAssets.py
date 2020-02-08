from ORM.BL import BL


class VerifyAsset:
    def listAssetsWithBadImageLinks(self):
        return

    def listAssetsWithoutImage(self):
        bl = BL()
        return bl.getAssetsWithoutImages()

    def verifyImageLinks(self):
        return

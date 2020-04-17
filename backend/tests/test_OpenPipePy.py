from pythonAPI.OpenPipePy import OpenPipePy


class TestOpenPipePy():
    def test_addAsset(self):
        self.fail()

    def test_getAllAssets(self):
        result = OpenPipePy().getAllAssets(1, 10, '1900-01-01', '5000-01-01')
        assert ("total" in result)

    def test_addAssetToFolder(self):
        self.fail()

    def test_deleteFolderMember(self):
        self.fail()

    def test_addFolder(self):
        self.fail()

    def test_updateFolder(self):
        self.fail()

    def test_deleteFolder(self):
        self.fail()

    def test_getFolder(self):
        result = OpenPipePy().getFolder(27)
        assert ("total" in result)

    def test_getAllFolders(self):
        result = OpenPipePy().getAllFolders(3)
        assert ("total" in result)

    def test_getPublicAssetsInFolder(self):
        result = OpenPipePy().getPublicAssetsInFolder(27, 1, 10)
        assert ("total" in result)

    def test_addMetaTag(self):
        self.fail()

    def test_addBatchMetaTags(self):
        self.fail()

    def test_deleteMetaTag(self):
        self.fail()

    def test_updateCanonicalMetaTag(self):
        self.fail()

    def test_getCanonicalMetaTags(self):
        result = OpenPipePy().getCanonicalMetaTags()
        assert ("total" in result)

    def test_addMetaData(self):
        self.fail()

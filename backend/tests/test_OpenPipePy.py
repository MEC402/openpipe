from pythonAPI.OpenPipePy import OpenPipePy


class TestOpenPipePy():
    def test_addAsset(self):
        pass

    def test_getAllAssets(self):
        result = OpenPipePy().getAllAssets(1, 10, '1900-01-01', '5000-01-01', 1)
        assert ("total" in result)

    def test_addAssetToFolder(self):
        pass

    def test_deleteFolderMember(self):
        pass

    def test_addFolder(self):
        pass

    def test_updateFolder(self):
        pass

    def test_deleteFolder(self):
        pass

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
        pass

    def test_addBatchMetaTags(self):
        pass

    def test_deleteMetaTag(self):
        pass

    def test_updateCanonicalMetaTag(self):
        pass

    def test_getCanonicalMetaTags(self):
        result = OpenPipePy().getCanonicalMetaTags()
        assert ("openpipe_canonical_artist" in result)

    def test_addMetaData(self):
        pass

    def test_guid_folders(self):
        result = OpenPipePy().guid("folder/")
        assert ("total" in result)

    def test_guid_folder(self):
        result = OpenPipePy().guid("folder/28")
        assert ("total" in result)

    def test_guid_assets(self):
        result = OpenPipePy().guid("asset/")
        assert ("total" in result)

    def test_guid_asset(self):
        result = OpenPipePy().guid("asset/1")
        assert ("total" in result)

    def test_guid_artists(self):
        result = OpenPipePy().guid("artist/")
        assert ("total" in result)

    def test_guid_artist(self):
        result = OpenPipePy().guid("artist/1")
        assert ("total" in result)

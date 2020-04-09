from pythonAPI.OpenPipePy import OpenPipePy


def testGetPublicAssets():
        result=OpenPipePy().getPublicAssetsInFolder(20,1,10)
        assert ("total" in result)



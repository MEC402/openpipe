from pythonAPI.OpenPipePy import OpenPipePy


def testGetPublicAssets():
    result = OpenPipePy().getPublicAssetsInFolder(20, 1, 10)
    assert ("total" in result)


def testGetAllFolders():
    result = OpenPipePy().getAllFolders(10)
    assert ("total" in result)

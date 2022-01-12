"""
This script verify each asset to insure it follows the formatting available here:

"""
from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

"""
Loads the verifier configuration
"""
# TODO: Read the config from file rather than hard coding it
def loadConfig():
    config={
        "localImage":{
            "small":{
                "path":"",
                "prefix":""
            },
            "large":{
                "path":"",
                "prefix":""
            },
            "full": {
                "path":"",
                "prefix":""
            },
        }
    }

"""
Checks assets metaTags and mark wrong ones
"""
def verifyAsset(asset):
    # check Asset has all the canonical metaTags

    # check Asset has Local thumbnail and Large and Full Image

    # check Asset has dimensions of thumbnail and Large and Full Image

    # check Asset openpipe_canonical_date follows the (CE|BC) YYYY:MMM:dd format or null

    # No Null, undefined, unknown, ect value for metaTags they all should be empty string

    # Asset last modified should be > max(metaTags.lastModified)

    #


def verifyFolder():
    # Folder image has a local thumbnail



"""
Checks all the assets in the database that their SysVerified flag is 0
If the
"""
def runAssetVerifier():
    tables = TO().getClasses()
    MetaTag = tables["metaTag"]
    Asset = tables["asset"]

    orm=ORM().session
    orm.query()


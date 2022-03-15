import BL_Assets as bl_assets
import  BL_Folders as bl_folders

def test_getAllAssets():
    a=bl_assets.getAllAssets(1,10, '2020-01-01', '2020-11-01')
    print(a)

def test_getAllFolderIDs():
    a=bl_folders.getAllFolderIDs()
    print(a)

def test_get_folder_by_id():
    a = bl_folders.getFolderByID(28)
    print(a)

def test_get_folders():
    a = bl_folders.getFolders(1,10)
    print(a)

test_get_folders()
















['openpipe_canonical_artist','openpipe_canonical_title','openpipe_canonical_date','openpipe_canonical_Moment','openpipe_canonical_medium','openpipe_canonical_Technique','openpipe_canonical_country','openpipe_canonical_culture','openpipe_canonical_period','openpipe_canonical_biography','openpipe_canonical_longitude','openpipe_canonical_latitude','openpipe_canonical_classification','openpipe_canonical_Object_Type','openpipe_canonical_Region','openpipe_canonical_largeImageDimensions']






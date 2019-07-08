panorama database tools for maintaining and updating panorama entries

Tool List

pgetidir #--> get the name of the current ingest folder
pgetidir --new #create a new ingest folder record in the database





SQL Schema

Tables:
ifolders -> ingest folders
timestamp, basename,foldername,

ifiles -> list of image files all records.
fullpath, filename, panorama id, status

panoramas -> list of panoramas
panorama id, pair id, 



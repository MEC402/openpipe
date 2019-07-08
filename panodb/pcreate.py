#pcreate
#create an initial panorama database for importing
#
# tables:
#   images
#   ingests
#   panoramas
#   equirect
#   tilesets
#
import sqlite3
import pipeconfig

# Creates or opens a file called mydb with a SQLite3 DB
dbase = pipeconfig.GBASE +"/" + pipeconfig.GPIPE + "/" + pipeconfig.GDBASE
print(dbase)
pdb = sqlite3.connect(dbase)
pdb.execute('''CREATE TABLE images (date text, folder text, filename text, panorama int, ingest int, eye text)''')
pdb.execute('''CREATE TABLE ingests (date text, basefolder text, folder text, eye text, site text)''')
pdb.execute('''CREATE TABLE panoramas (date text, panoname text, leftpano text, rightpano text, numimages int)''')
pdb.execute('''CREATE TABLE equirect (date text, folder text, filename text, panorma int)''')
pdb.execute('''CREATE TABLE tilesets (date text, folder text, filename text, panorama int)''')
pdb.commit();

pdb.close();

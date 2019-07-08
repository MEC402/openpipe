#!/bin/bash

set -x
#get arguments
eqdir=$1
sitedir=$2

#build tiledirectory
mkdir ${sitedir}/panotiles

#extract eqlist
eqlist=`(cd ${eqdir}; ls *.png )`

#generate tiles for each panorama
for v in ${eqlist}
do
#generate 
    mkdir ${sitedir}/panotiles/${v%.png}
    python3.6 generate_tiles.py ${eqdir}/${v} ${sitedir}/panotiles/${v%.png}/left 4 /data/scratch
done



#generate previews
#echo python3.6 mkpreviews.py ${sitedir}/panotiles


#generate JSON files
(cd ${sitedir}; python3.6 ~/builds/openpipe/pipetiles/genpjson.py panotiles > panoramas.json)

#put in the html files
cp -r ~/builds/openpipe/webtemplate/* ${sitedir}/

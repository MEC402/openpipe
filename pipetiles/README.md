# pipeline
collection of tools and software for producing VR and Mixed Reality Content.


#expected tileset directory structure for Web:

.../panotiles/
              {panoname}/left/{left_tiles}  #this is the mono tile set
              {panoname}/right/{right_tiles}

#tileset individual directory files
...{panoname}/left/{left_tiles}
...{panoname}/left/preview.png #6 sides of cube face preview
...{panoname}/left/icon.png #splash image for contact sheet



#steps to generate web directory set:

for a set of panoramas we generate all of the needed tile in the create directory structure:

create ...{sitename}/panotiles/  #directory top level
create ...{sitename}/panotiles/{panoname}/left/

create the individual tiles for left or Mono in
chop_me.py ...{sitename}/panotiles/{panoname}/left
chop_me.py ...{sitename}/panotiles/{panoname}/right #if right exists

create the preview file 
mkpreview.py ...{sitename}/panotiles/{panoname}/left/
mkpreview.py ...{sitename}/panotiles/{panoname}/right/ #if right exists

create the icon file
mkicon.py ...{sitename}/panotiles/{panoname}/{left,right}

Generate json file
genpjson.py ...{sitename}


#generate the web content
copy javascript and index pages from webtemplate/ ...{sitename}/
-->all info should be automatically pulled from JSON files.


#copy to web server
copy ...{sitename} webserver:public_html/{sitename}

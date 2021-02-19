import json
import ast

def cleanList(stlist):
    reslist = []
    if len(stlist) == 0:
        reslist.append("unknown")
        return reslist

    for i in stlist:
        if i is None or not i.strip():
           reslist.append("unknown")
        else:
           reslist.append(i.strip())
        return reslist

def ClevelandArtist(artistlist):
    tmp = []
#    print(artistlist)
    shortname = artistlist[0]
    if '"' in shortname:
      sdict = ast.literal_eval(shortname)
    elif "'" in shortname:
      sdict = ast.literal_eval(shortname)
    else:
      sdict = [{"description": "clevelandbadartist"}]
       
#    print(sdict,"Not Cleveland")
#    shortname = shortname.replace("'",'"')
#    shortname = shortname.replace("None",'"None"')
#    print(shortname,"cleveland")
#    ajson = json.loads(shortname)
#    ajson = json.loads(shortname)
#    print(sdict, "ARTSTME")
    for c in sdict:
      aname = c["description"]
      tmp.append(aname)
    return cleanList(tmp)

def RijksArtist(artistlist):
    tmp = []
#    print(artistlist)
    shortname = artistlist[0]
    if '"' in shortname:
      sdict = ast.literal_eval(shortname)
    elif "'" in shortname:
      sdict = ast.literal_eval(shortname)
    else:
      sdict = [{"name": "unknown"}]
       
#    print(sdict,"Not Cleveland")
#    shortname = shortname.replace("'",'"')
#    shortname = shortname.replace("None",'"None"')
#    print(shortname,"cleveland")
#    ajson = json.loads(shortname)
#    ajson = json.loads(shortname)
#    print(sdict, "ARTSTME")
    for c in sdict:
      aname = c["name"]
      tmp.append(aname)
    return cleanList(tmp)

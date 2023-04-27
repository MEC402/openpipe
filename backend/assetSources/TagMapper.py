#TagMapper.py
# functions to extrad data from museum src tags and return them 
# prepared for storage in destination tags.

#loop through the json tag list and extract and return
def mapTags(data,tagmapjson,schema):
    response = {}
    response = schema.copy()

    for m in tagmapjson["canons"]:
       afunction = "none"
       if "function" in m:
          afunction = m["function"]

       dstres = mapOneTag(data,m["code"],m["src"],afunction)
       response[m["dst"]] = dstres

    #print(response)
    return (response)

def toString(aval):
     stringres = str(aval)
     return (stringres)

def mapOneTag(data,code, src, function):
       if (code == "STATIC"):
            #print("STATIC " + src)
            return (src)
       elif (code == "COPY"):
            #print("COPY " + " " + src)
            #print(data[src])
            return (toString(data[src]))

       return "";

    

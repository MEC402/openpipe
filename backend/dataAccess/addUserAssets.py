#! C:/Users/walluser/AppData/Local/Programs/Python/Python38-32/python.exe


import cgi, cgitb
cgitb.enable(display=1, logdir="")

form = cgi.FieldStorage()


    

print ("Content-Type: text/html")
print ("") #use this double quote print statement to add a blank line in the script
print ("<b>Hello python</b>")
print(form)

# insert into database
#print(json.dumps(BL().insertUserAsset(data), default=str))
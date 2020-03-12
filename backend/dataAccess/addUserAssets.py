#! C:/Users/walluser/AppData/Local/Programs/Python/Python38-32/python.exe
import cgi, os
import cgitb; cgitb.enable()
cgitb.enable(display=1, logdir="~/added_user_assets_logs/")




print("Content-Type: text/html")    # HTML is following
print() 


form = cgi.FieldStorage()

fileitem = form["file"]
if fileitem.file:
    fn = os.path.basename(fileitem.filename)
    open('~/added_user_assets/'+fn, 'wb').write(fileitem.file.read())
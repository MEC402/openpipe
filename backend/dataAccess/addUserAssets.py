#! C:/Users/walluser/AppData/Local/Programs/Python/Python38-32/python.exe
import cgi, os
import cgitb; cgitb.enable()
cgitb.enable(display=1, logdir="C:/Users/walluser/Desktop/logs")




print("Content-Type: text/html")    # HTML is following
print() 


form = cgi.FieldStorage()

fileitem = form["file"]
if fileitem.file:
    fn = os.path.basename(fileitem.filename)
    
   # open('C:/Users/walluser/Desktop/logs/'+fn, 'wb').write(fileitem.file.read())
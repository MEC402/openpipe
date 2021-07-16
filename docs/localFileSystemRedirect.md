 To redirect the images coming from the main filestore to local one we need to do these 3 steps:

 1. Start the local server inside the OpenpipeLocalData Directory using (The defualt port is 8000): python -m ComplexHTTPServer [port#]
 2. Go to C:\Windows\System32\drivers\etc and open the hosts file in admin mod and add the following lines:
 
127.0.0.1         localhost
127.0.0.1    mec402.boisestate.edu
127.0.0.1    www.mec402.boisestate.edu

 3. To do the port mapping run the following command in a cmd admin: netsh interface portproxy add v4tov4 listenport=80 listenaddress=127.0.0.1 connectport=8000 connectaddress=127.0.0.1

Test it through the browser to make sure it works.



You can see the entry you have added with the command:

netsh interface portproxy show v4tov4

You can remove the entry with the following command:

netsh interface portproxy delete v4tov4 listenport=80 listenaddress=127.0.0.1

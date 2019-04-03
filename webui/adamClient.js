class Adam 
{ // art digital asset manager
    constructor(name) 
    {
       this.name = name;
      console.log("ADAM:construct");
    }

    connect(aURI)
    {
      this.myuri = aURI;
      console.log("ADAM:Connect");
    }

    // get the number of rows in a named table
    getNumRows(atable)
    {
        return 3;   // empty for now
    }
    // get rows from the named table
    getRows(atable, fist, last)
    {
       var xhttp = new XMLHttpRequest();
       xhttp.onreadystatechange = function() 
       {
         if (this.readyState == 4 && this.status == 200) 
         {
             var myrows = JSON.parse(this.responseText);
             //document.getElementById("wmlist").innerHTML=this.responseText;
             var aplace = document.getElementById("imgtable");
             addViewList(aplace,myrows);
         }
 
       }
       xhttp.open("GET","adam1.php",true);
       xhttp.send();
       return [["row1","name2","name3"],
               ["row2","name2","name3"],
               ["row3","name2","name3"]];
    }

    getComments(atable, imgid)
    {
       var xhttp = new XMLHttpRequest();
       xhttp.onreadystatechange = function() 
       {
         if (this.readyState == 4 && this.status == 200) 
         {
             var myrows = JSON.parse(this.responseText);
             //document.getElementById("wmlist").innerHTML=this.responseText;
             var aplace = document.getElementById("imgtable");
             addViewCommentList(aplace,myrows);
         }
 
       }
       var qstring = 'adamComments.php?imgid='+imgid;
       xhttp.open("GET",qstring,true);
       xhttp.send();
       return [["row1","name2","name3"],
               ["row2","name2","name3"],
               ["row3","name2","name3"]];
    }

    adamUpdateComment(comid,acomment)
    {
       var xhttp = new XMLHttpRequest();
       xhttp.onreadystatechange = function() 
       {
         if (this.readyState == 4 && this.status == 200) 
         {
             console.log('do a page refresh');
             document.location.reload(true);
         }
 
       }
       var qstring = 'adamUpdateComment.php?commentid='+comid
                      +'&comment='+acomment;
       console.log(qstring);
       xhttp.open("GET",qstring,true);
       xhttp.send();
    }

    DeleteComment(comid)
    {
       var xhttp = new XMLHttpRequest();
       xhttp.onreadystatechange = function() 
       {
         if (this.readyState == 4 && this.status == 200) 
         {
             console.log('do a page refresh');
             document.location.reload(true);
         }
 
       }
       var qstring = 'adamDeleteComment.php?commentid='+comid;
       console.log(qstring);
       xhttp.open("GET",qstring,true);
       xhttp.send();
    }
    NewComment(aimgid)
    {
       var xhttp = new XMLHttpRequest();
       xhttp.onreadystatechange = function() 
       {
         if (this.readyState == 4 && this.status == 200) 
         {
             console.log('do a page refresh');
             document.location.reload(true);
         }
 
       }
       var qstring = 'adamNewComment.php?imgid='+aimgid;
       console.log(qstring);
       xhttp.open("GET",qstring,true);
       xhttp.send();
    }

    // get the names of the columes for a specific table 
    getColNames(atable)
    {
       return ["name1","name2","name3"];
    }

}


